import wave, sys, numpy as np
def rd(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32767; return a
v, f = rd(sys.argv[1]), rd(sys.argv[2])
n = max(len(v), len(f)); v = np.pad(v, (0, n - len(v))); f = np.pad(f, (0, n - len(f)))
env = np.convolve(np.abs(v), np.ones(4410) / 4410, "same")            # duck the effects a little under the voice
duck = 1 - 0.45 * np.clip(env / 0.05, 0, 1)
m = v * 1.0 + f * 0.6 * duck
m /= max(1, np.abs(m).max() / 0.95)
w = wave.open(sys.argv[3], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close()
