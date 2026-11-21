import subprocess, re, json, functools, os
os.environ["PLATFORM"]="tiktok"
import recap
f="vo/recap.mp3"
total=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
out=subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","silencedetect=n=-38dB:d=0.18","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",out)]
en=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",out)]
S=[];cur=0.0
for a,b in zip(st,en):
    if a-cur>0.05: S.append((cur,a))
    cur=b
if total-cur>0.1: S.append((cur,total))
# last spoken block = "Subscribe. Part six decides." after a long pause
gaps=[(S[i+1][0]-S[i][1],i) for i in range(len(S)-1)]
g,i_last=max(gaps[-6:])
yt=S[i_last+1:]; S=S[:i_last+1]
words=[sum(len(w) for w,_ in ws)+2*len(ws) for ws in recap.RLINES]
N=len(words);M=len(S)
rate=sum(b-a for a,b in S)/sum(words)
@functools.lru_cache(None)
def F(i,j):
    if i==N: return (0.0,()) if j==M else (1e18,())
    best=(1e18,())
    for k in range(j+1,M-(N-i-1)+1):
        d=S[k-1][1]-S[j][0]; c=(d-words[i]*rate)**2; sub=F(i+1,k)
        if c+sub[0]<best[0]: best=(c+sub[0],(k,)+sub[1])
    return best
_,cuts=F(0,0); bounds=[0]+list(cuts)
lines=[(round(S[bounds[i]][0],3),round(S[bounds[i+1]-1][1],3)) for i in range(N)]
for i,(a,b) in enumerate(lines): print(i,a,b,' '.join(w for w,_ in recap.RLINES[i]))
print("youtube ending",yt)
# YouTube: last line keeps "This is From Zero to Legend." then the Subscribe take is spliced in
json.dump({"lines":lines,"yt_tail":[yt[0][0],yt[-1][1]],"main_end":lines[-1][1]},open("vo/recap_lines.json","w"))
