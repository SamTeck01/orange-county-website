# Join shots with 0.5 s dissolves by blending frames directly (ffmpeg xfade chain dropped time).
import os, sys, shutil
from PIL import Image
src, out, D = sys.argv[1], sys.argv[2], 12
L = [int(x) for x in open("v2_shots.txt").read().split()]
os.makedirs(out, exist_ok=True); [os.remove(os.path.join(out, f)) for f in os.listdir(out)]
starts = [1]; [starts.append(starts[-1] + n) for n in L[:-1]]
k = 0
def put(path=None, img=None):
    global k; k += 1; p = f"{out}/o_{k:05d}.png"
    shutil.copy(path, p) if path else img.save(p)
for i, (s, n) in enumerate(zip(starts, L)):
    a = s + (D if i > 0 else 0); b = s + n - (D if i < len(L) - 1 else 0)
    for f in range(a, b): put(f"{src}/f_{f:04d}.png")
    if i < len(L) - 1:
        for j in range(D):
            A = Image.open(f"{src}/f_{s + n - D + j:04d}.png").convert("RGB"); B = Image.open(f"{src}/f_{starts[i + 1] + j:04d}.png").convert("RGB")
            put(img=Image.blend(A, B, (j + 1) / (D + 1)))
print("frames", k)
