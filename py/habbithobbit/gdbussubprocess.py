import subprocess
import threading
import logging
import atexit


class GdbusSubprocess(threading.Thread):
    def __init__(self, cmdline, callback):
        self._cmdline = cmdline
        self._callback = callback
        self._popen = subprocess.Popen(["gdbus"] + cmdline, stdout=subprocess.PIPE)
        atexit.register(self.stop)
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def stop(self):
        if self._popen is None:
            return
        self._popen.stdout.close()
        self._popen.terminate()
        self._popen = None

    def run(self):
        try:
            while True:
                line = self._popen.stdout.readline()
                if line == "":
                    if self._popen is None:
                        return
                    raise Exception("gdbus subprocess terminated")
                self._callback(line.strip())
        except:
            logging.exception("GdbusSubprocess terminates: %(cmdline)s", dict(cmdline=self._cmdline))
