import threading
import time
import random
from json import dumps


class Sensor():
    def __init__(self, name, read_rate, on_read, read):
        self.name = name
        self.read_rate = read_rate
        self.on_read = on_read
        self._thread = None
        self._stop_loop = False

    def _read(self):
        return random.randint(1, 10)

    def read_loop_start(self):
        if self._thread is not None:
            raise Exception(
                'Thread is already running and cannot be started again')
        self._stop_loop = False
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def read_loop_stop(self):
        if self._thread is None:
            raise Exception(
                'Thread is not currently running and cannot be stopped')
        self._stop_loop = True
        if threading.currentThread != self._thread:
            self._thread.join()
            self._thread = None

    def _read_loop(self):
        while not self._stop_loop:
            value = self._read()
            payload = dumps({"value": value,
                             "timestamp": time.time(),
                             "name": self.name})
            self.on_read(self.name, payload)
            time.sleep(self.read_rate)


def water_sensor(name, read_rate, on_read):
    def read_water_value(): return random.randint(1, 10)
    sensor = Sensor(name, read_rate, on_read, read_water_value)
    return sensor
