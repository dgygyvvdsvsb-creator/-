"""Build the per-platform narration tracks + line timings (TikTok = main take; YouTube = main take with lines 1 and 22 from the patch)."""
import json, subprocess, wave, os
import numpy as np
SR = 44100
H = os.path.dirname(os.path.abspath(__file__))


def load(p):
    x = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(x, np.float32).copy()


def save(p, a):
    w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


main = load(f"{H}/vo/ep4_voice_main.mp3")
yt = load(f"{H}/vo/ep4_voice_yt_patch.mp3")
L = json.load(open(f"{H}/vo/lines_raw.json"))
json.dump(L, open(f"{H}/vo/lines_tiktok.json", "w"))
save(f"{H}/vo/voice_tiktok.wav", main)

s = lambda t: int(t * SR)
SH = 0.84                                  # the YouTube line 1 is 0.84 s longer
out = np.zeros(s(len(main) / SR + 2.0), np.float32)
out[:s(1.47)] = main[:s(1.47)]                                   # line 0
seg = yt[:s(3.85)]; out[s(1.61):s(1.61) + len(seg)] = seg         # line 1 (patch)
seg = main[s(4.70):s(62.50)]; out[s(4.70 + SH):s(4.70 + SH) + len(seg)] += seg   # lines 2..21
seg = yt[s(4.20):]; st = 62.66 + SH - 0.08; out[s(st):s(st) + len(seg)] += seg    # line 22 (patch)
save(f"{H}/vo/voice_youtube.wav", out)
Y = [L[0], [1.61, 1.61 + 3.78]] + [[a + SH, b + SH] for a, b in L[2:22]] + [[62.66 + SH, 62.66 + SH + (7.15 - 4.28)]]
json.dump([[round(a, 3), round(b, 3)] for a, b in Y], open(f"{H}/vo/lines_youtube.json", "w"))
print("ok", len(main) / SR, len(out) / SR)
