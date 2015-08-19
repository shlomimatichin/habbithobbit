import threading
from habbithobbit import xprop
import logging
import glib
import dbus
from dbus.mainloop.glib import DBusGMainLoop


class RecordDesktopNotifications(threading.Thread):
    def __init__(self, recoder):
        self._recorder = recoder
        self._loop = DBusGMainLoop(set_as_default=True)
        self._sessionBus = dbus.SessionBus()
        self._sessionBus.add_match_string(
            "type='method_call',interface='org.freedesktop.Notifications',member='Notify',eavesdrop=true")
        self._sessionBus.add_message_filter(self._onMessage)
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def run(self):
        glib.MainLoop().run()

    def _onMessage(self, bus, message):
        keys = ["app_name", "replaces_id", "app_icon", "summary",
                "body", "actions", "hints", "expire_timeout"]
        args = message.get_args_list()
        if len(args) == len(keys):
            notification = dict([(keys[i], args[i]) for i in range(len(keys))])
        event = dict(type="desktop notification", notification=notification)
        self._recorder.record(event)
