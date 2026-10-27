# Original cinematic underscore: warm pads, piano arpeggios, soft pulse, swell and resolve. 44.1 kHz stereo WAV.
import numpy as np, sys, wave
SR = 44100; DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 72.0; BPM = 96; BEAT = 60 / BPM
N = int(SR * DUR); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
# Am - F - C - G, 2 bars each (8 beats)
PROG = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
BAR = 4 * BEAT; CH = 2 * BAR
def env(n, a, r):
    e = np.ones(n); ai = min(n, int(a * SR)); ri = min(n, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[n - ri:] *= np.linspace(1, 0, ri); return e
def lp(x, k):  # one-pole low-pass
    y = np.empty_like(x); a = 0.0
    for i in range(0, len(x), 4096):
        seg = x[i:i + 4096]; out = np.empty_like(seg)
        for j, v in enumerate(seg): a += k * (v - a); out[j] = a
        y[i:i + 4096] = out
    return y
def add(sig, start, pan=0.0, gain=1.0):
    s0 = int(start * SR); s1 = min(N, s0 + len(sig))
    if s1 <= s0: return
    L[s0:s1] += sig[:s1 - s0] * gain * (1 - pan) ; R[s0:s1] += sig[:s1 - s0] * gain * (1 + pan)
# master intensity curve: intro soft, build, full, resolve
inten = np.interp(t, [0, 6, 16, DUR - 14, DUR - 4, DUR], [0.35, 0.55, 0.85, 1.0, 0.7, 0.0])
k = 0; time = 0.0
while time < DUR:
    root, chord = PROG[k % 4]; n = int(CH * SR) + int(1.5 * SR)
    tt = np.arange(n) / SR
    pad = np.zeros(n)
    for m in chord + [chord[0] + 12]:
        for d in (-0.12, 0.0, 0.11):  # detuned saw stack
            f = hz(m) * 2 ** (d / 12); ph = (tt * f) % 1.0; pad += (2 * ph - 1) * 0.06
    pad = lp(pad * env(n, 1.4, 1.6), 0.035)
    add(pad, time, -0.25, 0.9); add(np.roll(pad, 600), time, 0.25, 0.9)
    bass = np.sin(2 * np.pi * hz(root - 12) * tt) * env(n, 0.3, 1.2) * 0.35
    add(bass, time, 0, 1.0)
    # piano-like arpeggio in 8ths
    notes = [chord[0] + 12, chord[1] + 12, chord[2] + 12, chord[1] + 24]
    for i in range(16):
        st = time + i * BEAT / 2
        if st >= DUR: break
        m = notes[i % 4]; nn = int(1.6 * SR); ts = np.arange(nn) / SR
        tone = (np.sin(2 * np.pi * hz(m) * ts) + 0.4 * np.sin(4 * np.pi * hz(m) * ts) + 0.15 * np.sin(6 * np.pi * hz(m) * ts)) * np.exp(-ts * 3.2) * 0.16
        if st > 6: add(tone, st, 0.35 if i % 2 else -0.35)
    k += 1; time += CH
# soft pulse (kick + shaker) from 16 s until the final 6 s
b = 16.0
while b < DUR - 6:
    nn = int(0.4 * SR); ts = np.arange(nn) / SR
    kick = np.sin(2 * np.pi * (45 + 80 * np.exp(-ts * 30)) * ts) * np.exp(-ts * 9) * 0.5
    add(kick, b); 
    sh = np.random.default_rng(int(b * 100)).normal(0, 1, int(0.08 * SR)) * np.exp(-np.arange(int(0.08 * SR)) / SR * 50) * 0.05
    add(sh, b + BEAT / 2, 0.4)
    b += BEAT
# riser into the full section and a reverse swell before the end card
for at in (14.0, DUR - 9.0):
    nn = int(2.0 * SR); ts = np.arange(nn) / SR
    noise = np.random.default_rng(int(at)).normal(0, 1, nn); riser = lp(noise, 0.02) * (ts / 2.0) ** 2 * 0.4
    add(riser, at, 0, 1.0)
# simple stereo reverb: a few feedback delays
def verb(x):
    y = x.copy()
    for d, g in ((0.031, 0.35), (0.047, 0.3), (0.073, 0.25), (0.113, 0.2), (0.17, 0.15)):
        s = int(d * SR); y[s:] += x[:-s] * g
    return y
L = verb(L) * inten; R = verb(R) * inten
peak = max(np.abs(L).max(), np.abs(R).max()); L, R = L / peak * 0.85, R / peak * 0.85
out = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open("score.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print("ok", DUR)
