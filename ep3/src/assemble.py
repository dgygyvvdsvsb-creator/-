import subprocess,os,numpy as np
from PIL import Image
W,H=720,1280;N=W*H*3
dec=subprocess.Popen(["ffmpeg","-v","error","-i","src.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","720x1280","-r","30","-i","-",
  "-i","src.mp4","-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
  "-c:a","aac","-b:a","192k","-ac","2","-movflags","+faststart","-shortest","EP3_FINAL_v5.mp4"],stdin=subprocess.PIPE)
i=0;rep=0
while True:
    b=dec.stdout.read(N)
    if len(b)<N:break
    p=f"new/{i:05d}.png"
    if os.path.exists(p):
        b=Image.open(p).convert("RGB").tobytes();rep+=1
    enc.stdin.write(b);i+=1
enc.stdin.close();enc.wait();print("frames",i,"replaced",rep)
