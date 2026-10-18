import bpy, sys
from mathutils import Vector
A = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/assets/dl/OC Epe assets"
FILES = {
 "maple": ("blend", A + "/Fab/Freeman_Maple/blender/AV Acer X freemanii Freeman.blend"),
 "beech": ("fbx", A + "/Fab/Beech/fbx/FBX/Beech Tree.fbx"),
 "hptree": ("fbx", A + "/Fab/HighPoly_Tree/highpoly_tree_model/HighPoly Tree Model/Model/SM_HP_Tree.FBX"),
 "pines": ("fbx", A + "/Fab/Pine_Tree_Trio/pine-tree-trio-free-download/source/PineTreeTrio.fbx"),
 "palm": ("fbx", A + "/Fab/Realistic_Palm/palm_hp_4/Palm_4_1.fbx"),
 "alex": ("fbx", A + "/Fab/Alexandra_Palm/alexandra_palm_ukgkcilia_high/Alexandra_Palm_ukgkcilia_High_ukgkcilia_VarA_LOD0.fbx"),
 "spindle": ("fbx", A + "/Fab/European_Spindle_hedge/european_spindle_wk1ncbxja_high/European_Spindle_wk1ncbxja_High_wk1ncbxja_VarA_LOD0.fbx"),
 "grass": ("fbx", A + "/Fab/Wild_Grass/wild_grass_vczndjqja_high/Wild_Grass_vczndjqja_High_vczndjqja_VarC_LOD0.fbx"),
 "camry": ("gltf", A + "/Sketchfab_cars/Toyota_Camry_2020_gltf/scene.gltf"),
 "corolla": ("gltf", A + "/Sketchfab_cars/Toyota_Corolla_2020_gltf/scene.gltf"),
 "lexus": ("gltf", A + "/Sketchfab_cars/Lexus_RX350_MK2_2003-2008_gltf/scene.gltf"),
 "rp178": ("fbx", A + "/Renderpeople/rp_posed_00178_29_FBX/rp_posed_00178_29.fbx"),
}
for k, (kind, f) in FILES.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        if kind == "fbx": bpy.ops.import_scene.fbx(filepath=f)
        elif kind == "gltf": bpy.ops.import_scene.gltf(filepath=f)
        else:
            with bpy.data.libraries.load(f) as (src, dst): dst.objects = src.objects
            for o in dst.objects:
                if o: bpy.context.scene.collection.objects.link(o)
    except Exception as e:
        print("ASSET", k, "FAIL", e); continue
    ms = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3); polys = 0
    for o in ms:
        polys += len(o.data.polygons)
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    mats = {}
    for o in ms:
        for s in o.material_slots:
            m = s.material
            if m and m.name not in mats:
                imgs = [n.image.name + ("" if n.image.has_data or n.image.filepath and __import__("os").path.exists(bpy.path.abspath(n.image.filepath)) else "(MISSING)") for n in (m.node_tree.nodes if m.use_nodes else []) if n.type == 'TEX_IMAGE' and n.image]
                mats[m.name] = imgs
    print("ASSET", k, "objs", len(ms), "polys", polys, "size", [round(v, 2) for v in (mx - mn)], "zmin", round(mn.z, 2))
    for m, imgs in mats.items(): print("   MAT", m, imgs[:4])
