import os,sys,subprocess
from multiprocessing import Pool
P=os.environ.get("PLATFORM","tiktok"); D=f"frames_{P}"; os.makedirs(D,exist_ok=True)
import build
NF=int(build.TOTAL*30)
def work(i):
    p=f"{D}/{i:05d}.png"
    if not os.path.exists(p): build.frame((i+.5)/30).save(p,compress_level=1)
if __name__=="__main__":
    with Pool(4) as pool: list(pool.imap_unordered(work,range(NF),chunksize=8))
    out=sys.argv[1]
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",f"{D}/%05d.png","-i",f"mix_{P}.wav","-map","0:v","-map","1:a",
      "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ac","2","-shortest","-movflags","+faststart",out],check=True)
