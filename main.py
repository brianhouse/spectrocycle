#!venv/bin/python

import sys
import time
import math
from util import *

CYCLE_DURATION = 1  # seconds
MAX_CYCLES = 2
CHOP = -250
THRESHOLD = None

if len(sys.argv) < 2:
    print("[path]")
    exit()

filename = sys.argv[1]
sound = Sound(filename)

samp_per_cycle = int(CYCLE_DURATION * sound.rate)
print("samp_per_cycle", samp_per_cycle)
cycles = [np.array(sound.signal[i:i + samp_per_cycle]) for i in range(0, len(sound.signal), samp_per_cycle)]
cycles = cycles[:MAX_CYCLES]
print("cycles", len(cycles))

width, height = 1080 * 4, 1080 * 4
# width, height = len(freqs) * 8, len(freqs) * 8
surface, ctx = drawing(width, height)

ring_size = (width - 50) / (2 * len(cycles))
color = random.choice(colors)
color = colors[0]

for c, cycle in enumerate(cycles):

    log.info(f"Cycle {c}")
    log.info("Computing spectrogram...")

    spectrum, freqs, ts, image = plt.specgram(cycle, NFFT=512, Fs=sound.rate, noverlap=512 // 2, mode="psd", scale="dB")
    spectrum = np.log10(spectrum)
    spectrum = normalize(spectrum)

    log.info(f"--> freq bins {len(freqs)}")
    log.info(f"--> time columns {len(ts)}")

    log.info("Drawing...")

    if CHOP is not None:
        freqs = freqs[:CHOP]  # chop off the top

    max_v = 0
    for freq_n in range(len(freqs)):
        for t_n in range(len(ts)):
            v = spectrum[freq_n][t_n]
            r = 1.0 - (freq_n / len(freqs))
            r *= ring_size
            r += ring_size * c
            a1 = (t_n / len(ts)) * 360
            a2 = a1 + (360 / len(ts))
            if THRESHOLD is not None:
                color[3] = 1 if v > THRESHOLD else 0
            else:
                color[3] = v
            ctx.set_source_rgba(*color)
            ctx.set_line_width(10.0)
            ctx.arc(width / 2, height / 2, r, math.radians(a1), math.radians(a2))
            ctx.stroke()

log.info("--> done")

output(surface)
