import numpy as np, subprocess, wave, sys, os
P=sys.argv[1]; sr=44100
def load(f, ss=None, to=None):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+(["-to",str(to)] if to is not None else [])+["-i",f,"-ac","1","-ar",str(sr),"-f","s16le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.int16).astype(np.float32)/32768
import json
L=json.load(open("vo/lines.json"))
v=load("vo/main.mp3")
if P=="youtube":
    cut=int(L[-1][0]*sr)
    v=np.concatenate([v[:cut], load("vo/end.mp3",7.40,10.60)])
w=wave.open("sfx.wav"); fx=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
n=max(len(v),len(fx)); out=np.zeros(n,np.float32)
# duck effects under the voice
env=np.convolve(np.abs(np.pad(v,(0,n-len(v)))),np.ones(2205)/2205,"same")
duck=1-0.55*np.clip(env/0.05,0,1)
out[:len(fx)]+=fx*0.75*duck[:len(fx)]
out[:len(v)]+=v*1.0
out/=max(1,np.abs(out).max()/0.95)
w=wave.open(f"mix_{P}.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
print(P,len(out)/sr)
