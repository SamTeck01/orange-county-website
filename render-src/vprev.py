import bpy, sys
bpy.ops.wm.open_mainfile(filepath="/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2/epe.blend")
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 640, 360; sc.cycles.samples = 12; sc.render.use_persistent_data = True
sc.camera = bpy.data.objects["Video_Cam"]
for f in (1, 50, 90, 130, 170, 240):
    sc.frame_set(f); sc.render.filepath = f"/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2/dbg/v_{f:03d}.png"; bpy.ops.render.render(write_still=True)
