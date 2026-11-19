import os,sys
from multiprocessing import Pool
RANGES=[(106,205,"seg_pen","seg_A"),(285,544,"seg_pen","seg_B"),(970,1096,"seg_c","seg_C"),(1204,1396,"seg_d","seg_D"),(1396,1728,"seg_e","seg_E")]
os.makedirs("new",exist_ok=True)
jobs=[(i,m,f) for a,b,m,f in RANGES for i in range(a,b)]
def work(j):
    i,m,f=j
    p=f"new/{i:05d}.png"
    if os.path.exists(p):return
    import importlib
    fn=getattr(importlib.import_module(m),f)
    fn((i+0.5)/30).save(p,compress_level=1)
if __name__=="__main__":
    with Pool(4) as pool:
        for k,_ in enumerate(pool.imap_unordered(work,jobs,chunksize=8)):
            if k%100==0:print(k,len(jobs),flush=True)
