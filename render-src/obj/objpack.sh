set -e
cd /tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad
rm -rf objout; mkdir -p objout/Orange_County_Epe_3D; python3 objexp.py > objexp.log 2>&1; tail -1 objexp.log
cd objout/Orange_County_Epe_3D
python3 - <<'PY'
from PIL import Image; import glob, os
mtl=glob.glob("*.mtl")[0]; s=open(mtl).read()
for f in [x for x in os.listdir(".") if x.lower().endswith((".png",".jpg",".jpeg",".tif",".tiff",".tga",".exr"))]:
    if os.path.getsize(f)<1_500_000 and not f.lower().endswith(".tga"): continue
    im=Image.open(f); im.load()
    if max(im.size)>2048: im.thumbnail((2048,2048))
    alpha= im.mode in("RGBA","LA") and im.getchannel("A").getextrema()[0]<250
    if alpha: n=os.path.splitext(f)[0]+".png"; im.save(n,optimize=True)
    else:
        n=os.path.splitext(f)[0]+".jpg"; n = n if n!=f else os.path.splitext(f)[0]+"_c.jpg"; im.convert("RGB").save(n,quality=88)
    if n!=f: os.remove(f); s=s.replace(f,n)
open(mtl,"w").write(s)
PY
sed -i -E 's/([0-9]\.[0-9]{4})[0-9]+/\1/g' "Orange County Epe.obj"
cat > readme.txt <<'R'
Orange County Epe - 3D model (OBJ + MTL + textures), metres, Y-up.
Open in Blender (File > Import > Wavefront OBJ), SketchUp Pro, 3ds Max, Lumion, Twinmotion etc.
Keep all files in the same folder so the textures load. Trees are lightened for file size.
R
cd ../..; python3 objchk.py 2>&1 | grep CHK_DONE
