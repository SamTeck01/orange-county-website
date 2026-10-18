import bpy, sys, math
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath="epe.blend"); sc = bpy.context.scene
sky = next(n for n in sc.world.node_tree.nodes if n.type == 'TEX_SKY'); bg = next(n for n in sc.world.node_tree.nodes if n.type == 'BACKGROUND')
sky.sun_rotation = math.radians(float(a[0])); bg.inputs["Strength"].default_value = float(a[1]); sc.view_settings.exposure = float(a[2])
sc.camera = bpy.data.objects["Aerial_Hero"]; sc.render.resolution_x, sc.render.resolution_y = 640, 360; sc.cycles.samples = 8
sc.render.filepath = f"dbg/sky_{a[0]}_{a[1]}_{a[2]}.png"; bpy.ops.render.render(write_still=True)
