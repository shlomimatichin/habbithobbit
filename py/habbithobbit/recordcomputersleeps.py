from habbithobbit import workevery
import time
import logging


class RecordComputerSleeps(workevery.WorkEvery):
    WORK_INTERVAL = 1
    _INTERVAL_BETWEEN_WORKS_TO_TRIGGER = 2.5

    def __init__(self, recoder):
        self._recorder = recoder
        self._lastTime = time.time()
        workevery.WorkEvery.__init__(self)

    def work(self):
        now = time.time()
        slept = now - self._lastTime > self._INTERVAL_BETWEEN_WORKS_TO_TRIGGER
        if slept:
            event = dict(type="sleep",
                         start=self._lastTime,
                         end=now)
            self._recorder.record(event)
        self._lastTime = now
