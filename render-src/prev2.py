import bpy, math
bpy.ops.wm.open_mainfile(filepath="lib2.blend"); sc = bpy.context.scene
for c in list(sc.collection.children): sc.collection.children.unlink(c)
for i, n in enumerate(("P_alex_VarA", "H_spindle_VarA", "G_grass_VarD", "C_camry", "RP_mei")):
    e = bpy.data.objects.new("I" + n, None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections[n]; e.location = (i * 5.5, 0, 0); sc.collection.objects.link(e)
bpy.ops.mesh.primitive_plane_add(size=100)
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[1].default_value = 0.8
sun = bpy.data.objects.new("s", bpy.data.lights.new("s", "SUN")); sun.data.energy = 4; sun.rotation_euler = (0.9, 0.1, 0.5); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (11, -16, 4); cam.rotation_euler = (math.radians(80), 0, 0); cam.data.lens = 28
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.render.resolution_x, sc.render.resolution_y = 1200, 600
sc.render.filepath = "dbg/lib2b.png"; bpy.ops.render.render(write_still=True)
