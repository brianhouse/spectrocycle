import time
import wave
import cairo
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from .log_config import log, config


class Sound(object):

    def __init__(self, path):
        log.info("Loading sound from %s..." % path)
        self.path = path
        self.wf = wave.open(self.path, 'rb')
        self.bits = self.wf.getsampwidth() * 8
        if self.bits != 16:
            raise NotImplementedError
        self.signal = np.fromstring(self.wf.readframes(-1), 'Int16') # signed 16-bit samples
        self.wf.rewind()
        self.rate = self.wf.getframerate()
        self.samples = len(self.signal)
        self.duration = self.samples / self.rate
        log.info(f"--> bits {self.bits}")
        log.info(f"--> rate {self.rate}")
        log.info(f"--> samples {self.samples}")
        log.info(f"--> duration {self.duration:.2f}s")


    def plot(self):

        # 50-5000 hz
        # need a window @ 25 hz, 0.04 seconds
        # 0.04 / (1 / sampling_rate)
        # at 11025, that's 441
        # so at that sampling_rate and higher, 512 is good
        block_size = 512

        # set up plot
        plt.rcParams['toolbar'] = 'None'
        plt.figure(frameon=True, figsize=(15, 8), dpi=80, facecolor=(1., 1., 1.), edgecolor=(1., 1., 1.))

        # show amplitude domain
        plt.subplot(2, 1, 1)
        plt.plot(self.signal, color=(1., 0., 0.))
        plt.axis([0.0, self.duration * self.rate, 0-(2**self.bits/2), 2**self.bits/2]) # go to bitrate

        # show spectrogram
        plt.subplot(2, 1, 2)
        block_overlap = block_size / 2 # power of two, default is 128
        spectrum, freqs, ts, image = plt.specgram(self.signal, NFFT=block_size, Fs=self.rate, noverlap=block_overlap)
        plt.axis([0.0, self.duration, 0, self.rate/2])

        fig = plt.gcf()
        fig.canvas.set_window_title(self.path)

        log.info("--> freq bins %s" % len(freqs))
        log.info("--> time columns %s" % len(ts))

        plt.show()


def normalize(signal, minimum=None, maximum=None):
    signal = np.array(signal).astype('float')
    if minimum is None:
        minimum = np.min(signal)
    if maximum is None:
        maximum = np.max(signal)
    signal -= minimum
    maximum -= minimum
    signal /= maximum
    signal = np.clip(signal, 0.0, 1.0)
    return signal


def resample(ts, values, n_samples):
    assert np.all(np.diff(ts) >= 0)
    ts = normalize(ts)
    return np.interp(np.linspace(0.0, 1.0, n_samples), ts, values)


def drawing(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.rectangle(0, 0, width, height)
    ctx.set_source_rgba(255, 255, 255, 255)
    ctx.fill()
    ctx.stroke()
    return surface, ctx

def output(surface):
    filename = f"charts/{int(time.time())}.png"
    surface.write_to_png(filename)
    subprocess.call(["open", filename])
