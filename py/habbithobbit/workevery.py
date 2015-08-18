import threading
import logging


class WorkEvery(threading.Thread):
    WORK_INTERVAL = 1

    def __init__(self):
        self.__stop = threading.Event()
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def stop(self):
        self.__stop.set()

    def run(self):
        try:
            while not self.__stop.isSet():
                self.work()
                self.__stop.wait(self.WORK_INTERVAL)
        except:
            logging.exception("%(klass)s thread terminates", dict(klass=self.__class__.__name__))
