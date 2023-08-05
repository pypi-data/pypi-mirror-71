from precise import network_runner
import time
import numpy as np

class IntermittentListener (network_runner.Listener):
    def __init__(self, model_name, chunk_size = -1, runner_cls = None):
        network_runner.Listener.__init__ (self, model_name, chunk_size, runner_cls)
        self.last_updated = time.time ()

    def update(self, stream):
        if time.time () - self.last_updated > 2.0:
            self.mfccs = np.zeros((self.pr.n_features, self.pr.n_mfcc))
        self.last_updated = time.time ()
        mfccs = self.update_vectors(stream)
        raw_output = self.runner.run(mfccs)
        return self.threshold_decoder.decode(raw_output)
