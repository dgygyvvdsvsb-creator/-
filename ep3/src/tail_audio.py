import numpy as np,subprocess,wave,sys
sr=44100
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","src.mp4","-vn","-ac","1","-ar",str(sr),"-f","s16le","-"],capture_output=True).stdout,np.int16).astype(np.float32)/32768
T0,T1,TAP=57.6,63.6,59.55
n=int((T1-T0)*sr);t=np.arange(n)/sr
rng=np.random.default_rng(1)
# rain: band-limited noise with slow flutter
noise=rng.standard_normal(n+2000).astype(np.float32)
k=np.ones(6)/6;rain=np.convolve(noise,k,"same")[:n]-np.convolve(noise,np.ones(60)/60,"same")[:n]
rain*=0.0045/np.sqrt((rain**2).mean())*(1+0.15*np.sin(t*1.7))
out=rain.copy()
# heartbeat (lub-dub) every 0.85 s, slowing down, quiet
def thump(at,f=55,amp=0.06,dur=0.16):
    i=int(at*sr);m=int(dur*sr)
    if i>=n:return
    tt=np.arange(min(m,n-i))/sr
    out[i:i+len(tt)]+=amp*np.sin(2*np.pi*f*tt)*np.exp(-tt*22)
for b in np.arange(0.35,6.0,0.9):
    thump(b);thump(b+0.22,amp=0.04)
# distant two-tone siren fading out
sir=0.006*np.sin(2*np.pi*np.where((t*1.6)%1<0.5,660,880)*t)*np.clip(1-t/4.5,0,1)
out+=sir
# whoosh as the panel slides in (~57.95)
i=int((57.95-T0)*sr);m=int(0.45*sr)
w=rng.standard_normal(m).astype(np.float32);w=np.convolve(w,np.ones(12)/12,"same")
env=np.sin(np.linspace(0,np.pi,m))**2
out[i:i+m]+=0.05*w*env
# button tap: click + bright pop + sparkle
i=int((TAP-T0)*sr)
tt=np.arange(int(0.25*sr))/sr
pop=0.12*np.sin(2*np.pi*(500+1600*tt)*tt)*np.exp(-tt*25)
out[i:i+len(pop)]+=pop
for j,f in enumerate((1568,2093,2637)):
    a=i+int((0.06+j*0.07)*sr);tt=np.arange(int(0.3*sr))/sr
    out[a:a+len(tt)]+=0.035*np.sin(2*np.pi*f*tt)*np.exp(-tt*12)
# chips pop at 61.05
for at in (61.05,61.15):
    a=int((at-T0)*sr);tt=np.arange(int(0.12*sr))/sr
    out[a:a+len(tt)]+=0.05*np.sin(2*np.pi*(900-300*tt*8)*tt)*np.exp(-tt*35)
# fade out last 0.6 s
out[-int(0.6*sr):]*=np.linspace(1,0,int(0.6*sr))
full=np.concatenate([x[:int(T0*sr)],out])
# ---- hook SFX layered over the original first 3.5 s
def add(at,sig):
    i=int(at*sr);full[i:i+len(sig)]+=sig[:max(0,len(full)-i)]
tt=np.arange(int(0.7*sr))/sr
boom=0.55*np.sin(2*np.pi*(90*np.exp(-tt*3))*tt)*np.exp(-tt*5)          # impact at frame 0
crack=0.25*rng.standard_normal(len(tt))*np.exp(-tt*40)
add(0.0,boom+crack)
for at in (0.55,1.10,2.20,2.53,2.86,3.20):                             # whoosh on every cut
    m=int(0.22*sr);w=np.convolve(rng.standard_normal(m),np.ones(8)/8,"same")
    add(at-0.06,0.10*w*np.sin(np.linspace(0,np.pi,m))**2)
tt=np.arange(int(0.5*sr))/sr
add(1.55,0.45*np.sin(2*np.pi*(120*np.exp(-tt*6))*tt)*np.exp(-tt*8)+0.2*rng.standard_normal(len(tt))*np.exp(-tt*30))  # kick

# blend rain in under the last 0.5 s of the original so the seam is invisible
a=int((T0-0.5)*sr);b=int(T0*sr)
r2=rain[:b-a]*np.linspace(0,1,b-a);full[a:b]+=r2
full=np.clip(full,-1,1)
w=wave.open("audio_full.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
w.writeframes((full*32767).astype(np.int16).tobytes());w.close()
print(len(full)/sr)
