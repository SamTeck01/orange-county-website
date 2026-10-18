# Imports the downloaded Fab / Sketchfab / Renderpeople assets, repairs their materials,
# normalises size and pivot (base centred at the origin, metres) and saves one collection each to lib2.blend.
import bpy, os, glob, math
from mathutils import Vector
A = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/assets/dl/OC Epe assets"
OUT = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2/lib2.blend"
bpy.ops.wm.read_factory_settings(use_empty=True)

def img(path, data=False):
    if not path or not os.path.exists(path): return None
    im = bpy.data.images.load(path, check_existing=True)
    if data: im.colorspace_settings.name = 'Non-Color'
    return im

def find(folder, *keys, exclude=("Billboard", "LOD")):
    for f in sorted(glob.glob(folder + "/**/*", recursive=True)):
        b = os.path.basename(f).lower()
        if all(k.lower() in b for k in keys) and not any(e.lower() in b for e in exclude) and b.rsplit(".", 1)[-1] in ("png", "jpg", "jpeg", "tga", "tif", "exr"):
            return f
    return None

def pbr_mat(name, color=None, opacity=None, normal=None, rough=None, gloss=None, transl=None, leaf=False):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    def tex(p, data=False):
        i = img(p, data)
        if not i: return None
        n = nt.nodes.new("ShaderNodeTexImage"); n.image = i; return n
    c = tex(color)
    if c:
        if leaf:
            hs = nt.nodes.new("ShaderNodeHueSaturation"); hs.inputs["Saturation"].default_value = 1.1; hs.inputs["Value"].default_value = 1.0
            nt.links.new(c.outputs["Color"], hs.inputs["Color"]); nt.links.new(hs.outputs["Color"], b.inputs["Base Color"])
        else:
            nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
        if opacity is None and leaf and c.image and c.image.depth == 32:
            nt.links.new(c.outputs["Alpha"], b.inputs["Alpha"])
    o = tex(opacity, True)
    if o:
        # Megascans masks are soft; a hard cut keeps leaves solid instead of ghostly
        th = nt.nodes.new("ShaderNodeMath"); th.operation = 'GREATER_THAN'; th.inputs[1].default_value = 0.12
        nt.links.new(o.outputs["Color"], th.inputs[0]); nt.links.new(th.outputs[0], b.inputs["Alpha"])
    nrm = tex(normal, True)
    if nrm:
        nm = nt.nodes.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = 0.8
        nt.links.new(nrm.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    r = tex(rough, True)
    if r: nt.links.new(r.outputs["Color"], b.inputs["Roughness"])
    else:
        g = tex(gloss, True)
        if g:
            inv = nt.nodes.new("ShaderNodeInvert"); nt.links.new(g.outputs["Color"], inv.inputs["Color"]); nt.links.new(inv.outputs["Color"], b.inputs["Roughness"])
        else: b.inputs["Roughness"].default_value = 0.6 if leaf else 0.8
    if leaf:
        b.inputs["Subsurface Weight"].default_value = 0.0
        try:
            b.inputs["Transmission Weight"].default_value = 0.0
            b.inputs["Diffuse Roughness"].default_value = 0.5
        except Exception: pass
        b.inputs["Specular IOR Level"].default_value = 0.3
    return m

def load(kind, path):
    before = set(bpy.data.objects)
    if kind == "fbx": bpy.ops.import_scene.fbx(filepath=path)
    elif kind == "gltf": bpy.ops.import_scene.gltf(filepath=path)
    else:
        with bpy.data.libraries.load(path) as (src, dst): dst.objects = [n for n in src.objects]
        for o in dst.objects:
            if o and o.type in ('MESH', 'EMPTY'): bpy.context.scene.collection.objects.link(o)
    return [o for o in bpy.data.objects if o not in before]

def finish(name, objs, height=None, length=None):
    """Bake transforms, drop non-meshes, scale to a real-world size, base-centre at origin, store in a collection."""
    meshes = [o for o in objs if o.type == 'MESH']
    for o in objs:
        if o.type != 'MESH':
            for ch in o.children: ch.matrix_parent_inverse = o.matrix_world.inverted() @ ch.matrix_parent_inverse if False else ch.matrix_parent_inverse
    for o in meshes:
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
    for o in objs:
        if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
    for o in meshes:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c); mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    size = mx - mn
    s = height / size.z if height else (length / max(size.x, size.y) if length else 1.0)
    base = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    col = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(col)
    for o in meshes:
        o.matrix_world.translation -= base
        o.matrix_world = __import__("mathutils").Matrix.Scale(s, 4) @ o.matrix_world
        for c in list(o.users_collection): c.objects.unlink(o)
        col.objects.link(o)
    print("LIB", name, "objs", len(meshes), "polys", sum(len(o.data.polygons) for o in meshes), "size", [round(v * s, 2) for v in size], flush=True)
    return col

FAB = A + "/Fab"
# --- trees
o = load("blend", FAB + "/Freeman_Maple/blender/AV Acer X freemanii Freeman.blend"); finish("T_maple", o, height=4.5)
d = FAB + "/Beech"; o = load("fbx", d + "/fbx/FBX/Beech Tree.fbx")
for x in o:
    if x.type != 'MESH': continue
    for sl in x.material_slots:
        if sl.material and "Leaves" in sl.material.name:
            sl.material = pbr_mat("Beech_Leaves", find(d, "Beech_Leaves", "Base_color"), find(d, "Beech_Leaves", "Opacity"), find(d, "Beech_Leaves", "Normal"), find(d, "Beech_Leaves", "Roughness"), leaf=True)
        elif sl.material:
            sl.material = pbr_mat("Beech_Trunk", find(d, "Beech_Trunk", "Base_color"), None, find(d, "Beech_Trunk", "Normal"), find(d, "Beech_Trunk", "Roughness"))
finish("T_beech", o, height=4.3)
d = FAB + "/HighPoly_Tree"; o = load("fbx", d + "/highpoly_tree_model/HighPoly Tree Model/Model/SM_HP_Tree.FBX")
for x in o:
    if x.type != 'MESH': continue
    for sl in x.material_slots:
        if not sl.material: continue
        if "Leaf" in sl.material.name: sl.material = pbr_mat("HP_Leaf", find(d, "T_HP_Tree_Leaf"), leaf=True)
        else: sl.material = pbr_mat("HP_Trunk", find(d, "T_HP_Tree_Trunk.", ), None, find(d, "T_HP_Tree_Trunk_normal"))
finish("T_hp", o, height=4.6)
d = FAB + "/Pine_Tree_Trio"; o = load("fbx", d + "/pine-tree-trio-free-download/source/PineTreeTrio.fbx")
pm = pbr_mat("Pine", find(d, "NewTree"), leaf=True)
for x in o:
    if x.type == 'MESH':
        for sl in x.material_slots: sl.material = pm
finish("T_pines", o, height=4.8)
# --- palms
d = FAB + "/Realistic_Palm"; o = load("fbx", d + "/palm_hp_4/Palm_4_1.fbx")
for x in o:
    if x.type != 'MESH': continue
    for sl in x.material_slots:
        if not sl.material: continue
        if "Leaf" in sl.material.name: sl.material = pbr_mat("Palm_Leaf", find(d, "Leaf_Atlas"), leaf=True)
        else: sl.material = pbr_mat("Palm_Trunk", find(d, "Trunk_Atlas."), None, find(d, "Trunk_Atlas_Normal"))
finish("P_palm", o, height=9.5)
def megascan(folder, var, name, height):
    f = glob.glob(folder + f"/*{var}_LOD0.fbx")[0]; o = load("fbx", f)
    m = pbr_mat(name + "_Mat", find(folder, "BaseColor"), find(folder, "Opacity"), find(folder, "Normal"), find(folder, "Roughness"), find(folder, "Gloss"), leaf=True)
    for x in o:
        if x.type == 'MESH':
            for sl in x.material_slots: sl.material = m
            if not x.material_slots: x.data.materials.append(m)
    return finish(name, o, height=height)
d = glob.glob(FAB + "/Alexandra_Palm/*")[0]
for v in ("VarA", "VarB", "VarC", "VarD"): megascan(d, v, "P_alex_" + v, 3.2)
d = glob.glob(FAB + "/European_Spindle_hedge/*")[0]
for v in ("VarA", "VarF", "VarH"): megascan(d, v, "H_spindle_" + v, 1.3)
d = glob.glob(FAB + "/Wild_Grass/*")[0]
for v in ("VarC", "VarD", "VarE", "VarG"): megascan(d, v, "G_grass_" + v, 0.45)
# --- cars (front faces -Y in these files; length ~4.6 m)
for nm, f, L in (("C_camry", "Toyota_Camry_2020_gltf", 4.89), ("C_corolla", "Toyota_Corolla_2020_gltf", 4.63), ("C_lexus", "Lexus_RX350_MK2_2003-2008_gltf", 4.73)):
    o = load("gltf", A + f"/Sketchfab_cars/{f}/scene.gltf"); finish(nm, o, length=L)
# --- photoreal people (Renderpeople, posed)
R = A + "/Renderpeople"
for nm, f in (("RP_mei", "renderpeople_free_posed_people_BLD/rp_mei_posed_001_BLD/rp_mei_posed_001_100k.blend"),
              ("RP_fabienne", "renderpeople_free_posed_people_BLD/rp_fabienne_percy_posed_001_BLD/rp_fabienne_percy_posed_001_200k.blend"),
              ("RP_dennis", "renderpeople_free_posed_people_BLD/rp_dennis_posed_004_BLD/rp_dennis_posed_004_100k.blend")):
    o = load("blend", R + "/" + f)
    from mathutils import Matrix
    for x in o:
        if x.type == 'MESH' and x.parent is None: x.matrix_world = Matrix.Rotation(math.radians(90), 4, 'X') @ x.matrix_world   # stored Y-up
    finish(nm, o, height=1.72 if nm != "RP_dennis" else 1.80)
o = load("fbx", R + "/rp_posed_00178_29_FBX/rp_posed_00178_29.fbx")
d = R + "/rp_posed_00178_29_FBX"
m = pbr_mat("RP178", find(d, "basecolor", exclude=()), None, find(d, "normals", exclude=()), find(d, "roughness", exclude=()))
for x in o:
    if x.type == 'MESH':
        for sl in x.material_slots: sl.material = m
finish("RP_178", o, height=1.75)
for c in bpy.data.collections: c.use_fake_user = True
bpy.ops.file.pack_all() if False else None
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("LIB2 SAVED", flush=True)
