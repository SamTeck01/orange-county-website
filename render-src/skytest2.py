import bpy, sys, math
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath="epe.blend"); sc = bpy.context.scene
sky = next(n for n in sc.world.node_tree.nodes if n.type == 'TEX_SKY')
sky.sun_rotation = math.radians(float(a[0]))
sc.render.resolution_x, sc.render.resolution_y = 480, 270; sc.cycles.samples = 8
for cam in a[1:]:
    sc.camera = bpy.data.objects[cam]; sc.render.filepath = f"dbg/s2_{a[0]}_{cam}.png"; bpy.ops.render.render(write_still=True)
