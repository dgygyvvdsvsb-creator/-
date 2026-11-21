import subprocess, re, json, build
def segs(f, total):
    out = subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","silencedetect=n=-38dB:d=0.18","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",out)]
    en=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",out)]
    s=[]; cur=0.0
    for a,b in zip(st,en):
        if a-cur>0.05: s.append((cur,a))
        cur=b
    if total-cur>0.1: s.append((cur,total))
    return s
S=segs("vo/main.mp3",64.6)
words=[sum(len(w) for w,_ in ws)+2*len(ws) for ws,_ in build.LINES]
N=len(words); M=len(S)
rate=sum(b-a for a,b in S)/sum(words)
import functools
INF=1e18
@functools.lru_cache(None)
def f(i,j):  # lines i.. using segments j..
    if i==N: return (0.0,()) if j==M else (INF,())
    best=(INF,())
    rem=N-i-1
    for k in range(j+1, M-rem+1):
        d=S[k-1][1]-S[j][0]
        c=(d-words[i]*rate)**2
        sub=f(i+1,k)
        if c+sub[0]<best[0]: best=(c+sub[0],(k,)+sub[1])
    return best
cost,cuts=f(0,0)
bounds=[0]+list(cuts)
lines=[]
for i in range(N):
    a=S[bounds[i]][0]; b=S[bounds[i+1]-1][1]
    lines.append((round(a,3),round(b,3)))
for i,(a,b) in enumerate(lines): print(i,a,b,' '.join(w for w,_ in build.LINES[i][0]))
json.dump(lines,open("vo/lines.json","w"))
