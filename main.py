#!/usr/bin/env python3

import time
import math
from util import *

CYCLE = 2.0 #* 6
CYCLES = 10
CHOP = True
THRESHOLD = .125

# filename = "200424_mono_.wav"
# filename = "robin_chat_sample_11k_16_mono.wav"
# filename = "200502_mono.wav"
filename = "200519_mono.wav"
# filename = "urgency.wav"
sound = Sound(filename)
# sound.plot()
# exit()

n = int(CYCLE * sound.rate)
cycles = [np.array(sound.signal[i:i + n]) for i in range(0, len(sound.signal), n)]

cycles = cycles[:CYCLES]

width, height = 1080*4, 1080*4
# width, height = len(freqs) * 8, len(freqs) * 8
surface, ctx = drawing(width, height)

ring_size = (width - 50) / (2 * len(cycles))
color = random.choice(colors)

for c, cycle in enumerate(cycles):

    log.info(f"Cycle {c}")
    log.info("Computing spectrogram...")

    spectrum, freqs, ts, image = plt.specgram(cycle, NFFT=512, Fs=sound.rate, noverlap=512/2)

    log.info(f"--> freq bins {len(freqs)}")
    log.info(f"--> time columns {len(ts)}")

    log.info("Drawing...")

    if CHOP:
        freqs = freqs[:-90] # chop off the top

    for freq_n in range(len(freqs)):
        for t_n in range(len(ts)):
            v = spectrum[freq_n][t_n]
            v = 0 if v > THRESHOLD else 255
            r = 1.0 - (freq_n / len(freqs))
            r *= ring_size
            r += ring_size * c
            a1 = (t_n / len(ts)) * 360
            a2 = a1 + (360 / len(ts))
            color[3] = 255-(v*255)
            ctx.set_source_rgba(*color)
            ctx.arc(width/2, height/2, r, math.radians(a1), math.radians(a2))
            ctx.stroke()

log.info("--> done")

output(surface)
