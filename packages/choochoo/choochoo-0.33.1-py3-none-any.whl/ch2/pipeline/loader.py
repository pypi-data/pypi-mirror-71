
from collections import defaultdict, namedtuple
from logging import getLogger
from time import sleep

from sqlalchemy.exc import IntegrityError

from ..commands.args import UNLOCK
from ..sql import StatisticJournal, StatisticName, Dummy, Interval
from ..sql.tables.statistic import STATISTIC_JOURNAL_CLASSES, STATISTIC_JOURNAL_TYPES
from ..sql.types import short_cls

log = getLogger(__name__)


class StatisticJournalLoader:

    # we want to load multiple tables (because we're using inheritance) quickly and safely.
    # to do this, we need to generate IDs ourselves (to avoid reading the ID for the base class)
    # on sqlite we can do this by:
    # - using a single transaction
    # - starting to write (a dummy StatisticJournal, which also gets us the last ID)
    # - calculating IDs from the dummy ID
    # - writing the data (still in the same transaction)
    # - removing the dummy
    # - committing
    # afaict that would work on any SQL database with a reasonable level of isolation.
    # what is special to sqlite is that the final commit will not fail, because there is only ever one
    # process writing (this is true even when using multiple processes)

    # well the above worked for a while. then started throwing exceptions, so i needed to add
    # the while loop below.

    def __init__(self, s, owner, add_serial=True, clear_timestamp=True, abort_after=100):
        self._s = s
        self._owner = owner
        self.__statistic_name_cache = dict()
        self.__staging = defaultdict(list)
        self.__latest = dict()
        self.__add_serial = add_serial
        self.__start = None
        self.__finish = None
        self.__last_time = None
        self.__serial = 0 if add_serial else None
        self.__clear_timestamp = clear_timestamp
        self.__abort_after = abort_after
        self.__counts = defaultdict(lambda: 0)

    @property
    def start(self):
        return self.__start

    @property
    def finish(self):
        return self.__finish

    def __bool__(self):
        return bool(self.__staging)

    def load(self):
        if not self.__start:
            log.warning('No data to load')
            return
        self._s.commit()
        dummy = self._preload()
        try:
            self._load_ids(dummy)
        except Exception:
            self._s.rollback()
            # dummy may have been deleted in the rollback - it depends if there were any intermediate commits
            # (which is a whole other problem), so to be sure...
            self.unlock(self._s)
            raise
        self._postload()

    def _preload(self):
        dummy_source, dummy_name = Dummy.singletons(self._s)
        dummy, count = None, 0
        while not dummy:
            try:
                log.debug(f'Trying to acquire database ({count})')
                dummy = StatisticJournal(source=dummy_source, statistic_name=dummy_name, time=0.0)
                self._s.add(dummy)
                self._s.flush()
                log.debug('Acquired database')
            except IntegrityError:
                log.debug('Failed to acquire database')
                self._s.rollback()
                dummy, count = None, count+1
                if count > self.__abort_after:
                    raise Exception(f'Could not acquire database after {count} attempts '
                                    f'(you may need to use `ch2 {UNLOCK}` once all workers have stopped)')
                sleep(0.1)
        log.debug(f'Dummy ID {dummy.id}')
        return dummy

    def _load_ids(self, dummy):
        rowid, count = dummy.id + 1, 0
        for type in self.__staging:
            log.debug('Loading %d values for type %s' % (len(self.__staging[type]), short_cls(type)))
            for i in range(min(5, len(self.__staging[type]))):
                sjournal = self.__staging[type][i]
                log.debug(f'Example: {sjournal.value} at {sjournal.time}')
            for sjournal in self.__staging[type]:
                sjournal.id = rowid
                rowid += 1
            self._s.bulk_save_objects(self.__staging[type])
            count += len(self.__staging[type])
        self._s.commit()
        log.info(f'Loaded {count} statistics')
        log.debug('Removing Dummy')
        self._s.delete(dummy)
        self._s.commit()
        log.debug('Dummy removed')

    def _postload(self):
        # manually clean out intervals because we're doing a fast load
        if self.__clear_timestamp and self.start and self.finish:
            Interval.mark_dirty_times(self._s, self.start, self.finish)
            self._s.commit()

    @classmethod
    def unlock(cls, s):
        dummy_source, dummy_name = Dummy.singletons(s)
        s.query(StatisticJournal). \
            filter(StatisticJournal.source == dummy_source,
                   StatisticJournal.statistic_name == dummy_name).delete()
        s.commit()

    def add(self, name, units, summary, source, value, time, cls, description=None, title=None):

        if value is None:
            raise Exception(f'Trying to save null value for {name}')
        if value != value:
            raise Exception(f'Trying to save nan value for {name}')

        # note that name is used as title if title is None, and name is reduced to a simple name.
        # so legacy code works correctly

        if self.__add_serial:
            if self.__last_time is None:
                self.__last_time = time
            elif time > self.__last_time:
                self.__last_time = time
                self.__serial += 1
            elif time < self.__last_time:
                raise Exception('Time travel - timestamp for statistic decreased')

        self.__start = min(self.__start, time) if self.__start else time
        self.__finish = max(self.__finish, time) if self.__finish else time

        if name not in self.__statistic_name_cache:
            if not description: log.warning(f'No description for {name} ({self._owner})')
            self.__statistic_name_cache[name] = \
                StatisticName.add_if_missing(self._s, name, STATISTIC_JOURNAL_TYPES[cls],
                                             units, summary, self._owner, 
                                             description=description, title=title)

        try:
            source = source.id
        except AttributeError:
            pass  # literal id
        statistic_name = self.__statistic_name_cache[name]
        journal_class = STATISTIC_JOURNAL_CLASSES[statistic_name.statistic_journal_type]
        if cls != journal_class:
            raise Exception(f'Inconsistent class for {name}: {cls}/{journal_class}')
        instance = journal_class(statistic_name_id=statistic_name.id, source_id=source, value=value,
                                 time=time, serial=self.__serial)
        if name in self.__latest:
            prev = self.__latest[name]
            if instance.time > prev.time:
                self.__latest[name] = instance
                self.__staging[journal_class].append(instance)
                self.__counts[name] += 1
            elif instance.time == prev.time:
                if instance.value == prev.value:
                    log.debug(f'Skipping duplicate for {name}')
                else:
                    self._resolve_duplicate(name, instance, prev)
            else:
                self.__staging[journal_class].append(instance)
                self.__counts[name] += 1
        else:
            self.__latest[name] = instance
            self.__staging[journal_class].append(instance)
            self.__counts[name] += 1

    def _resolve_duplicate(self, name, instance, prev):
        raise Exception(f'Duplicate time ({prev.time}) for {name} ({instance.value}/{prev.value})')

    def latest(self, name, constraint):
        return self.__latest.get((name, constraint))

    def as_waypoints(self, names):
        Waypoint = make_waypoint(names.values())
        time_to_waypoint = defaultdict(lambda: Waypoint())
        statistic_ids = dict((name.id, name) for name in self.__statistic_name_cache.values())
        for type in self.__staging:
            for sjournal in self.__staging[type]:
                name = statistic_ids[sjournal.statistic_name_id].name
                if name in names:
                    time_to_waypoint[sjournal.time] = \
                        time_to_waypoint[sjournal.time]._replace(**{'time': sjournal.time,
                                                                    names[name]: sjournal.value})
        return [time_to_waypoint[time] for time in sorted(time_to_waypoint.keys())]

    def coverage_percentages(self):
        total = max(self.__counts.values())
        for name, count in self.__counts.items():
            yield name, 100 * count / total


def make_waypoint(names, extra=None):
    names = list(names)
    if extra:
        names += [extra]
    names = ['time'] + names
    defaults = [None] * len(names)
    return namedtuple('Waypoint', names, defaults=defaults)