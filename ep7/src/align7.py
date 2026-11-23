"""Align the narration mp3 to script lines: speech segments from silencedetect, grouped by DP on expected length."""
import re, subprocess, sys, json

SPOKEN = [
    "Last kick. Saturday's shirt.",
    "Most of you said: right.",
    "You go right. He goes left.",
    "Goal. The reserves win.",
    "Saturday's shirt: Dixon. Not you.",
    "But the coach isn't looking at Dixon.",
    "He stares at your gloves. Red string.",
    "And goes pale.",
    "Nineteen eighty-four. Ten thousand in the rain.",
    "In goal: Grandad. Same gloves.",
    "The ball hangs in the lights.",
    "Number nine jumps...",
    "Knee first.",
    "A stretcher. Silence.",
    "Grandad never played again.",
    "Today. His whistle falls.",
    "He walks away. Not a word.",
    "That night, you call Grandad.",
    "Who is my coach?",
    "Silence. Then he hangs up.",
    "One message: Stay away from him.",
    "Ask the coach... or stay away?",
    "Vote below. Follow for part eight.",
]
SPOKEN_OLD = [
    "They started without you.",
    "You chose the trial. But first... one night.",
    "Hospital chair. Beeping monitor. No sleep.",
    "Four a.m. His hand finds yours.",
    "Go to that trial. Not without you.",
    "Eight a.m. He can go home.",
    "Grandad grabs his cane. Home? No. Riverside.",
    "Mum's old car. Two hours. Rain.",
    "You sprint. Gloves in hand.",
    "Keepers were at nine thirty. Too late.",
    "Mason laughs. Hospital boy.",
    "Then the coach sees Grandad... and freezes.",
    "Ten minutes. Trial match. Go.",
    "First shot. Through your legs. No sleep.",
    "You get back up. Like Grandad said.",
    "One on one. You spread big. Saved!",
    "Last kick. Mason. Top corner... fingertips! Out!",
    "Final whistle. You're in.",
    "But you'd live there. Two hours from home.",
    "Mum works nights. Who looks after Grandad?",
    "He just says, Go. His hand shakes.",
    "The academy... or home?",
    "Vote below. Follow for episode five.",
]


def segments(path, noise="-35dB", d=0.25):
    out = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    dur = float(re.findall(r"Duration: (\d+):(\d+):([\d.]+)", out)[0][2]) + 60 * float(re.findall(r"Duration: (\d+):(\d+):([\d.]+)", out)[0][1])
    # speech = complement of silences
    sil = sorted(zip(([0.0] if st and en and en[0] < st[0] else []) + st, en + ([dur] if len(st) > len(en) else [])))
    speech, t = [], 0.0
    for a, b in sil:
        if a - t > 0.05:
            speech.append([t, a])
        t = b
    if dur - t > 0.05:
        speech.append([t, dur])
    return speech


def align(speech, lines):
    w = [len(re.sub(r"[^a-z]", "", l.lower())) for l in lines]
    tot_t = sum(b - a for a, b in speech)
    rate = tot_t / sum(w)
    n, m = len(speech), len(lines)
    INF = 1e18
    best = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for j in range(1, m + 1):
        for i in range(1, n + 1):
            for k in range(j - 1, i):
                if best[k][j - 1] >= INF:
                    continue
                talk = sum(b - a for a, b in speech[k:i])
                gap_before = speech[k][0] - speech[k - 1][1] if k > 0 else 1.0
                cost = ((talk - w[j - 1] * rate) / (w[j - 1] * rate + 0.4)) ** 2 - 0.3 * min(gap_before, 0.8)
                c = best[k][j - 1] + cost
                if c < best[i][j]:
                    best[i][j] = c
                    back[i][j] = k
    res, i = [], n
    for j in range(m, 0, -1):
        k = back[i][j]
        res.append([round(speech[k][0], 3), round(speech[i - 1][1], 3)])
        i = k
    return res[::-1]


if __name__ == "__main__":
    sp = segments(sys.argv[1])
    print(len(sp), "speech segments")
    r = align(sp, SPOKEN)
    for (a, b), l in zip(r, SPOKEN):
        print(f"{a:6.2f} {b:6.2f}  {l}")
    json.dump(r, open(sys.argv[2], "w"))
