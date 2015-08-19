from habbithobbit.analyze import downloadpackages
from habbithobbit.analyze import networking
import logging
import subprocess
import threading
import shutil
import os
import signal
import glob
import atexit


class KibanaDaemon(threading.Thread):
    _DIR = "kibana"

    @classmethod
    def clear(cls):
        shutil.rmtree(cls._DIR, ignore_errors=True)

    def __init__(self):
        self._unpack()
        self._popen = subprocess.Popen("bin/kibana", cwd=self._unpackedDir())
        atexit.register(self.stop)
        networking.waitForTCPServer(("localhost", 5601), timeout=10)
        logging.info("Kibana daemon up and running")
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def stop(self):
        if self._popen is None:
            return
        popen = self._popen
        self._popen = None
        popen.terminate()
        popen.wait()

    def run(self):
        try:
            self._popen.wait()
            if self._popen is None:
                return
            logging.error("Kibana daemon stopped, committing suicide")
            os.kill(os.getpid(), signal.SIGKILL)
        except:
            logging.exception("kibana daemon monitor raised")

    def _unpackedDir(self):
        result = glob.glob(os.path.join(self._DIR, "*", "bin", "kibana"))
        if len(result) == 0:
            return None
        return os.path.dirname(os.path.dirname(result[0]))

    def _unpack(self):
        if self._unpackedDir() is not None:
            return self._unpackedDir()
        packed = downloadpackages.DownloadPackages().downloadKibana()
        if not os.path.isdir(self._DIR):
            os.makedirs(self._DIR)
        subprocess.check_call(["tar", "xf", packed, "-C", self._DIR])
        assert self._unpackedDir() is not None
