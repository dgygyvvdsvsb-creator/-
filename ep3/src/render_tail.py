import os,sys
from multiprocessing import Pool
P=os.environ["PLATFORM"];D=f"tail_{P}";os.makedirs(D,exist_ok=True)
def work(i):
    from seg_f import seg_F
    p=f"{D}/{i:05d}.png"
    seg_F((i+0.5)/30).save(p,compress_level=1)
if __name__=="__main__":
    with Pool(4) as pool: list(pool.imap_unordered(work,range(1728,1908),chunksize=6))
