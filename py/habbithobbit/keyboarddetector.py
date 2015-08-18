from Xlib import X, XK
import Xlib.display
from Xlib.ext import record
from Xlib.protocol import rq
import sys
import threading
import time

display = Xlib.display.Display()
keyboardActivity = False


class PrintThread(threading.Thread):
    def run(self):
        global keyboardActivity
        while True:
            print keyboardActivity
            keyboardActivity = False
            sys.stdout.flush()
            time.sleep(1)


printThread = PrintThread()
printThread.daemon = True
printThread.start()


def callback(reply):
    global keyboardActivity
    keyboardActivity = True


if not display.has_extension("RECORD"):
    raise Exception("No RECORD extension")

context = display.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.KeyPress),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])

display.record_enable_context(context, callback)
display.record_free_context(context)
