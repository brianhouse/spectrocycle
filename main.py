#!/usr/bin/env python3

import time
import math
from util import *

CYCLE = 2.0 #* 6

filename = "200424_mono_.wav"
# filename = "robin_chat_sample_11k_16_mono.wav"
filename = "200502_mono.wav"
# filename = "urgency.wav"
sound = Sound(filename)
# sound.plot()
# exit()

n = int(CYCLE * sound.rate)
cycles = [np.array(sound.signal[i:i + n]) for i in range(0, len(sound.signal), n)]

cycles = cycles[:10]

width, height = 1080*4, 1080*4
# width, height = len(freqs) * 8, len(freqs) * 8
surface, ctx = drawing(width, height)

ring_size = (width - 50) / (2 * len(cycles))
print("ring_size", ring_size)

for c, cycle in enumerate(cycles):

    log.info(f"Cycle {c}")
    log.info("Computing spectrogram...")

    spectrum, freqs, ts, image = plt.specgram(cycle, NFFT=512, Fs=sound.rate, noverlap=512/2)

    log.info(f"--> freq bins {len(freqs)}")
    log.info(f"--> time columns {len(ts)}")

    log.info("Drawing...")

    freqs = freqs[:-90] # chop off the top

    THRESHOLD = .5
    for freq_n in range(len(freqs)):
        for t_n in range(len(ts)):
            v = spectrum[freq_n][t_n]
            v = 0 if v > THRESHOLD else 255
            r = 1.0 - (freq_n / len(freqs))
            r *= ring_size
            r += ring_size * c
            a1 = (t_n / len(ts)) * 360
            a2 = a1 + (360 / len(ts))
            ctx.set_source_rgba(v, v, v, 255-(v*255))
            ctx.arc(width/2, height/2, r, math.radians(a1), math.radians(a2))
            ctx.stroke()

log.info("--> done")

output(surface)
