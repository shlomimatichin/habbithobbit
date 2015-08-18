import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from habbithobbit import recorder
from habbithobbit import recordwindow
#from habbithobbit import recorddesktopnotifications
import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument("--output", default="/tmp/recording")
args = parser.parse_args()

recorderInstance = recorder.Recorder(args.output)
recordWindow = recordwindow.RecordWindow(recorderInstance)
#recordDesktopNotifications = recorddesktopnotifications.RecordDesktopNotifications(recorderInstance)

time.sleep(100000)
