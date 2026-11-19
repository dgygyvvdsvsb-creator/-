import sys,importlib
from PIL import Image
mod=importlib.import_module(sys.argv[1]);fn=getattr(mod,sys.argv[2])
ts=[float(x) for x in sys.argv[3].split(",")]
ims=[fn(t).resize((360,640)) for t in ts]
out=Image.new("RGB",(360*len(ims),640))
for i,im in enumerate(ims):out.paste(im,(360*i,0))
out.save(sys.argv[4])
