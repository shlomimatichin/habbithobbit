import Xlib.display
import time
import sys


display = Xlib.display.Display()
last = None
while True:
    data = display.screen().root.query_pointer()._data
    now = (data['root_x'], data['root_y'])
    if last is not None and now != last:
        print "Movement detected"
    else:
        print "No movement"
    sys.stdout.flush()
    last = now
    time.sleep(1)
