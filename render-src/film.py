# Preview films. usage: film.py -- <v1|v2> <check|sheet|render>
import bpy, math, sys, os
from mathutils import Vector
D = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2"
which, mode = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.open_mainfile(filepath=f"{D}/epe.blend"); sc = bpy.context.scene
FPS = 24; sc.render.fps = FPS
sc.render.use_motion_blur = False

def ease(u): return u * u * (3 - 2 * u)
def catmull(pts, t):
    n = len(pts) - 1; s = min(n - 1e-6, max(0.0, t * n)); i = int(s); u = s - i
    p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[min(i + 1, n)], pts[min(i + 2, n)]
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u * u * u)

frames = []   # per frame: (loc, tgt, lens, labels, dusk)
if which == "v1":
    # one continuous, slow path; keys with hold-easing between them
    K = [((85, -170, 130), (85, 140, 0)), ((133, -70, 50), (133, 30, 0)), ((133, -24, 24), (133, 14, 2)),
         ((126, 6, 19), (110, 20, 2)), ((126, 28, 15), (106, 45, 0)), ((140, 44, 22), (108, 54, 0)),
         ((133, 95, 46), (128, 210, 0)), ((95, -150, 175), (86, 140, 0))]
    N = 32 * FPS; seg = len(K) - 1
    for f in range(N):
        x = f / (N - 1); s = x * seg; i = min(seg - 1, int(s)); u = ease(s - i)
        a0, t0 = map(Vector, K[i]); a1, t1 = map(Vector, K[i + 1])
        # Catmull through all keys for position, eased within each segment
        loc = catmull([Vector(k[0]) for k in K], (i + u) / seg); tgt = catmull([Vector(k[1]) for k in K], (i + u) / seg)
        frames.append((loc, tgt, 30, loc.z >= 40, False))
else:
    S = [  # (seconds, pos0, pos1, tgt0, tgt1, lens, labels, dusk)
        (5, (133.6, -22, 1.7), (133.6, -17, 1.7), (133.6, 10, 3.2), (133.6, 10, 3.2), 26, False, False),
        (6, (-110, -95, 140), (-60, -150, 140), (85, 135, 0), (85, 140, 0), 30, True, False),
        (3, (144, 18, 12), (142, 22, 10.5), (131, 33, 0), (131, 34, 0), 28, False, False),
        (10, (55, 35, 58), (110, 45, 58), (55, 125, 0), (110, 135, 0), 30, True, False),
        (6, (96, 62, 34), (120, 32, 26), (112, 26, 0), (133, 8, 0), 28, False, False),
        (5, (8, -30, 26), (78, -26, 24), (28, 20, 0), (95, 22, 0), 28, True, False),     # commercial strip, labels on
        (7, (124.9, 9.5, 2.2), (124.9, 22.5, 2.2), (113.4, 13, 2.6), (113.4, 27, 2.6), 26, False, False),
        (4, (126, 34, 1.8), (126, 44, 1.8), (100, 42, 0.6), (100, 50, 0.6), 24, False, False),  # pool
        (6, (40, 175, 48), (40, 195, 44), (18, 245, 0), (18, 262, 0), 30, True, False),
        (4, (62, 205, 62), (50, 212, 58), (16, 272, 0), (16, 274, 0), 30, True, False),        # 700 sqm
        (8, (110, -14, 1.7), (122, -14, 1.7), (116, 12, 2.5), (128, 12, 2.5), 26, False, False),
        (4, (146.5, -7, 2.2), (146.5, -7, 2.2), (135, 14, 3.0), (135, 14, 6.0), 24, False, False),  # lights & CCTV
        (7, (85, -80, 105), (85, -135, 150), (85, 140, 0), (85, 140, 0), 32, True, False),
        (3, (215, -95, 160), (205, -85, 150), (86, 132, 0), (86, 132, 0), 32, True, True),      # dusk
        (2, (133.6, -17, 1.7), (133.6, -17, 1.7), (133.6, 10, 3.2), (133.6, 10, 3.2), 26, False, False),
    ]
    for (sec, a0, a1, t0, t1, lens, lab, dusk) in S:
        n = int(sec * FPS * (0.78 if sec > 3 else 1.0))
        for k in range(n):
            u = ease(k / max(1, n - 1))
            frames.append((Vector(a0).lerp(Vector(a1), u), Vector(t0).lerp(Vector(t1), u), lens, lab, dusk))
N = len(frames); sc.frame_start, sc.frame_end = 1, N
if which == 'v2': open(f'{D}/v2_shots.txt', 'w').write(' '.join(str(int(x[0] * FPS * (0.78 if x[0] > 3 else 1.0))) for x in S))

# camera
cd = bpy.data.cameras.new("FilmCam"); cd.clip_start = 0.1; cd.clip_end = 6000
cam = bpy.data.objects.new("FilmCam", cd); sc.collection.objects.link(cam); sc.camera = cam
def place(f):
    loc, tgt, lens, lab, dusk = frames[f]
    cam.location = loc; cam.rotation_euler = (tgt - loc).to_track_quat('-Z', 'Y').to_euler(); cd.lens = lens
    cd.dof.use_dof = loc.z < 4; cd.dof.focus_distance = (tgt - loc).length; cd.dof.aperture_fstop = 5.6

# moving cars: only the arriving red car moves, and only on the IN lane (v2 shot 1 drives it away through the gate)
cars = [o for o in bpy.data.objects if o.name.startswith("Car") and o.instance_type == 'COLLECTION']
for o in cars:
    if o.animation_data: o.animation_data_clear()
# park every other car squarely on the expressway asphalt (one sat across the fence line)
P0, P1 = Vector((1.43, 15.36)), Vector((170.75, 0.0))
def y_edge(x): return P0.y + (x - P0.x) * (P1.y - P0.y) / (P1.x - P0.x)
for o in cars:
    if o.location.y < 3 and abs(o.location.x - 134) > 6:
        o.location.y = y_edge(o.location.x) - (5.0 if o.location.x < 134 else 8.5)
red = min(cars, key=lambda o: abs(o.location.x - 134) + abs(o.location.y - 4)) if cars else None
if red and which == "v2":
    p = red.location.copy()
    red.location = (p.x, -9.0, p.z); red.keyframe_insert("location", frame=1)
    red.location = (p.x, 26.0, p.z); red.keyframe_insert("location", frame=5 * FPS)
    red.location = (p.x, 26.0, p.z); red.keyframe_insert("location", frame=N)

# labels: only in high aerials
labels = list(bpy.data.collections["03_Labels"].all_objects)
bpy.data.collections["03_Labels"].hide_render = False
prev = None
for f in range(N):
    lab = frames[f][3]
    if lab != prev:
        for o in labels:
            o.hide_render = not lab; o.keyframe_insert("hide_render", frame=f + 1)
        prev = lab
# dusk shot: sky + exposure keys
sky = next(n for n in sc.world.node_tree.nodes if n.type == 'TEX_SKY'); base_el = sky.sun_elevation; base_ex = sc.view_settings.exposure
fill = bpy.data.objects.get("ShadowFill")
prev = None
for f in range(N):
    d = frames[f][4]
    if d != prev:
        sky.sun_elevation = math.radians(2.5) if d else base_el; sky.keyframe_insert("sun_elevation", frame=f + 1)
        sc.view_settings.exposure = base_ex + (1.6 if d else 0); sc.view_settings.keyframe_insert("exposure", frame=f + 1)
        if fill: fill.data.energy = 1.5 if d else 9.0; fill.data.keyframe_insert("energy", frame=f + 1)
        prev = d

if mode == "check":
    dg = bpy.context.evaluated_depsgraph_get(); bad = []
    dirs = [Vector(v) for v in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,0),(-1,1,0),(1,-1,0),(-1,-1,0))]
    for f in range(0, N, 6):
        sc.frame_set(f + 1); place(f); dg = bpy.context.evaluated_depsgraph_get()
        loc = cam.location.copy(); fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
        near = min([sc.ray_cast(dg, loc, d.normalized(), distance=2.0)[0] and 1 or 99 for d in dirs if not (d.z < 0 and loc.z < 3)])
        hit, p, n, i, ob, m = sc.ray_cast(dg, loc, fwd, distance=6.0)
        if near < 99 or hit:
            bad.append((f, round(loc.x, 1), round(loc.y, 1), round(loc.z, 1), ob.name if hit else "near<2m"))
    print("BAD", len(bad)); [print("  ", b) for b in bad[:40]]
elif mode == "sheet":
    sc.render.engine = 'CYCLES'; sc.render.use_persistent_data = True; sc.cycles.samples = 2; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 320, 180
    os.makedirs(f"{D}/sheet_{which}", exist_ok=True)
    for f in range(0, N, FPS):
        sc.frame_set(f + 1); place(f); sc.render.filepath = f"{D}/sheet_{which}/s_{f // FPS:03d}.png"; bpy.ops.render.render(write_still=True)
    print("SHEET_DONE", N)
else:
    sc.render.engine = 'CYCLES'; sc.render.use_persistent_data = True
    fast = len(sys.argv) > sys.argv.index("--") + 3
    sc.render.resolution_x, sc.render.resolution_y = (854, 480) if fast else (1280, 720); sc.cycles.samples = 3 if fast else 14; sc.cycles.adaptive_threshold = 0.05
    sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    out = f"{D}/film_{which}" + ("_480" if fast else "_hq"); os.makedirs(out, exist_ok=True)
    for f in range(N):
        p = f"{out}/f_{f + 1:04d}.png"
        if os.path.exists(p): continue
        sc.frame_set(f + 1); place(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME", f + 1, N, flush=True)
    print("FILM_DONE", which, flush=True)
