from multiprocessing import Pool
def work(i):
    from seg_h import seg_H
    seg_H((i+0.5)/30).save(f"new/{i:05d}.png",compress_level=1)
if __name__=="__main__":
    with Pool(4) as p: list(p.imap_unordered(work,range(0,106),chunksize=4))
