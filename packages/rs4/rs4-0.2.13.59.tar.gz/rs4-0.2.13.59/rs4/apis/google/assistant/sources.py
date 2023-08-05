import os
import collections
import threading
from .grpc import audio_helpers
import sounddevice as sd

class SoundDeviceInputStream (audio_helpers.SoundDeviceStream):
    def __init__(self, sample_rate, sample_width, block_size, flush_size, device = None):
        if sample_width == 2:
            audio_format = 'int16'
        else:
            raise Exception('unsupported sample width:', sample_width)
        self._audio_stream = sd.RawInputStream(
            samplerate=sample_rate, dtype=audio_format, channels=1, device = device,
            blocksize=int(block_size/2)  # blocksize is in number of frames.
        )
        self._sample_width = sample_width
        self._block_size = block_size
        self._flush_size = flush_size
        self._sample_rate = sample_rate


class VirtualDeviceInputStream:
    def __init__ (self, smaple_rate = 16000, sample_width = 2, block_size = 6400):
        self._sample_rate = smaple_rate
        self._sample_width = sample_width
        self._block_size = block_size

        self._lock = threading.Condition ()
        self._stopped = True
        self._streams = collections.deque ()

    def put (self, stream):
        with self._lock:
            self._streams.append (stream)
            self._lock.notify ()

    def read (self, size, *args, **kargs):
        with self._lock:
            if self._stopped:
                raise IOError ('closed input stream')
            while not self._stopped and (not self._streams or sum ([len (s) for s in self._streams]) < size):
                self._lock.wait ()
            if self._stopped:
                return b''
            data = b''
            while 1:
                first = self._streams.popleft ()
                if len (data) + len (first) < size:
                    data += first
                else:
                    wanted = size - len (data)
                    data += first [:wanted]
                    self._streams.appendleft (first [wanted:])
                    break
            assert len (data) == size
        return data

    def flush (self):
        pass

    def start (self):
        with self._lock:
            self._streams.clear ()
            self._stopped = False
            self._lock.notify ()

    def stop (self):
        with self._lock:
            self._stopped = True
            self._lock.notify ()

    def close (self):
        self.stop ()

