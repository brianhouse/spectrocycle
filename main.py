#!venv/bin/python

import sys
import time
import math
from util import *

CYCLE_DURATION = 60  # seconds
MAX_CYCLES = 1
WINDOW_SIZE = 512
CHOP = 140  # 257
THRESHOLD = None
OVERLAP = .1

if len(sys.argv) < 2:
    print("[path]")
    exit()

filename = sys.argv[1]
sound = Sound(filename)

samp_per_cycle = int(CYCLE_DURATION * sound.rate)
cycles = [np.array(sound.signal[i:i + samp_per_cycle]) for i in range(0, len(sound.signal), samp_per_cycle)]
cycles = cycles[:MAX_CYCLES]
log.info(f"Cycle duration: {CYCLE_DURATION}")
log.info(f"Total cycles ({MAX_CYCLES} max): {len(cycles)}")

width, height = 3600 * 2, 3600 * 2  # 12"x12" @ 600 dpi
surface, ctx = drawing(width, height)

ring_width = (width - 50) / (2 * len(cycles))

for c, cycle in enumerate(cycles):

    log.info(f"## Cycle {c}")
    log.info("Computing spectrogram...")

    spectrum, freqs, ts, image = plt.specgram(cycle, NFFT=WINDOW_SIZE, Fs=sound.rate, noverlap=WINDOW_SIZE // 2, mode="magnitude", scale="dB")
    spectrum = np.log10(spectrum)
    spectrum = normalize(spectrum, -10, 3)
    spectrum **= 3

    if CHOP is not None:
        freqs = freqs[:-CHOP]  # chop off the top
    # for freq in freqs:
    #     print(freq, int(freq / 60))

    log.info(f"--> freq bins {len(freqs)}")
    log.info(f"--> time columns {len(ts)}")

    log.info("Drawing...")

    line_width = ring_width / len(freqs)

    max_v = 0
    for freq_n in range(len(freqs)):
        for t_n in range(len(ts)):
            v = spectrum[freq_n][t_n]
            r = 1.0 - (freq_n / len(freqs))   # position within current ring (linear)
            r *= ring_width                   # pixel within current ring
            r += ring_width * c               # multiply by current cycle
            a1 = (t_n / len(ts)) * 360        # start angle
            a2 = a1 + (360 / len(ts))         # stop angle
            if THRESHOLD is not None:
                v = 1 if v > THRESHOLD else 0
            else:
                v = 1. - v
            ctx.set_source_rgba(v, v, v, 1.)
            ctx.set_line_width(line_width)
            ctx.arc(width / 2, height / 2, r, math.radians(a1), math.radians(a2 + OVERLAP))
            ctx.stroke()

    log.info("--> cycle complete")

log.info("--> done")

output(surface)

