"""EP6 (1984) sound effects, no music: training, tape rewind, terrace chants, rain, saves, the collision, silence, stretcher."""
import numpy as np, wave, sys
import fb84 as E
sr = 44100; N = int((E.TOTAL + 0.1) * sr); out = np.zeros(N, np.float32); rng = np.random.default_rng(84)
S, D = E.STARTS, E.D
def add(t, sig, g=1.0):
    i = int(t * sr)
    if 0 <= i < N:
        n = min(len(sig), N - i); out[i:i + n] += g * sig[:n]
lp = lambda x, k: np.convolve(x, np.ones(k) / k, "same")
noise = lambda d: rng.standard_normal(int(d * sr)).astype(np.float32)
def env(n, a=.005, r=.2):
    t = np.arange(n) / sr; return np.minimum(1, t / a) * np.exp(-t / r)
def tone(f, d, r=.08):
    x = np.arange(int(d * sr)) / sr; return np.sin(2 * np.pi * f * x) * env(len(x), .003, r)
def kick(t, g=1):
    x = np.arange(int(.25 * sr)) / sr
    add(t, np.sin(2 * np.pi * (150 * np.exp(-x * 18) + 60) * x) * np.exp(-x * 14) + .3 * noise(.25) * np.exp(-x * 60), .55 * g)
def thud(t, g=1):
    x = np.arange(int(.4 * sr)) / sr; add(t, np.sin(2 * np.pi * (90 * np.exp(-x * 5)) * x) * np.exp(-x * 9), .6 * g)
def whoosh(t, g=1):
    n = int(.3 * sr); add(t - .08, lp(noise(.3), 10) * np.sin(np.linspace(0, np.pi, n)) ** 2, .2 * g)
def roar(t, d=1.6, g=1):
    n = int(d * sr); add(t, lp(noise(d), 30) * np.sin(np.linspace(0, np.pi, n)) ** 0.7, .35 * g)
def bed(t0, t1, g, k=40):
    n = int((t1 - t0) * sr); s = lp(noise(t1 - t0), k)[:n]
    f = np.minimum(1, np.minimum(np.arange(n) / (.3 * sr), (n - np.arange(n)) / (.3 * sr))); add(t0, s * f, g)
def chant(t0, t1, g=1):   # terrace chant: rhythmic swells
    x = np.arange(int((t1 - t0) * sr)) / sr
    s = lp(noise(t1 - t0), 60)[:len(x)] * (0.6 + 0.4 * np.sin(2 * np.pi * 1.6 * x) ** 2)
    add(t0, s, .4 * g)
def whistle(t, d=.5):
    x = np.arange(int(d * sr)) / sr
    add(t, np.sin(2 * np.pi * (2700 + 60 * np.sin(2 * np.pi * 30 * x)) * x) * np.minimum(1, x / .02) * np.minimum(1, (d - x) / .05), .12)
def net(t):
    add(t, lp(noise(.6), 3) * env(int(.6 * sr), .02, .18), .2)
def step(t, g=1):
    add(t, lp(noise(.06), 6) * env(int(.06 * sr), .002, .02), .3 * g)
# hook: impact hit at 0
thud(0, 1.8); add(0, lp(noise(.5), 2) * env(int(.5 * sr), .001, .1), .4); bed(0, S[1], 0.06, 4)
# present day: training
bed(S[1], S[4], 0.03, 40)
kick(S[1] + 0.2 * D(1)); thud(S[1] + 0.45 * D(1), 0.8)
for k in range(3): thud(S[2] + 0.2 + k * 0.5, 0.25)            # heartbeat in slow motion
for k in range(3): thud(S[3] + 0.2 + k * 0.45, 0.4 + 0.2 * k)
# tape rewind / static
n = int(.9 * sr); x = np.arange(n) / sr
add(S[3] + 0.7 * D(3), np.sin(2 * np.pi * (2000 - 1700 * x / .9) * x) * .2 * np.sin(np.linspace(0, np.pi, n)), .5)
add(S[4], lp(noise(0.45), 2) * 0.6)
# 1984: rain + crowd under everything until the impact
bed(S[4], S[16], 0.05, 4)
chant(S[5], S[9], 1.0)
bed(S[9], S[16], 0.10, 40)
kick(S[9] + 0.25 * D(9), 1.2); thud(S[9] + 0.42 * D(9), 1.1); roar(S[9] + 0.45 * D(9), 1.4)
thud(S[10] + 0.1 * D(10), 0.6); kick(S[10] + 0.4 * D(10)); thud(S[10] + 0.5 * D(10), 1.2); roar(S[10] + 0.52 * D(10), 1.6, 1.2)
net(S[11] + 0.4 * D(11)); roar(S[11] + 0.42 * D(11), 2.2, 1.6)
kick(S[12] + 0.45 * D(12), 0.8)
for k in range(4): add(S[13] + 0.2 + k * 0.5, tone(660, .2, .1), .08)   # scoreboard clock
whistle(S[13] + 0.55 * D(13), 0.25); kick(S[13] + 0.9 * D(13), 0.9)
whoosh(S[14] + 0.2, 1.5)
for k in range(4): thud(S[15] + 0.3 + k * 0.55, 0.5)           # slow heartbeat on the jump
thud(S[16], 2.0); add(S[16], lp(noise(.3), 2) * env(int(.3 * sr), .001, .08), .5); roar(S[16] + 0.1, 0.8, 1.2)
# SILENCE: only rain, very low
bed(S[17], S[22], 0.03, 4)
thud(S[17] + 0.6 * D(17), 0.7)
add(S[19] + 0.6 * D(19), lp(noise(.5), 3) * env(int(.5 * sr), .02, .15), .08)
for k in range(8): step(S[20] + 0.2 + k * 0.45, 0.6)
add(S[20] + 0.2, lp(noise(2.5), 80) * 0.15)                     # murmur
# back to today
add(S[22], lp(noise(0.3), 2) * 0.5)
add(S[22] + 0.7 * D(22), tone(2200, .25, .06), .2); thud(S[22] + 0.7 * D(22), 0.4)
whoosh(S[23], 1.2)
for k in range(10): add(S[23] + 0.3 + k * 0.11, lp(noise(.02), 2) * env(int(.02 * sr), .001, .008), .15)
whoosh(S[24]); add(S[24] + 0.8, tone(880, .15) + tone(1320, .15), .2)
for s_ in S[1:]: whoosh(s_, 0.5)
out[-int(.4 * sr):] *= np.linspace(1, 0, int(.4 * sr)); out /= max(1, np.abs(out).max() / 0.9)
w = wave.open(sys.argv[1], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
