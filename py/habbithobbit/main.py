import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from habbithobbit import recorder
from habbithobbit import recordwindow
from habbithobbit import recordcomputersleeps
from habbithobbit import recordscreenlocks
from habbithobbit import recordmouseactivity
from habbithobbit import recordkeyboardactivity
#from habbithobbit import recorddesktopnotifications
import argparse
import time
import signal
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--output", default="/tmp/recording")
args = parser.parse_args()

recorderInstance = recorder.Recorder(args.output)
recordWindow = recordwindow.RecordWindow(recorderInstance)
recordComputerSleeps = recordcomputersleeps.RecordComputerSleeps(recorderInstance)
recordScreenLocks = recordscreenlocks.RecordScreenLocks(recorderInstance)
recordMouseActivity = recordmouseactivity.RecordMouseActivity(recorderInstance)
recordKeyboardActivity = recordkeyboardactivity.RecordKeyboardActivity(recorderInstance)
#recordDesktopNotifications = recorddesktopnotifications.RecordDesktopNotifications(recorderInstance)

def exitHandler():
    sys.exit()
signal.signal(signal.SIGTERM, exitHandler)
signal.signal(signal.SIGINT, exitHandler)

time.sleep(1000000)
