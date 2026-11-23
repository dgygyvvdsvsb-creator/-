"""EP7 narration: the single take, with extra breathing room after action lines (TikTok > 60 s)."""
import json, subprocess, wave, os
import numpy as np
SR = 44100
H = os.path.dirname(os.path.abspath(__file__))
EXTRA = {0: 0.7, 2: 0.9, 3: 0.6, 6: 0.6, 7: 0.9, 10: 0.6, 11: 0.8, 12: 0.8, 13: 1.0, 14: 0.6, 16: 0.7, 19: 0.9, 20: 0.9, 21: 0.6}


def load(p):
    x = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(x, np.float32).copy()


v = load(f"{H}/vo/ep7_voice.mp3")
L = json.load(open(f"{H}/vo/lines_raw.json"))
cuts = [0.0] + [(L[i][1] + L[i + 1][0]) / 2 for i in range(len(L) - 1)] + [len(v) / SR]
out, lines, shift = [], [], 0.0
for i in range(len(L)):
    a, b = int(cuts[i] * SR), int(cuts[i + 1] * SR)
    out.append(v[a:b])
    lines.append([round(L[i][0] + shift, 3), round(L[i][1] + shift, 3)])
    ex = EXTRA.get(i, 0.0)
    out.append(np.zeros(int(ex * SR), np.float32))
    shift += ex
voice = np.concatenate(out)
w = wave.open(f"{H}/vo/voice_tiktok.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
json.dump(lines, open(f"{H}/vo/lines_tiktok.json", "w"))
print("voice", round(len(voice) / SR, 2), "last line ends", lines[-1][1])
