import numpy as np, wave, os, sys
import ep6
sr=44100; N=int((ep6.TOTAL+0.1)*sr); out=np.zeros(N,np.float32); rng=np.random.default_rng(6)
S=ep6.STARTS; D=[(S[i+1] if i+1<len(S) else ep6.TOTAL)-S[i] for i in range(len(S))]
def add(t,sig,g=1.0):
    i=int(t*sr)
    if i>=N or i<0: return
    n=min(len(sig),N-i); out[i:i+n]+=g*sig[:n]
lp=lambda x,k: np.convolve(x,np.ones(k)/k,"same")
noise=lambda d: rng.standard_normal(int(d*sr)).astype(np.float32)
def env(n,a=.005,r=.2): t=np.arange(n)/sr; return np.minimum(1,t/a)*np.exp(-t/r)
def kick(t,g=1): x=np.arange(int(.25*sr))/sr; add(t,np.sin(2*np.pi*(150*np.exp(-x*18)+60)*x)*np.exp(-x*14)+.3*noise(.25)*np.exp(-x*60),.55*g)
def thud(t,g=1): x=np.arange(int(.4*sr))/sr; add(t,np.sin(2*np.pi*(90*np.exp(-x*5))*x)*np.exp(-x*9),.6*g)
def net(t): add(t,lp(noise(.6),3)*env(int(.6*sr),.02,.18),.18)
def whoosh(t): n=int(.3*sr); add(t-.08,lp(noise(.3),10)*np.sin(np.linspace(0,np.pi,n))**2,.2)
def roar(t,d=1.6,g=1): n=int(d*sr); add(t,lp(noise(d),30)*np.sin(np.linspace(0,np.pi,n))**0.7,.35*g)
def groan(t): n=int(1.2*sr); add(t,lp(noise(1.2),80)*np.sin(np.linspace(0,np.pi,n)),.4)
def whistle(t,d=.5): x=np.arange(int(d*sr))/sr; add(t,np.sin(2*np.pi*(2900+60*np.sin(2*np.pi*30*x))*x)*np.minimum(1,x/.02)*np.minimum(1,(d-x)/.05),.12)
def knock(t): x=np.arange(int(.12*sr))/sr; add(t,np.sin(2*np.pi*180*x)*np.exp(-x*40)+.3*noise(.12)*np.exp(-x*80),.5)
out+=lp(noise(N/sr),40)[:N]*0.05          # crowd bed
thud(0,1.6); kick(0.05)
for s in S[1:]: whoosh(s)
for k in range(3): knock(S[1]+0.15+k*0.28)
for q in range(3):
    t0=S[3]+q*D[3]/3; kick(t0+0.02,0.7); thud(t0+0.45*D[3]/3,0.6)
roar(S[8]+0.2,2.0); whistle(S[8]+1.2,0.35)
A0=S[9]; AL=S[11]-S[9]
kick(A0+0.06*AL,0.7); kick(A0+0.38*AL,1.3); net(A0+0.78*AL); groan(A0+0.78*AL)
kick(S[13]+0.05); thud(S[13]+0.4*D[13]); thud(S[13]+0.6*D[13],1.2); roar(S[13]+0.6*D[13])
kick(S[14]+0.6*D[14]); thud(S[14]+0.75*D[14],1.3); roar(S[14]+0.75*D[14])
kick(S[15]+0.3*D[15]); net(S[15]+0.6*D[15]); roar(S[15]+0.6*D[15],2.2,1.4)
for k in range(4): add(S[16]+0.3+k*0.5,np.sin(2*np.pi*880*np.arange(int(.15*sr))/sr)*env(int(.15*sr),.003,.08),.1)
kick(S[18]+0.62*D[18],1.2)
for k in range(5): thud(S[19]+0.2+k*0.42,.6)
thud(S[20]+0.35*D[20],1.6); add(S[20]+0.35*D[20],np.sin(2*np.pi*520*np.arange(int(.5*sr))/sr)*env(int(.5*sr),.002,.2),.18); roar(S[20]+0.4*D[20],2.0,1.5)
whistle(S[21]+0.1,0.3); whistle(S[21]+0.5,0.3); whistle(S[21]+0.9,0.8)
for k in range(10): thud(S[22]+0.2+k*0.55,.6)
whoosh(S[24])
for q in range(2):
    t0=S[4]+q*D[4]/2; kick(t0+0.05,0.6); thud(t0+0.55*D[4]/2,0.7)
whistle(S[17]+0.62*D[17],0.6); thud(S[17]+0.6*D[17],1.3); groan(S[17]+0.6*D[17])
out[-int(.4*sr):]*=np.linspace(1,0,int(.4*sr))
out/=max(1,np.abs(out).max()/0.9)
w=wave.open("sfx6.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
