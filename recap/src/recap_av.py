import numpy as np, subprocess, wave, sys, os, json, random
P=sys.argv[1]; os.environ["PLATFORM"]=P
import recap
sr=44100
def load(f, ss=None, to=None):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+(["-to",str(to)] if to is not None else [])+["-i",f,"-ac","1","-ar",str(sr),"-f","s16le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.int16).astype(np.float32)/32768
j=json.load(open("vo/recap_lines.json"))
if P=="youtube":
    v=np.concatenate([load("vo/recap.mp3",0,recap.FOLLOW_AT), load("vo/recap.mp3",j["yt_tail"][0]-0.03,j["yt_tail"][1]+0.1)])
else:
    v=load("vo/recap.mp3",0,j["lines"][-1][1]+0.15)
N=int((recap.RTOTAL+0.1)*sr); out=np.zeros(N,np.float32)
rng=np.random.default_rng(4)
def add(t,sig,g=1.0):
    i=int(t*sr)
    if i>=N: return
    n=min(len(sig),N-i); out[i:i+n]+=g*sig[:n]
def lp(x,k): return np.convolve(x,np.ones(k)/k,"same")
noise=lambda d: rng.standard_normal(int(d*sr)).astype(np.float32)
def env(n,a=.005,r=.2): t=np.arange(n)/sr; return np.minimum(1,t/a)*np.exp(-t/r)
def thud(t,g=1): x=np.arange(int(.4*sr))/sr; add(t,np.sin(2*np.pi*(90*np.exp(-x*5))*x)*np.exp(-x*9),.6*g)
def kick(t): x=np.arange(int(.25*sr))/sr; add(t,np.sin(2*np.pi*(150*np.exp(-x*18)+60)*x)*np.exp(-x*14),.5)
def whoosh(t): n=int(.3*sr); add(t-.08,lp(noise(.3),10)*np.sin(np.linspace(0,np.pi,n))**2,.2)
def pop(t,g=1): x=np.arange(int(.12*sr))/sr; add(t,np.sin(2*np.pi*(500+2500*x)*x)*np.exp(-x*30),.12*g)
out+=(lp(noise(N/sr),5)-lp(noise(N/sr),60))[:N]*0.01
out+=lp(noise(N/sr),40)[:N]*0.035
S=recap.RSTARTS
thud(0,1.6)
for s in S[1:]: whoosh(s)
for k in range(10): kick(S[0]+0.25+k*0.28)
pop(S[1]+1.5); pop(S[2]+0.2)
for k in range(6): thud(S[3]+0.3+k*0.45,.5)
kick(S[4]+2.6); kick(S[5]+0.1); thud(S[5]+0.6,1.2)
thud(S[6]+1.0,1.0)
for k in range(4): add(S[6]+1.3+k*0.4,np.sin(2*np.pi*np.where((np.arange(int(.4*sr))/sr*2.5)%1<.5,660,880)*np.arange(int(.4*sr))/sr).astype(np.float32)*.2,.06)
pop(S[7]+0.1); pop(S[7]+0.25); pop(S[7]+2.3,1.5)
kick(S[9]+0.05); thud(S[9]+0.1,1.2); pop(S[9]+1.7,1.5)
thud(S[11]+0.6,1.3)
pop(S[12]+0.3); pop(S[13]+1.8); pop(S[14]+0.9)
for k in range(6): pop(S[15]+0.05+k*0.28)
whoosh(S[16]); pop(S[16]+1.2,2)
env_v=np.convolve(np.abs(np.pad(v,(0,max(0,N-len(v))))[:N]),np.ones(2205)/2205,"same")
out*=1-0.55*np.clip(env_v/0.05,0,1)
if os.environ.get("NOVOICE") != "1":
    out[:len(v)]+=v[:N]
out[-int(.4*sr):]*=np.linspace(1,0,int(.4*sr))
out/=max(1,np.abs(out).max()/0.95)
w=wave.open(f"recap_mix_{P}.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
# video
from multiprocessing import Pool
D=f"rframes_{P}"; os.makedirs(D,exist_ok=True)
NF=int(recap.RTOTAL*30)
def work(i):
    recap.rframe((i+.5)/30).save(f"{D}/{i:05d}.png",compress_level=1)
if __name__=="__main__":
    with Pool(4) as pool: list(pool.imap_unordered(work,range(NF),chunksize=8))
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",f"{D}/%05d.png","-i",f"recap_mix_{P}.wav","-map","0:v","-map","1:a",
      "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ac","2","-shortest","-movflags","+faststart",f"START_HERE_{P}" + ("_novoice" if os.environ.get("NOVOICE") == "1" else "") + ".mp4"],check=True)
    print(P,"done")
