"""EP4 sound effects (no music): hospital beeps, rewind, rain + car, footsteps, whistle, kicks, net, small crowd."""
import numpy as np, wave, sys
import ep4
sr = 44100
N = int((ep4.TOTAL + 0.1) * sr)
out = np.zeros(N, np.float32)
rng = np.random.default_rng(4)
S = ep4.STARTS
D = ep4.D


def add(t, sig, g=1.0):
    i = int(t * sr)
    if i >= N or i < 0:
        return
    n = min(len(sig), N - i)
    out[i:i + n] += g * sig[:n]


lp = lambda x, k: np.convolve(x, np.ones(k) / k, "same")
noise = lambda d: rng.standard_normal(int(d * sr)).astype(np.float32)
def env(n, a=.005, r=.2):
    t = np.arange(n) / sr
    return np.minimum(1, t / a) * np.exp(-t / r)
def tone(f, d, g=1, r=.08):
    x = np.arange(int(d * sr)) / sr
    return np.sin(2 * np.pi * f * x) * env(len(x), .003, r) * g
def kick(t, g=1):
    x = np.arange(int(.25 * sr)) / sr
    add(t, np.sin(2 * np.pi * (150 * np.exp(-x * 18) + 60) * x) * np.exp(-x * 14) + .3 * noise(.25) * np.exp(-x * 60), .55 * g)
def thud(t, g=1):
    x = np.arange(int(.4 * sr)) / sr
    add(t, np.sin(2 * np.pi * (90 * np.exp(-x * 5)) * x) * np.exp(-x * 9), .6 * g)
def net(t):
    add(t, lp(noise(.6), 3) * env(int(.6 * sr), .02, .18), .2)
def whoosh(t, g=1):
    n = int(.3 * sr)
    add(t - .08, lp(noise(.3), 10) * np.sin(np.linspace(0, np.pi, n)) ** 2, .2 * g)
def cheer(t, d=1.4, g=1):   # a few parents clapping / cheering (small local trial)
    n = int(d * sr)
    add(t, lp(noise(d), 25) * np.sin(np.linspace(0, np.pi, n)) ** 0.7, .18 * g)
    for k in range(int(d * 9)):
        add(t + rng.uniform(0, d * 0.8), lp(noise(.03), 2) * env(int(.03 * sr), .001, .01), .25 * g)
def groan(t):
    n = int(1.0 * sr)
    add(t, lp(noise(1.0), 80) * np.sin(np.linspace(0, np.pi, n)), .3)
def whistle(t, d=.5):
    x = np.arange(int(d * sr)) / sr
    add(t, np.sin(2 * np.pi * (2900 + 60 * np.sin(2 * np.pi * 30 * x)) * x) * np.minimum(1, x / .02) * np.minimum(1, (d - x) / .05), .12)
def step(t, g=1):
    add(t, lp(noise(.06), 6) * env(int(.06 * sr), .002, .02), .35 * g)
def beep(t):
    add(t, tone(1046, .12, 1, .05), .07)
def rainbed(t0, t1, g):
    n = int((t1 - t0) * sr)
    sig = lp(noise(t1 - t0), 4) * 0.6 + lp(noise(t1 - t0), 40) * 1.2
    fade = np.minimum(1, np.minimum(np.arange(n) / (.3 * sr), (n - np.arange(n)) / (.3 * sr)))
    add(t0, sig * fade, g)

# hook: sound hit + sprint
thud(0, 1.6); whoosh(0.02, 1.4)
for k in range(int(D(0) / 0.18)):
    step(0.05 + k * 0.18, 1.0)
# rewind sweep
n = int(0.8 * sr); x = np.arange(n) / sr
add(S[1], np.sin(2 * np.pi * (300 + 1800 * x / 0.8) * x) * 0.25 * np.sin(np.linspace(0, np.pi, n)) + lp(noise(.8), 3) * .15, .4)
thud(S[1] + 0.35 * D(1), 1.0)
# hospital night: rain on the window, monitor beeps
rainbed(S[1] + 0.35 * D(1), S[5], 0.035)
t = S[1] + 0.4 * D(1)
while t < S[5] + 0.5:
    beep(t); t += 0.94
# morning: doctor's footsteps, cane tap
for k in range(5):
    step(S[5] + 0.05 + k * 0.14 * D(5) / 2, 0.6)
thud(S[6] + 0.3 * D(6), 0.7); add(S[6] + 0.32 * D(6), tone(1500, .08, 1, .02), .15)
for k in range(3):
    thud(S[6] + (0.5 + k * 0.12) * D(6), 0.35)
# car in the rain
rainbed(S[7], S[8], 0.14)
x = np.arange(int(D(7) * sr)) / sr
add(S[7], (np.sin(2 * np.pi * 55 * x) * 0.5 + lp(noise(D(7)), 60)[:len(x)] * 0.8) * 0.12)
whoosh(S[7] + 0.55 * D(7), 1.2)
# sprint along the fence
for k in range(int(D(8) / 0.17)):
    step(S[8] + k * 0.17, 1.0)
# trial ambience: distant kicks, voices
x = np.arange(int((S[18] - S[8]) * sr)) / sr
add(S[8], lp(noise(S[18] - S[8]), 50)[:len(x)] * 0.045)
for k in range(10):
    kick(S[9] + k * 1.1 + rng.uniform(0, .5), 0.12)
# freeze: heartbeat
for k in range(2):
    thud(S[11] + 0.55 * D(11) + k * 0.6, 0.8); thud(S[11] + 0.55 * D(11) + k * 0.6 + 0.16, 0.5)
# 'Go.' whistle
whistle(S[12] + 0.75 * D(12), 0.45)
for k in range(int(0.7 * D(12) / 0.2)):
    step(S[12] + k * 0.2, 0.6)
# goal through the legs
kick(S[13] + 0.148 * D(13), 1.2); net(S[13] + 0.51 * D(13)); groan(S[13] + 0.52 * D(13))
thud(S[13] + 0.51 * D(13), 0.8)
# getting up, Grandad's nod
thud(S[14] + 0.2 * D(14), 0.5)
# 1v1 save
kick(S[15] + 0.6 * D(15)); thud(S[15] + 0.72 * D(15), 1.3); cheer(S[15] + 0.74 * D(15), 1.4)
# Mason's last kick + fingertips + crossbar
kick(S[16] + 0.18 * D(16), 1.3)
whoosh(S[16] + 0.4 * D(16), 1.2)
th = S[16] + 0.55 * D(16)
thud(S[16] + (0.4 + 0.6 * 0.52) * D(16), 0.9)
thud(th, 1.5); add(th + 0.02, tone(520, .5, 1, .2), .18); cheer(th + 0.1, 1.8, 1.3)
# final whistle
whistle(S[17] + 0.02, .25); whistle(S[17] + .35, .25); whistle(S[17] + .7, .7)
cheer(S[17] + 0.55 * D(17), 1.6, 1.2)
# twist + Mum + Grandad
whoosh(S[18], 1.2)
for k in range(2):
    thud(S[18] + 0.6 * D(18) + k * 0.5, 0.6)
for k in range(3):
    thud(S[20] + 0.5 * D(20) + k * 0.55, 0.6); thud(S[20] + 0.5 * D(20) + k * 0.55 + 0.16, 0.4)
whoosh(S[21], 1.2)
for k in range(10):
    add(S[21] + 0.3 + k * 0.11, lp(noise(.02), 2) * env(int(.02 * sr), .001, .008), .15)   # typing
whoosh(S[22], 1.0)
add(S[22] + 0.8, tone(880, .15, 1, .06) + tone(1320, .15, 1, .06), .2)
for s_ in S[2:]:
    whoosh(s_, 0.6)
out[-int(.4 * sr):] *= np.linspace(1, 0, int(.4 * sr))
out /= max(1, np.abs(out).max() / 0.9)
w = wave.open(sys.argv[1] if len(sys.argv) > 1 else "sfx4.wav", "wb")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
