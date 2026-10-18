# Web model: realise instances, drop heavy decor, flatten materials to plain colours, decimate, export GLB.
import bpy, sys, os, math
bpy.ops.wm.open_mainfile(filepath="epe.blend")
OUT = sys.argv[sys.argv.index("--") + 1]
DROP = ("08_People",)
for c in list(bpy.data.collections):
    if c.name in DROP:
        for o in list(c.all_objects): bpy.data.objects.remove(o, do_unlink=True)
# drop far scenery: keep only things within 120 m of the estate centre (plus everything that is not vegetation)
for o in list(bpy.data.objects):
    if o.type in ('CAMERA', 'LIGHT'): bpy.data.objects.remove(o, do_unlink=True); continue
    if o.name == "Terrain": bpy.data.objects.remove(o, do_unlink=True); continue
    x, y = o.matrix_world.translation.x, o.matrix_world.translation.y
    if o.instance_type == 'COLLECTION' and o.name.startswith("I_") and math.hypot(x - 85, y - 140) > 190:
        bpy.data.objects.remove(o, do_unlink=True)
    elif o.name.startswith("Car") and o.instance_type == 'COLLECTION':
        bpy.data.objects.remove(o, do_unlink=True)
    elif o.instance_type == 'COLLECTION' and o.instance_collection and any(k in o.instance_collection.name for k in ("tree", "shrub", "grass", "flower", "conifer", "potted", "plant")):
        bpy.data.objects.remove(o, do_unlink=True)
vl = bpy.context.view_layer
bpy.context.view_layer.update()
for o in bpy.context.scene.objects: o.select_set(o.instance_type == "COLLECTION")
vl.objects.active = next((o for o in bpy.context.scene.objects if o.select_get()), None)
if vl.objects.active: bpy.ops.object.duplicates_make_real()
for o in list(vl.objects):
    if o.type in ('FONT', 'CURVE'):
        for s in vl.objects: s.select_set(False)
        o.select_set(True); vl.objects.active = o
        try: bpy.ops.object.convert(target='MESH')
        except Exception: pass
# ground plane to replace the huge terrain
bpy.ops.mesh.primitive_plane_add(size=520, location=(85, 140, -0.06)); g = bpy.context.object; g.name = "Ground"
COL = {"Lawn": (0.25, 0.45, 0.15), "Wild_Ground": (0.10, 0.19, 0.06), "Asphalt": (0.20, 0.21, 0.24), "Pavers": (0.62, 0.62, 0.60),
       "Curb": (0.72, 0.72, 0.70), "Plaster_White": (0.90, 0.89, 0.86), "Plaster_Cream": (0.85, 0.78, 0.65), "Wood_Deck": (0.55, 0.40, 0.28),
       "Pool_Tile": (0.20, 0.55, 0.75), "Wood_Clad": (0.45, 0.32, 0.22), "Concrete_Panel": (0.42, 0.42, 0.43), "Patio": (0.75, 0.72, 0.66),
       "Laterite": (0.60, 0.32, 0.18), "Turf": (0.20, 0.50, 0.18), "Lawn_Light": (0.26, 0.50, 0.19), "Lawn_Deep": (0.12, 0.29, 0.08),
       "Sign_Panel": (0.92, 0.90, 0.86), "Stone_Clad": (0.55, 0.50, 0.43), "Flower_Hedge": (0.05, 0.17, 0.04)}
cache = {}
def simple(m):
    if m is None: return None
    if m.name in cache: return cache[m.name]
    key = next((k for k in COL if m.name.startswith(k)), None)
    bs = m.node_tree.nodes.get("Principled BSDF") if m.use_nodes and m.node_tree else None
    if key: rgb = COL[key]
    elif "water" in m.name.lower(): rgb = (0.12, 0.55, 0.72)
    elif bs and not bs.inputs["Base Color"].is_linked: rgb = tuple(bs.inputs["Base Color"].default_value[:3])
    else: rgb = (0.30, 0.42, 0.20) if ("leaf" in m.name.lower() or "palm" in m.name.lower()) else (0.6, 0.6, 0.6)
    n = bpy.data.materials.new("W_" + m.name[:40]); n.use_nodes = True; b = n.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = 0.8
    if bs:
        b.inputs["Metallic"].default_value = min(0.6, bs.inputs["Metallic"].default_value)
        em = bs.inputs.get("Emission Strength")
        if em and em.default_value > 0.5 and not bs.inputs["Emission Color"].is_linked:
            b.inputs["Emission Color"].default_value = bs.inputs["Emission Color"].default_value; b.inputs["Emission Strength"].default_value = 1.0
    cache[m.name] = n; return n
gm = bpy.data.materials.new("W_Ground"); gm.use_nodes = True; gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.10, 0.19, 0.06, 1)
g.data.materials.append(gm)
tris = 0
done = set()
dg = bpy.context.evaluated_depsgraph_get()
for o in list(bpy.context.scene.objects):
    if o.type != 'MESH' or o.data.name in done: continue
    me = o.data; done.add(me.name)
    for i, sl in enumerate(me.materials): me.materials[i] = simple(sl)
    n = len(me.polygons)
    if n > 2500:
        t = bpy.data.objects.new("tmp_dec", me); bpy.context.scene.collection.objects.link(t)
        d = t.modifiers.new("dec", 'DECIMATE'); d.ratio = max(0.04, 2500 / n)
        dg = bpy.context.evaluated_depsgraph_get(); new = bpy.data.meshes.new_from_object(t.evaluated_get(dg))
        bpy.data.objects.remove(t, do_unlink=True)
        me.user_remap(new); done.add(new.name); n = len(new.polygons)
    tris += n
print("objects", len(vl.objects), "faces before", tris, flush=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', use_visible=True, export_apply=True, export_materials='EXPORT',
                          export_image_format='NONE', export_yup=True, export_draco_mesh_compression_enable=False)
print("SIZE_MB", round(os.path.getsize(OUT) / 1e6, 1), flush=True)
