import bpy, math, sys
mode = sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath="lib2.blend"); sc = bpy.context.scene
for c in list(sc.collection.children): sc.collection.children.unlink(c)
m = bpy.data.materials["H_spindle_VarA_Mat"]; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
if mode in ("noalpha", "nonorm"):
    for l in list(b.inputs["Alpha"].links): nt.links.remove(l)
if mode == "nonorm":
    for l in list(b.inputs["Normal"].links): nt.links.remove(l)
e = bpy.data.objects.new("I", None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections["H_spindle_VarA"]; sc.collection.objects.link(e)
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.6, 0.7, 0.9, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sun = bpy.data.objects.new("s", bpy.data.lights.new("s", "SUN")); sun.data.energy = 4; sun.rotation_euler = (0.9, 0.1, -0.4); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, -3.2, 0.8); cam.rotation_euler = (math.radians(88), 0, 0); cam.data.lens = 35
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.render.resolution_x, sc.render.resolution_y = 500, 500
sc.render.filepath = f"dbg/sp_{mode}.png"; bpy.ops.render.render(write_still=True)
