import os
import random

from mk2.plugins import Plugin
from mk2.events import Hook, StatPlayerCount


class Alert(Plugin):
    interval = Plugin.Property(default=200)
    command  = Plugin.Property(default="say {message}")
    path     = Plugin.Property(default="alerts.txt")
    min_pcount = Plugin.Property(default=0)
    
    messages = []
    
    def setup(self):
        self.register(self.count_check, StatPlayerCount)
        if self.path and os.path.exists(self.path):
            f = open(self.path, 'r')
            for l in f:
                l = l.strip()
                if l:
                    self.messages.append(l)
            f.close()

    def count_check(self, event):
        self.requirements_met = event.players_current >= self.min_pcount

    def server_started(self, event):
        if self.messages:
            self.repeating_task(self.repeater, self.interval)

    def repeater(self, event):
        if self.requirements_met:
            self.send_format(self.command, message=random.choice(self.messages))

