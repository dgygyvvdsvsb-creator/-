"""EP6 (1984) sound effects, no music: training, tape rewind, terrace chants, rain, saves, the collision, silence, stretcher."""
import numpy as np, wave, sys
import ep7 as E
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
RIGHT = E.RIGHT
# 0 hook: hit, the crowd holding its breath, run-up steps
thud(0, 1.6); whoosh(0.02, 1.2); bed(0, S[5], 0.07, 40)
for k in range(int(D(0) / 0.25)): step(0.1 + k * 0.25, 0.5)
# 1 vote: heartbeat
for k in range(3): thud(S[1] + 0.2 + k * 0.6, 0.45); thud(S[1] + 0.36 + k * 0.6, 0.3)
# 2 the kick, the dive
kick(S[2] + 0.18 * D(2), 1.3); whoosh(S[2] + 0.3 * D(2), 1.2); thud(S[2] + 0.5 * D(2), 0.9)
if not RIGHT: thud(S[2] + 0.5 * D(2), 1.6)
# 3 result
if RIGHT:
    net(S[3]); roar(S[3] + 0.05, 2.0, 1.4)
else:
    roar(S[3] + 0.05, 2.0, 1.6)
# 4 pen on the clipboard
for k in range(6): add(S[4] + 0.3 * D(4) + k * 0.07, lp(noise(.05), 3) * env(int(.05 * sr), .002, .02), .2)
# 5 Mason laughs (short bursts)
for k in range(4): add(S[5] + 0.3 + k * 0.18, lp(noise(.12), 8) * env(int(.12 * sr), .005, .05), .35)
# 6-7 heartbeat while he stares
for k in range(5): thud(S[6] + 0.2 + k * 0.6, 0.5); thud(S[6] + 0.36 + k * 0.6, 0.3)
# 8 tape rewind into 1984
n = int(.9 * sr); x = np.arange(n) / sr
add(S[8] + 0.65 * D(8), np.sin(2 * np.pi * (2000 - 1700 * x / .9) * x) * .2 * np.sin(np.linspace(0, np.pi, n)), .5)
add(S[9], lp(noise(0.35), 2) * 0.6)
# 9-12 1984: rain + terrace
bed(S[9], S[13], 0.06, 4)
chant(S[9] + 0.4, S[12], 1.0)
whoosh(S[11] + 0.2, 1.5)
for k in range(3): thud(S[12] + 0.2 + k * 0.45, 0.5)
# 13 knee first
thud(S[13], 2.0); add(S[13], lp(noise(.3), 2) * env(int(.3 * sr), .001, .08), .5); roar(S[13] + 0.1, 0.7, 1.0)
# 14-15 silence: rain only, stretcher steps
bed(S[14], S[16], 0.03, 4)
for k in range(5): step(S[14] + 0.2 + k * 0.45, 0.6)
# 16 back to today: tape glitch, whistle hits the grass
add(S[16], lp(noise(0.3), 2) * 0.5)
add(S[16] + 0.65 * D(16), tone(2200, .25, .06), .2); thud(S[16] + 0.65 * D(16), 0.4)
bed(S[16], S[18], 0.03, 40)
for k in range(6): step(S[17] + 0.2 + k * 0.4, 0.5)
# 18-21 night: rain on the window, ringing, the call, hang-up beep, message ping
bed(S[18], S[22], 0.035, 4)
for k in range(2): add(S[18] + 0.3 + k * 0.9, tone(440, .4, .3) + tone(480, .4, .3), .12)
add(S[20] + 0.62 * D(20), tone(620, .15, .06), .2); add(S[20] + 0.62 * D(20) + 0.2, tone(620, .15, .06), .2)
add(S[21] + 0.2, tone(1320, .12, .05) + tone(1760, .12, .05), .2)
for k in range(3): thud(S[21] + 0.6 + k * 0.55, 0.5)
# 22 typing, 23 pop
whoosh(S[22], 1.2)
for k in range(10): add(S[22] + 0.3 + k * 0.11, lp(noise(.02), 2) * env(int(.02 * sr), .001, .008), .15)
whoosh(S[23]); add(S[23] + 0.8, tone(880, .15) + tone(1320, .15), .2)
for s_ in S[1:]: whoosh(s_, 0.5)
out[-int(.4 * sr):] *= np.linspace(1, 0, int(.4 * sr)); out /= max(1, np.abs(out).max() / 0.9)
w = wave.open(sys.argv[1], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
