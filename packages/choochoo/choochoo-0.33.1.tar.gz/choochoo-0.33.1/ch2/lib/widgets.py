
import datetime as dt
from abc import abstractmethod
from logging import getLogger

from sqlalchemy import desc
from urwid import ExitMainLoop

from ..sql.tables.activity import ActivityJournal
from .date import DAY, WEEK, MONTH, YEAR, to_time, to_date, add_date, local_date_to_time, time_to_local_date
from ..urwid.tui.tabs import TabNode

log = getLogger(__name__)


class App(TabNode):
    '''
    An urwid mainloop, database session and tabs.
    '''

    def __init__(self, db):
        self.__db = db
        self.__session = None
        super().__init__(*self._build(self.__new_session()))

    def __new_session(self):
        if self.__session:
            self.save()
            self.__session.close()
        self.__session = self.__db.session(autoflush=False)
        return self.__session

    @property
    def _session(self):
        return self.__session

    def keypress(self, size, key):
        if key == 'meta q':
            self.save()
            raise ExitMainLoop()
        elif key == 'meta x':
            self.abort()
            raise ExitMainLoop()
        elif key == 'meta s':
            self.save()
        else:
            return super().keypress(size, key)

    def abort(self):
        if self.__session:
            self.__session.rollback()

    def save(self):
        if self.__session:
            self.__session.commit()

    @abstractmethod
    def _build(self, session):
        pass

    def rebuild(self):
        widget, tabs = self._build(self.__new_session())
        self._w = widget
        try:
            self.replace(tabs)
        except Exception as e:
            log.warning('Could not replace tabs: %s' % e)


class DateSwitcher(App):
    '''
    Extend App with shortcuts for changing date and rebuilding.
    '''

    def __init__(self, db, date):
        self.__date = date
        super().__init__(db)

    def keypress(self, size, key):
        if key.startswith('meta'):
            c = key[-1]
            if c.lower() in (DAY, WEEK, MONTH, YEAR, 't'):
                self._next_prev_date(c)
                return
            if c.lower() == 'a':
                self._next_prev_activity(c)
                return
        return super().keypress(size, key)

    def _next_prev_activity(self, c):
        s = self._session
        if c == 'a':
            journal = ActivityJournal.before_local_time(s, self._date)
        else:
            journal = ActivityJournal.after_local_time(s, self._date)
        if journal:
            self._change_date(time_to_local_date(journal.start))

    def _next_prev_date(self, c):
        if c.lower() == 't':
            date = dt.date.today()
        else:
            delta = (-1 if c == c.lower() else 1, c.lower())
            date = add_date(self.__date, delta)
        self._change_date(date)

    def _change_date(self, date):
        self.__date = self._refine_new_date(date)
        self.rebuild()

    def _refine_new_date(self, date):
        '''
        Hook for subclasses
        '''
        return date

    @property
    def _date(self):
        return self.__date
