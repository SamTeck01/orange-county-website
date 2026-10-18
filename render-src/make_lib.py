# Import every Poly Haven model once into its own collection, report size/polys, save as an asset library.
import bpy, os, glob
from mathutils import Vector
A = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/assets/ph/models"
bpy.ops.wm.read_factory_settings(use_empty=True)
lib = bpy.data.collections.new("LIB"); bpy.context.scene.collection.children.link(lib)
for d in sorted(glob.glob(A + "/*/")):
    name = os.path.basename(d.rstrip("/")); g = glob.glob(d + "*.gltf")
    if not g: continue
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=g[0])
    new = [o for o in bpy.data.objects if o not in before]
    col = bpy.data.collections.new(name); lib.children.link(col)
    for o in new:
        for c in o.users_collection: c.objects.unlink(o)
        col.objects.link(o)
    pts = [o.matrix_world @ Vector(c) for o in new if o.type == 'MESH' for c in o.bound_box]
    tris = sum(len(o.data.polygons) for o in new if o.type == 'MESH')
    if pts:
        mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))); mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        print(f"LIB {name:28s} objs {len(new):3d} polys {tris:8d} size {tuple(round(v,2) for v in (mx-mn))} minz {mn.z:.2f}", flush=True)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("lib.blend"))
