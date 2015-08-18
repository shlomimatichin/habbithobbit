from habbithobbit import workevery
from habbithobbit import xprop
import logging


class RecordWindow(workevery.WorkEvery):
    WORK_INTERVAL = 1

    def __init__(self, recoder):
        self._recorder = recoder
        self._lastActiveWindowID = None
        self._lastActiveWindowName = None
        workevery.WorkEvery.__init__(self)

    def work(self):
        window = xprop.Window.active()
        if self._sameAsLastIteration(window):
            return
        event = dict(
            type='window',
            windowName=window.name(),
            executable=window.executable())
        self._recorder.record(event)

    def _sameAsLastIteration(self, window):
        if self._lastActiveWindowID is not None and window.id() == self._lastActiveWindowID and \
                self._lastActiveWindowName is not None and window.name() == self._lastActiveWindowName:
            return True
        self._lastActiveWindowID = window.id()
        self._lastActiveWindowName = window.name()
        return False
