import subprocess,os,sys
from PIL import Image
P=sys.argv[1];OUT=sys.argv[2];N=720*1280*3
dec=subprocess.Popen(["ffmpeg","-v","error","-i","src.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","720x1280","-r","30","-i","-",
  "-i","audio_full.wav","-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
  "-c:a","aac","-b:a","192k","-ac","2","-movflags","+faststart",OUT],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(N)
    if len(b)<N:break
    p=f"new/{i:05d}.png"
    if os.path.exists(p):b=Image.open(p).convert("RGB").tobytes()
    enc.stdin.write(b);i+=1
for j in range(1728,1908):
    enc.stdin.write(Image.open(f"tail_{P}/{j:05d}.png").convert("RGB").tobytes())
enc.stdin.close();enc.wait()
