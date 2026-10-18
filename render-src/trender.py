import bpy, sys, time, os
a = sys.argv[sys.argv.index("--") + 1:]
W, H, S, labels = int(a[0]), int(a[1]), int(a[2]), a[3] == "1"
bpy.ops.wm.open_mainfile(filepath="/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2/epe.blend")
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = W, H; sc.cycles.samples = S
sc.render.use_persistent_data = True
for c in bpy.data.collections:
    if c.name == "03_Labels": c.hide_render = not labels
for cam in a[4:]:
    t = time.time(); sc.camera = bpy.data.objects[cam]
    sc.render.filepath = f"/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2/dbg/{cam}.png"
    bpy.ops.render.render(write_still=True); print("DONE", cam, round(time.time() - t), flush=True)
