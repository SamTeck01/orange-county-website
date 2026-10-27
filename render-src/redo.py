import bpy, math
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath="epe.blend"); sc = bpy.context.scene
sc.frame_set(1); sc.render.use_motion_blur = False
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.cycles.samples = 32; sc.cycles.adaptive_threshold = 0.02
bpy.data.collections["03_Labels"].hide_render = True
sc.camera = bpy.data.objects["Commercial_Strip"]; sc.render.filepath = "web2/14_Commercial_Plots_v2.png"; bpy.ops.render.render(write_still=True)
cd = bpy.data.cameras.new("LC"); cd.lens = 24; o = bpy.data.objects.new("LC", cd); sc.collection.objects.link(o)
o.location = (146.5, -7.0, 2.2); o.rotation_euler = (Vector((135.0, 14.0, 4.2)) - o.location).to_track_quat('-Z', 'Y').to_euler()
sc.camera = o; sc.render.filepath = "web2/15_Street_Lights_CCTV_v2.png"; bpy.ops.render.render(write_still=True)
print("REDO_DONE")
