import bpy, math, sys
flip = sys.argv[-1] == "flip"
bpy.ops.wm.open_mainfile(filepath="lib2.blend"); sc = bpy.context.scene
for c in list(sc.collection.children): sc.collection.children.unlink(c)
for mn in ("H_spindle_VarA_Mat", "P_alex_VarA_Mat"):
    m = bpy.data.materials[mn]; nt = m.node_tree
    if flip:
        uv = nt.nodes.new("ShaderNodeUVMap"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); com = nt.nodes.new("ShaderNodeCombineXYZ"); inv = nt.nodes.new("ShaderNodeMath"); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
        nt.links.new(uv.outputs["UV"], sep.inputs[0]); nt.links.new(sep.outputs[0], com.inputs[0]); nt.links.new(sep.outputs[1], inv.inputs[1]); nt.links.new(inv.outputs[0], com.inputs[1])
        for n in nt.nodes:
            if n.type == 'TEX_IMAGE': nt.links.new(com.outputs[0], n.inputs["Vector"])
for i, n in enumerate(("H_spindle_VarA", "P_alex_VarA")):
    e = bpy.data.objects.new("I" + n, None); e.instance_type = 'COLLECTION'; e.instance_collection = bpy.data.collections[n]; e.location = (i * 3.5, 0, 0); sc.collection.objects.link(e)
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.6, 0.7, 0.9, 1)
sun = bpy.data.objects.new("s", bpy.data.lights.new("s", "SUN")); sun.data.energy = 4; sun.rotation_euler = (0.9, 0.1, -0.4); sc.collection.objects.link(sun)
cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (1.75, -6, 1.6); cam.rotation_euler = (math.radians(85), 0, 0); cam.data.lens = 35
sc.render.engine = 'CYCLES'; sc.cycles.samples = 16; sc.render.resolution_x, sc.render.resolution_y = 600, 400
sc.render.filepath = f"dbg/fl_{sys.argv[-1]}.png"; bpy.ops.render.render(write_still=True)
