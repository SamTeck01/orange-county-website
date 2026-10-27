# "Golden Hour" - original modern cinematic track: atmospheric intro, punchy drop, sidechained supersaws,
# 808 sub, plucks, whooshes on every transition, impacts on the drop and the end card. 44.1 kHz stereo.
import numpy as np, sys, wave
from scipy.signal import lfilter, butter
SR = 44100; DUR = float(sys.argv[1]); CUTS = [float(x) for x in sys.argv[2].split(",")]
BPM = 110; B = 60 / BPM; BAR = 4 * B
N = int(SR * DUR); t = np.arange(N) / SR; L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(7)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def filt(x, f, kind='low'):
    b, a = butter(2, min(0.99, f / (SR / 2)), kind); return lfilter(b, a, x)
def add(sig, start, pan=0.0, g=1.0):
    s0 = int(start * SR)
    if s0 >= N: return
    s1 = min(N, s0 + len(sig)); sig = sig[:s1 - s0] * g
    L[s0:s1] += sig * (1 - pan); R[s0:s1] += sig * (1 + pan)
def saw(f, n, det=(-0.15, -0.07, 0, 0.07, 0.15)):
    tt = np.arange(n) / SR; return sum((2 * ((tt * f * 2 ** (d / 12) + rng.random()) % 1) - 1) for d in det) / len(det)
DROP = CUTS[0]                                   # the beat lands as the first shot ends
END = DUR - 4.0
# Bm - G - D - A   (one bar each)
PROG = [(47, [59, 62, 66]), (43, [59, 62, 67]), (50, [57, 62, 66]), (45, [57, 61, 64])]
# --- pads / supersaw chords
bar = 0; tm = 0.0
while tm < DUR:
    root, ch = PROG[bar % 4]; n = int((BAR + 0.6) * SR)
    sig = sum(saw(hz(m), n) for m in ch + [ch[0] - 12])
    env = np.minimum(1, np.arange(n) / (0.25 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.6 * SR))
    full = tm >= DROP - 0.01 and tm < END
    cut = 5500 if full else 700 + 1800 * min(1, tm / max(DROP, 1))
    sig = filt(sig * env, cut) * (0.22 if full else 0.16)
    if full:   # sidechain pump on every beat
        ph = (np.arange(n) / SR) % B; sig *= 0.25 + 0.75 * np.minimum(1, ph / (0.42 * B))
    add(sig, tm, -0.3); add(np.roll(sig, 900), tm, 0.3)
    # 808 sub with a short glide in
    if full:
        tt = np.arange(int(BAR * SR)) / SR; f = hz(root - 12) * (1 + 0.5 * np.exp(-tt * 40))
        sub = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt * 0.6) * 0.32
        add(sub, tm)
    # pluck arpeggio (16ths after the drop, 8ths before)
    step = B / 4 if full else B / 2; notes = [ch[0] + 12, ch[2] + 12, ch[1] + 12, ch[2] + 24]
    for i in range(int(BAR / step)):
        st = tm + i * step; nn = int(0.35 * SR); tt = np.arange(nn) / SR
        p = filt(saw(hz(notes[i % 4]), nn, (0, 0.08)), 4200) * np.exp(-tt * 14) * 0.13
        add(p, st, 0.45 if i % 2 else -0.45)
    bar += 1; tm += BAR
# --- drums (drop -> end)
def kick():
    tt = np.arange(int(0.45 * SR)) / SR; return np.tanh(3 * np.sin(2 * np.pi * np.cumsum(48 + 140 * np.exp(-tt * 35)) / SR) * np.exp(-tt * 7)) * 0.75
def clap():
    n = int(0.25 * SR); tt = np.arange(n) / SR; x = filt(rng.normal(0, 1, n), 1200, 'high')
    e = sum(np.exp(-np.maximum(0, tt - d) * 40) * (tt >= d) for d in (0, 0.012, 0.024)); return x * e * 0.28
def hat(o=False):
    n = int((0.18 if o else 0.05) * SR); tt = np.arange(n) / SR; return filt(rng.normal(0, 1, n), 7000, 'high') * np.exp(-tt * (18 if o else 70)) * 0.12
b = DROP; k = 0
while b < END - 0.05:
    add(kick(), b)
    if k % 2 == 1: add(clap(), b, 0.05)
    add(hat(), b + B / 2, 0.3); add(hat(), b + B / 4, -0.3, 0.6); add(hat(), b + 3 * B / 4, -0.3, 0.6)
    if k % 8 == 7: add(hat(True), b + B / 2, 0.3)
    b += B; k += 1
# --- whoosh into every cut, impact on drop and end card
def whoosh(d=1.1):
    n = int(d * SR); tt = np.arange(n) / SR; x = rng.normal(0, 1, n); y = np.zeros(n)
    for i in range(0, n, 2048):   # sweeping band
        f = 300 + 5000 * (i / n) ** 2; seg = filt(x[max(0, i - 400):i + 2048], f + 400)[-min(2048, n - i):]; y[i:i + len(seg)] = seg
    return y * np.sin(np.pi * tt / d) ** 2 * 0.35
def impact():
    n = int(2.5 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(30 + 60 * np.exp(-tt * 8)) / SR) * np.exp(-tt * 1.6)
    return (np.tanh(2 * boom) * 0.8 + filt(rng.normal(0, 1, n), 900) * np.exp(-tt * 3) * 0.3)
for c in CUTS:
    w = whoosh(); add(w, c - 0.8, -0.4, 0.8); add(w[::-1] * 0.5, c - 0.8, 0.4, 0.8)
add(impact(), DROP); add(impact(), END - 0.2, 0, 0.9)
# riser into the drop
n = int(min(DROP, 4.0) * SR); tt = np.arange(n) / SR
add(filt(rng.normal(0, 1, n), 2500) * (tt / tt[-1]) ** 3 * 0.35, DROP - n / SR)
# --- space + master
def verb(x):
    y = x.copy()
    for d, g in ((0.029, .3), (0.043, .27), (0.067, .23), (0.097, .2), (0.141, .16), (0.211, .12)):
        s = int(d * SR); y[s:] += x[:-s] * g
    return y
L, R = verb(L), verb(R)
fade = np.interp(t, [0, 0.6, DUR - 2.5, DUR], [0, 1, 1, 0]); L *= fade; R *= fade
L, R = np.tanh(1.4 * L / np.abs(L).max()), np.tanh(1.4 * R / np.abs(R).max())
pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L / pk * 0.9, R / pk * 0.9
with wave.open("cool.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
print("ok")
