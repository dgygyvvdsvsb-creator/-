import os, subprocess, sys
from multiprocessing import Pool
import ep7 as ep4
P = os.environ.get("PLATFORM", "tiktok")
D = sys.argv[3] if len(sys.argv) > 3 else f"f7_{P}"
os.makedirs(D, exist_ok=True)
NF = int(ep4.TOTAL * 30)


def work(i):
    ep4.frame((i + .5) / 30).save(f"{D}/{i:05d}.png", compress_level=1)


if __name__ == "__main__":
    with Pool(4) as pool:
        list(pool.imap_unordered(work, range(NF), chunksize=8))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{D}/%05d.png", "-i", sys.argv[2], "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", sys.argv[1]], check=True)
