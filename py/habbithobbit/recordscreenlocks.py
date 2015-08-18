from habbithobbit import gdbussubprocess
import dbus


class RecordScreenLocks:
    def __init__(self, recorder):
        self._recorder = recorder
        self._gdbusSubprocess = gdbussubprocess.GdbusSubprocess(
            ["monitor", "-e", "-d", "com.canonical.Unity", "-o", "/com/canonical/Unity/Session"],
            self._onLine)

    def _onLine(self, line):
        if 'com.canonical.Unity.Session.Locked' in line:
            event = dict(type="screen lock", locked=True)
            self._recorder.record(event)
        elif 'com.canonical.Unity.Session.Unlocked' in line:
            event = dict(type="screen lock", locked=False)
            self._recorder.record(event)
