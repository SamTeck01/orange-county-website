import bpy, math, sys
bpy.ops.wm.open_mainfile(filepath="lib2.blend"); sc = bpy.context.scene
names = [c.name for c in bpy.data.collections]
for c in list(sc.collection.children): sc.collection.children.unlink(c)
groups = [[n for n in names if n.startswith(p)] for p in ("T_", "P_", "H_", "G_", "C_", "RP_")]
y = 0
for row in groups:
    x = 0
    for n in row:
        c = bpy.data.collections[n]; e = bpy.data.objects.new("I" + n, None); e.instance_type = 'COLLECTION'; e.instance_collection = c
        big = n.startswith(("T_", "P_"))
        e.location = (x, y, 0); sc.collection.objects.link(e)
        x += 22 if n.startswith("T_pines") else (14 if big else 6)
    y += 16 if row and row[0].startswith(("T_", "P_")) else 7
bpy.ops.mesh.primitive_plane_add(size=400, location=(40, 30, 0))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[1].default_value = 0.8
sun = bpy.data.objects.new("s", bpy.data.lights.new("s", "SUN")); sun.data.energy = 4; sun.rotation_euler = (0.9, 0.1, 0.5); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (35, -45, 38); cam.rotation_euler = (math.radians(58), 0, 0); cam.data.lens = 24
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.render.resolution_x, sc.render.resolution_y = 1600, 900
sc.render.filepath = "dbg/lib2.png"; bpy.ops.render.render(write_still=True)
