#!/usr/bin/env python3

import time
import math
import subprocess
import cairo
from util import *

filename = "200424_mono_.wav"
# filename = "robin_chat_sample_11k_16_mono.wav"
sound = Sound(filename)

# sound.plot()
# exit()

log.info("Computing spectrogram...")

block_size = 512
block_overlap = block_size / 2 # power of two, default is 128

spectrum, freqs, ts, image = plt.specgram(sound.signal, NFFT=block_size, Fs=sound.rate, noverlap=block_overlap)

log.info(f"--> freq bins {len(freqs)}")
log.info(f"--> time columns {len(ts)}")

log.info("Drawing...")

freqs = freqs[:-90] # chop off the top

width, height = 1080, 1080
width, height = len(freqs) * 8, len(freqs) * 8
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
ctx.rectangle(0, 0, width, height)
ctx.set_source_rgba(255, 255, 255, 255)
ctx.fill()
ctx.stroke()

THRESHOLD = .5
for freq_n in range(len(freqs)):
    for t_n in range(len(ts)):

        v = spectrum[freq_n][t_n]
        v = 0 if v > THRESHOLD else 255
        r = 1.0 - (freq_n / len(freqs))
        # r = freq_n / len(freqs)
        r *= ((width-50)/2) - 1
        r += 1
        a1 = (t_n / len(ts)) * 360
        a2 = a1 + (360 / len(ts))
        # ctx.line((x * pixel_width) / ctx.width, (y * pixel_height) / ctx.height, ((x * pixel_width) + pixel_width) / ctx.width, (y * pixel_height) / ctx.height, stroke=(v, v, v, 1.), thickness=pixel_height)
        # ctx.arc(.5, .5, r, r, d, d+1, stroke=(0.0, 0.0, 0.0, .1), thickness=5.0)
        ctx.set_source_rgba(v, v, v, 255)
        ctx.arc(width/2, height/2, r, math.radians(a1), math.radians(a2))
        ctx.stroke()


log.info("--> done")
ctx.stroke()
filename = f"charts/{int(time.time())}.png"
surface.write_to_png(filename)
subprocess.call(["open", filename])
