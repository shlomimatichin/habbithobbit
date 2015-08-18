import simplejson
from habbithobbit import workevery
import time
import logging


class Recorder(workevery.WorkEvery):
    WORK_INTERVAL = 10

    def __init__(self, output):
        self._output = output
        self._data = []
        workevery.WorkEvery.__init__(self)

    def record(self, event):
        event['time'] = time.time()
        self._data.append(event)

    def work(self):
        data = self._threadSafePopData()
        if len(data) == 0:
            return
        with open(self._output, "a") as f:
            f.write(simplejson.dumps(data))
            f.write("\n")

    def _threadSafePopData(self):
        data = []
        while len(self._data) > 0:
            data.append(self._data.pop(0))
        return data
