import numpy as np, wave, build
sr=44100; N=int((build.TOTAL+0.2)*sr); out=np.zeros(N,np.float32)
rng=np.random.default_rng(3)
S=build.STARTS; D=[d for _,d in build.LINES]
def add(t,sig,g=1.0):
    i=int(t*sr); 
    if i>=N: return
    n=min(len(sig),N-i); out[i:i+n]+=g*sig[:n]
def env(n,a=0.005,r=0.2):
    t=np.arange(n)/sr; return np.minimum(1,t/a)*np.exp(-t/r)
def noise(d): return rng.standard_normal(int(d*sr)).astype(np.float32)
def lp(x,k): return np.convolve(x,np.ones(k)/k,"same")
def tone(f,d,r=0.2): t=np.arange(int(d*sr))/sr; return np.sin(2*np.pi*f*t)*env(len(t),0.003,r)
def kick(t,g=1): x=np.arange(int(.25*sr))/sr; add(t,(np.sin(2*np.pi*(150*np.exp(-x*18)+60)*x)*np.exp(-x*14)+.3*noise(.25)*np.exp(-x*60)),.5*g)
def thud(t,g=1): x=np.arange(int(.4*sr))/sr; add(t,np.sin(2*np.pi*(90*np.exp(-x*5))*x)*np.exp(-x*9),.6*g)
def net(t): add(t,lp(noise(.6),3)*env(int(.6*sr),.02,.18),.18)
def whoosh(t,g=1): n=int(.3*sr); add(t-.08,lp(noise(.3),10)*np.sin(np.linspace(0,np.pi,n))**2,.22*g)
def pop(t,g=1): x=np.arange(int(.12*sr))/sr; add(t,np.sin(2*np.pi*(500+2500*x)*x)*np.exp(-x*30),.12*g)
def beep(t,f=1300): add(t,tone(f,.12,.08),.12)
def crack(t): add(t,noise(.08)*env(int(.08*sr),.001,.02),.6); thud(t+.02,1.3)
def heartbeat(t0,t1,period=.8):
    t=t0
    while t<t1: thud(t,.7); thud(t+.18,.45); t+=period
def steps(t0,t1,p=.28):
    t=t0
    while t<t1: add(t,lp(noise(.06),4)*env(int(.06*sr),.001,.02),.12); t+=p
# beds: rain everywhere, crowd on pitch scenes
rain=lp(noise(build.TOTAL+.2),5)-lp(noise(build.TOTAL+.2),60); rain=rain[:N]*0.012
out+=rain
pitch_scenes=[0,1,5,6,7,8,9,10,11,15,17,18]
crowd=lp(noise(build.TOTAL+.2),40)[:N]*0.06
mask=np.zeros(N,np.float32)
for i in pitch_scenes:
    a=int(S[i]*sr); b=int(min(N,(S[i]+D[i])*sr)); mask[a:b]=1
mask=np.convolve(mask,np.ones(4000)/4000,"same")
out+=crowd*mask
# frame-0 impact
thud(0.0,1.6); add(0.0,noise(.15)*env(int(.15*sr),.001,.04),.35)
for st in S[1:]: whoosh(st)
T=S
kick(T[0]+.35); net(T[0]+.15+.45*D[0])
pop(T[1]+.1); pop(T[1]+.9)
pop(T[2]+.5)
for k in range(8): beep(T[3]+k*.25) if k%2==0 else None
pop(T[3]+.05); pop(T[3]+.45)
pop(T[4]+.1); thud(T[4]+.35*D[4],.4); pop(T[4]+.62*D[4])
pop(T[5]+.05); add(T[5]+.9,tone(880,.5,.3)*.5+tone(1320,.5,.3)*.3,.15)
thud(T[6]+.1,.8)
kick(T[7]+.05); thud(T[7]+.4*D[7],1.0)
for q in range(4):
    t0=T[9]+q*D[9]/4; kick(t0+.02); net(t0+.35)
steps(T[10]+.3*D[10],T[10]+D[10]-.05,.22); kick(T[10]+D[10]-.05,1.3)
thud(T[11]+.05,1.4); add(T[11]+.05,noise(.3)*env(int(.3*sr),.002,.1),.25); kick(T[11]+.05)
for k in range(3):  # phone ring
    add(T[12]+.1+k*.6,(tone(660,.25,.2)+tone(830,.25,.2))*.5,.2)
pop(T[13]+.45*D[13]); pop(T[13]+.65*D[13])
pop(T[14]+.8); pop(T[14]+.6*D[14])
whoosh(T[15]+.1); crack(T[15]+.36*D[15]); pop(T[15]+.45*D[15])
add(T[16]+.1*D[16],lp(noise(.5),2)*.6*np.abs(np.sin(np.linspace(0,30,int(.5*sr)))),.12)
pop(T[16]+.55*D[16]); pop(T[16]+.6*D[16])
steps(T[17],T[17]+.6*D[17]); pop(T[17]+.62*D[17])
heartbeat(T[18],T[19]+D[19])
pop(T[19]+.05); pop(T[19]+.2)
whoosh(T[20]); pop(T[20]+0.8,2)
for j,fq in enumerate((1568,2093,2637)): add(T[20]+0.85+j*.07,tone(fq,.3,.12),.08)
out[-int(.3*sr):]*=np.linspace(1,0,int(.3*sr))
out=np.clip(out/ max(1,np.abs(out).max()/0.9),-1,1)
w=wave.open("sfx.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
print(len(out)/sr)
