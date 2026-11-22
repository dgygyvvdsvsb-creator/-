import os, subprocess, sys
from multiprocessing import Pool
import ep6
P=os.environ.get("PLATFORM","tiktok"); D=f"f6_{P}"; os.makedirs(D,exist_ok=True)
NF=int(ep6.TOTAL*30)
def work(i):
    ep6.frame((i+.5)/30).save(f"{D}/{i:05d}.png",compress_level=1)
if __name__=="__main__":
    with Pool(4) as pool: list(pool.imap_unordered(work,range(NF),chunksize=8))
    audio=sys.argv[2] if len(sys.argv)>2 else "sfx6.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",f"{D}/%05d.png","-i",audio,"-map","0:v","-map","1:a",
      "-c:v","libx264","-preset","medium","-crf","14","-tune","animation","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ac","2","-shortest","-movflags","+faststart",sys.argv[1]],check=True)
