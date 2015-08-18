from habbithobbit import linesubprocess
import dbus


class RecordMouseActivity:
    def __init__(self, recorder):
        self._recorder = recorder
        self._last = False
        self._detector = linesubprocess.LineSubprocess(
            ["python", "-m", "habbithobbit.mousemovementdetector"],
            self._onLine)

    def _onLine(self, line):
        now = 'Movement detected' in line
        if now != self._last:
            event = dict(type="mouse activity", active=now)
            self._recorder.record(event)
            self._last = now
