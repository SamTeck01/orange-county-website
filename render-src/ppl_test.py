import bpy, math
from mathutils import Vector
RB = "/home/user/rb/repo/Assets"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=f"{RB}/Avatars/Adults/Male_Adult_04/Export/Male_Adult_04.fbx")
objs = list(bpy.data.objects)
arm = next(o for o in objs if o.type == 'ARMATURE')
print("avatar objs", [(o.name, o.type) for o in objs][:8], "arm scale", tuple(arm.scale), "dims", tuple(round(v, 2) for v in arm.dimensions))
meshes = [o for o in objs if o.type == 'MESH']
for m in meshes:
    print("mesh", m.name, len(m.data.polygons), [ (s.material.name if s.material else None) for s in m.material_slots])
    for s in m.material_slots:
        if s.material and s.material.use_nodes:
            print("   tex", [n.image.name for n in s.material.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image])
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=f"{RB}/Animations/all_animations_max_motextr_xy/m_walk_neutral_01.max.fbx")
new = [o for o in bpy.data.objects if o not in before]
a2 = next(o for o in new if o.type == 'ARMATURE')
act = a2.animation_data.action if a2.animation_data else None
print("anim arm", a2.name, "action", act.name if act else None, "range", tuple(act.frame_range) if act else None)
print("bones match", len(set(b.name for b in arm.data.bones) & set(b.name for b in a2.data.bones)), "of", len(arm.data.bones))
