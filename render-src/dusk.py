import bpy, sys, math
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath="epe.blend"); sc = bpy.context.scene
sky = next(n for n in sc.world.node_tree.nodes if n.type == 'TEX_SKY')
sky.sun_elevation = math.radians(float(a[0])); sc.view_settings.exposure = float(a[1])
sc.render.resolution_x, sc.render.resolution_y = 700, 394; sc.cycles.samples = 12
for cam, lab in (("Aerial_Hero", False), ("Gate_Front", True)):
    bpy.data.collections["03_Labels"].hide_render = lab
    sc.camera = bpy.data.objects[cam]; sc.render.filepath = f"dbg/d_{a[0]}_{a[1]}_{cam}.png"; bpy.ops.render.render(write_still=True)
