from habbithobbit import run
import re
import psutil


class Window:
    def __init__(self, id):
        self._id = id
        self._cachedPid = None

    @classmethod
    def active(cls):
        output = run.run(["xprop", "-root", "32x", r'\t$0', "_NET_ACTIVE_WINDOW"])
        return cls(output.strip().split('\t')[1])

    def id(self):
        return self._id

    def name(self):
        output = run.run(["xprop", "-id", self._id, "_NET_WM_NAME"])
        return re.search(r'"(.*)"', output).group(1)

    def pid(self):
        if self._cachedPid is None:
            output = run.run(["xprop", "-id", self._id, "32c", r'\t$0', "_NET_WM_PID"])
            self._cachedPid = int(output.strip().split('\t')[1])
        return self._cachedPid

    def executable(self):
        process = psutil.Process(self.pid())
        return process.exe()
