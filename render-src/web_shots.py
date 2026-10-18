import bpy, math
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath="epe.blend"); sc = bpy.context.scene
sc.frame_set(1); sc.render.use_motion_blur = False
sc.render.resolution_x, sc.render.resolution_y = 1600, 900; sc.cycles.samples = 20; sc.cycles.adaptive_threshold = 0.03
sc.render.image_settings.file_format = 'PNG'
lab = bpy.data.collections["03_Labels"]
def cam(name, loc, tgt, lens, fstop=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_start = 0.05; cd.clip_end = 3000
    o = bpy.data.objects.new(name, cd); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    if fstop: cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop; cd.dof.focus_distance = (Vector(tgt) - Vector(loc)).length
    return o
# CCTV on the gatehouse corner
c = [o for o in bpy.data.objects if o.name.startswith("CCTV") or "security_camera" in o.name.lower()]
cc = min(c, key=lambda o: (o.matrix_world.translation - Vector((139.8, 3.0, 3.5))).length).matrix_world.translation if c else Vector((139.8, 3.0, 3.6))
# a solar street light inside the estate
sl = [o for o in bpy.data.objects if o.name.startswith("SolarLight")]
s = min(sl, key=lambda o: (o.matrix_world.translation - Vector((128, 90, 0))).length).matrix_world.translation
SHOTS = [
 ("feature-cctv", cam("W_cctv", cc + Vector((1.6, -2.2, -0.35)), cc, 40, 2.8), False),
 ("feature-solar", cam("W_solar", s + Vector((-5.5, -7.0, 2.2)), s + Vector((0.6, 0, 6.2)), 30, 5.6), False),
 ("feature-road", cam("W_road", (133.0, 70.0, 1.6), (133.5, 180.0, 1.2), 32, 16), False),
 ("facility-gym", cam("W_gym", (107.4, 0.5, 1.9), (107.4, 12.0, 3.2), 26, 11), False),
 ("facility-pitch", cam("W_pitch", (118.0, 66.0, 6.0), (108.0, 54.0, 0.5), 26), False),
 ("facility-drainage", cam("W_drain", (131.2, 50.0, 0.9), (131.0, 90.0, 0.2), 28, 8), False),
 ("commercial-plots", bpy.data.objects["Commercial_Strip"], True),
]
import os
for name, c_, labels in SHOTS:
    if os.path.exists(f"web/{name}.png"): continue
    lab.hide_render = not labels; sc.camera = c_
    sc.render.filepath = f"web/{name}.png"; bpy.ops.render.render(write_still=True); print("SHOT", name, flush=True)
