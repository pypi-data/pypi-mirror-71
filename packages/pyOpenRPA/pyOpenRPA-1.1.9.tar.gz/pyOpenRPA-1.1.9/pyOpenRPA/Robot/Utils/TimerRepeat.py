from threading import Timer
import datetime
# lTimer = RepeatedTimer(3, def, [], {}) # it auto-starts, no need of rt.start()
# if def return None = timer stops
# lTimer.start()
class TimerRepeat(object):
    def __init__(self, interval, function, args, kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    def _run(self):
        self.is_running = False
        lResult = self.function(*self.args, **self.kwargs)
        if lResult is not None:
            if lResult:
                self.start()
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True
    def stop(self):
        self._timer.cancel()
        self.is_running = False