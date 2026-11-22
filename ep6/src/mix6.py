import numpy as np, subprocess, wave, sys, json, os
P=sys.argv[1]; os.environ["PLATFORM"]=P
import ep6
sr=44100
def load(f, ss=None, to=None):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+(["-to",str(to)] if to is not None else [])+["-i",f,"-ac","1","-ar",str(sr),"-f","s16le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.int16).astype(np.float32)/32768
j=json.load(open("vo/ep6_lines.json"))
last=j["lines"][-1][0]
if P=="youtube":
    v=np.concatenate([load("vo/ep6.mp3",0,last-0.02), load("vo/ep6.mp3",j["yt_tail"][0]-0.03,j["yt_tail"][1]+0.1)])
else:
    v=load("vo/ep6.mp3",0,j["lines"][-1][1]+0.15)
w=wave.open("sfx6.wav"); fx=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
N=int((ep6.TOTAL+0.1)*sr)
out=np.zeros(N,np.float32)
fx=fx[:N]; out[:len(fx)]+=fx*0.75
vv=np.zeros(N,np.float32); vv[:min(N,len(v))]=v[:N]
env=np.convolve(np.abs(vv),np.ones(2205)/2205,"same")
out*=1-0.55*np.clip(env/0.05,0,1)
out+=vv
out[-int(.3*sr):]*=np.linspace(1,0,int(.3*sr))
out/=max(1,np.abs(out).max()/0.95)
w=wave.open(f"mix6_{P}.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
print(P,len(out)/sr)
