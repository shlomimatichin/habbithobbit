from habbithobbit import linesubprocess
import dbus


class RecordKeyboardActivity:
    def __init__(self, recorder):
        self._recorder = recorder
        self._last = False
        self._detector = linesubprocess.LineSubprocess(
            ["python", "-m", "habbithobbit.keyboarddetector"],
            self._onLine)

    def _onLine(self, line):
        now = 'True' in line
        if now != self._last:
            event = dict(type="keyboard", active=now)
            self._recorder.record(event)
            self._last = now
