

import sys
import time

if sys.platform == "win32":
    # on Windows, the best timer is time.clock()
    try:
        timerfunc = time.clock
    except Exception as e:
        print(f"Failed to use time.clock, even though using windows: {str(e)}")
        timerfunc = time.time
else:
    # on most other platforms, the best timer is time.time()
    timerfunc = time.time


class Clock(object):
    def __init__(self):
        self.lasttime = timerfunc()
        self.curtime = timerfunc()
        self.frametime = 0

    def tick(self):
        self.lasttime = self.curtime
        self.curtime = timerfunc()
        dt = self.curtime - self.lasttime

        self.frametime = 0.99 * self.frametime + 0.01 * dt

        return dt

    def getfps(self):
        if self.frametime == 0:
            return 0
        return 1 / self.frametime
