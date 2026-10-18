# Runs inside build.py (shares its globals).
# ============================================================================= ASSET LIBRARY (Poly Haven, CC0)
WANT = ["island_tree_01", "island_tree_02", "island_tree_03", "tree_small_02", "pachira_aquatica_01", "shrub_01", "shrub_02",
        "shrub_03", "shrub_04", "flower_gazania", "flower_ursinia", "periwinkle_plant", "grass_medium_01", "grass_medium_02",
        "planter_box_01", "potted_plant_01", "potted_plant_02", "security_camera_01", "outdoor_table_chair_set_01",
        "modular_street_seating", "boulder_01"]
with bpy.data.libraries.load(LIB, link=False) as (src, dst):
    dst.collections = [c for c in src.collections if c in WANT]
ASSET = {c.name: c for c in bpy.data.collections if c.name in WANT}
# recentre every asset collection on its footprint so instances land where we place them
for c in ASSET.values():
    pts = [o.matrix_world @ Vector(v) for o in c.all_objects if o.type == 'MESH' for v in o.bound_box]
    if pts:
        c.instance_offset = (sum(p.x for p in pts) / len(pts), sum(p.y for p in pts) / len(pts), min(p.z for p in pts))
# per-object variants (flower / grass sets are several plants laid out in a row)
def variants(name):
    out = []
    for o in ASSET[name].objects:
        if o.type != 'MESH' or o.parent: continue
        vc = bpy.data.collections.new(f"{name}__{o.name}"); vc.objects.link(o) if o.name not in vc.objects else None
        bb = [Vector(v) for v in o.bound_box]; vc.instance_offset = o.matrix_world @ Vector(((min(v.x for v in bb) + max(v.x for v in bb)) / 2, (min(v.y for v in bb) + max(v.y for v in bb)) / 2, min(v.z for v in bb)))
        out.append(vc)
    return out or [ASSET[name]]
FLOWERS = variants("flower_gazania") + variants("flower_ursinia") + variants("periwinkle_plant")
GRASS = variants("grass_medium_01") + variants("grass_medium_02")
SHRUBS = variants("shrub_02") + variants("shrub_03") + variants("shrub_01")
# flame-tree variant: island tree with orange canopy (the warm accents of the Oyo renders)
def tinted(src_name, new_name, rgb):
    nc = bpy.data.collections.new(new_name)
    for o in ASSET[src_name].objects:
        n = o.copy(); nc.objects.link(n)
        for i, slot in enumerate(n.material_slots):
            if slot.material and "leaves" in slot.material.name:
                m2 = slot.material.copy(); m2.name = slot.material.name + "_" + new_name
                bs = m2.node_tree.nodes.get("Principled BSDF")
                if bs and bs.inputs["Base Color"].links:
                    lk = bs.inputs["Base Color"].links[0]; hs = m2.node_tree.nodes.new("ShaderNodeHueSaturation")
                    hs.inputs["Hue"].default_value = rgb[0]; hs.inputs["Saturation"].default_value = rgb[1]; hs.inputs["Value"].default_value = rgb[2]
                    m2.node_tree.links.new(lk.from_socket, hs.inputs["Color"]); m2.node_tree.links.new(hs.outputs["Color"], bs.inputs["Base Color"])
                slot.link = 'OBJECT'; slot.material = m2
    nc.instance_offset = ASSET[src_name].instance_offset
    ASSET[new_name] = nc
tinted("island_tree_02", "flame_tree", (0.39, 1.5, 1.25))
tinted("island_tree_01", "gold_tree", (0.42, 1.4, 1.2))
# ---- downloaded library (Fab / Megascans trees, palms, shrubs, grass; Sketchfab cars; Renderpeople people)
with bpy.data.libraries.load(f"{SP}/epe2/lib2.blend", link=False) as (src, dst):
    dst.collections = list(src.collections)
L2 = {c.name: c for c in dst.collections}
def autumn(src_name, new_name, hue, sat=1.4, val=1.1):
    """Copy a lib2 tree with its leaf colour pushed toward Oyo's orange-gold."""
    nc = bpy.data.collections.new(new_name); cache = {}
    for o in L2[src_name].objects:
        n = o.copy(); nc.objects.link(n)
        for i, sl in enumerate(n.material_slots):
            m = sl.material
            if not m or not m.use_nodes: continue
            b = m.node_tree.nodes.get("Principled BSDF")
            leafy = b and b.inputs["Base Color"].is_linked and (b.inputs["Alpha"].is_linked or any(k in m.name.lower() for k in ("pine", "leaf")))
            if not leafy: continue
            if m.name not in cache:
                m2 = m.copy(); nt = m2.node_tree; b2 = nt.nodes.get("Principled BSDF")
                lk = b2.inputs["Base Color"].links[0]; hs = nt.nodes.new("ShaderNodeHueSaturation")
                hs.inputs["Hue"].default_value = hue; hs.inputs["Saturation"].default_value = sat; hs.inputs["Value"].default_value = val
                nt.links.new(lk.from_socket, hs.inputs["Color"]); nt.links.new(hs.outputs["Color"], b2.inputs["Base Color"]); cache[m.name] = m2
            sl.link = 'OBJECT'; sl.material = cache[m.name]
    ASSET[new_name] = nc
# real trees replace the Poly Haven stand-ins everywhere the scene asks for them
ASSET["island_tree_01"] = L2["T_beech"]; ASSET["island_tree_02"] = L2["T_maple"]; ASSET["island_tree_03"] = L2["T_hp"]; ASSET["tree_small_02"] = L2["T_pines"]
autumn("T_beech", "flame_tree", 0.32, 2.4, 1.8); autumn("T_maple", "gold_tree", 0.35, 2.3, 1.8); autumn("T_pines", "gold_cone", 0.47, 2.0, 2.3); autumn("T_pines", "green_cone", 0.70, 1.2, 1.1); ASSET["tree_small_02"] = ASSET["green_cone"]; autumn("T_hp", "flame_tree2", 0.31, 1.9, 1.2)
SHRUBS = [L2[n] for n in L2 if n.startswith(("H_spindle", "P_alex"))]
GRASS = [L2[n] for n in L2 if n.startswith("G_grass")]
PALM_REAL = L2["P_palm"]
# conifers (the dark-green pines in the Oyo set)
M_PINE = flat("Pine_Needles", (0.03, 0.12, 0.04), rough=0.8); M_PINE_TRUNK = flat("Pine_Trunk", (0.25, 0.18, 0.12), rough=0.9)
def make_conifer(name, h):
    col = bpy.data.collections.new(name)
    cyl("Pine_Trunk", (0, 0, h * 0.12), 0.16, h * 0.24, M_PINE_TRUNK, col, verts=8)
    for k in range(5):
        z0 = h * (0.18 + k * 0.15); r = h * (0.24 - k * 0.042)
        me = bpy.data.meshes.new("pine"); bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=0.05, depth=h * 0.3)
        for v in bm.verts: v.co.x += math.sin(v.co.z * 9 + k) * 0.08 * r
        bm.to_mesh(me); bm.free(); o = bpy.data.objects.new("Pine", me); me.materials.append(M_PINE)
        for p in me.polygons: p.use_smooth = True
        o.location = (0, 0, z0 + h * 0.15); col.objects.link(o)
    ASSET[name] = col
make_conifer("conifer_a", 3.6); make_conifer("conifer_b", 4.6)

def inst(cname, x, y, z=0.0, s=1.0, rz=None, col=None, sxy=None):
    c = ASSET[cname] if isinstance(cname, str) else cname
    if isinstance(cname, str) and cname.startswith(("flame_tree", "gold_tree")) and sxy is None:
        sxy = 0.72; s *= 1.15   # Oyo's autumn trees are tall and narrow (poplar-like)
    e = bpy.data.objects.new("I_" + c.name[:20], None); e.instance_type = 'COLLECTION'; e.instance_collection = c
    e.location = (x, y, z); e.rotation_euler = (0, 0, R.uniform(0, 6.283) if rz is None else rz)
    e.scale = (s * (sxy or 1), s * (sxy or 1), s); (col or C_VEG).objects.link(e); return e

def terrain_h(x, y):
    d = math.hypot(x - 85, y - 140); w = min(1.0, max(0.0, (d - 260) / 500))
    h = (math.sin(x * 0.006) * math.cos(y * 0.005) * 9 + math.sin(x * 0.013 + 1.7) * 5 + math.cos(y * 0.011 + 0.4) * 6)
    return -0.05 + max(0, h + 6) * w * 1.6

# ============================================================================= COCONUT PALM (procedural, real leaflets)
M_PALM_LEAF = flat("Palm_Leaf", (0.13, 0.30, 0.06), rough=0.55)
_pl = M_PALM_LEAF.node_tree; _pb = _pl.nodes["Principled BSDF"]
_pb.inputs["Subsurface Weight"].default_value = 0.15; _pb.inputs["Subsurface Radius"].default_value = (0.2, 0.5, 0.1)
_pn = _pl.nodes.new("ShaderNodeTexNoise"); _pn.inputs["Scale"].default_value = 0.6
_pg = _pl.nodes.new("ShaderNodeNewGeometry"); _pl.links.new(_pg.outputs["Position"], _pn.inputs["Vector"])
_pr = _pl.nodes.new("ShaderNodeValToRGB"); _pr.color_ramp.elements[0].color = (0.10, 0.22, 0.04, 1); _pr.color_ramp.elements[1].color = (0.30, 0.42, 0.10, 1)
_pl.links.new(_pn.outputs["Fac"], _pr.inputs["Fac"]); _pl.links.new(_pr.outputs["Color"], _pb.inputs["Base Color"])
M_PALM_TRUNK = flat("Palm_Trunk", (0.30, 0.24, 0.18), rough=0.85)
_tn = M_PALM_TRUNK.node_tree; _tb = _tn.nodes["Principled BSDF"]
_tw = _tn.nodes.new("ShaderNodeTexWave"); _tw.wave_type = 'BANDS'; _tw.bands_direction = 'Z'; _tw.inputs["Scale"].default_value = 26.0; _tw.inputs["Distortion"].default_value = 6
_tc = _tn.nodes.new("ShaderNodeTexCoord"); _tn.links.new(_tc.outputs["Object"], _tw.inputs["Vector"])
_tr = _tn.nodes.new("ShaderNodeValToRGB"); _tr.color_ramp.elements[0].color = (0.06, 0.05, 0.04, 1); _tr.color_ramp.elements[1].color = (0.16, 0.12, 0.09, 1)
_tn.links.new(_tw.outputs["Color"], _tr.inputs["Fac"]); _tn.links.new(_tr.outputs["Color"], _tb.inputs["Base Color"])
_tbump = _tn.nodes.new("ShaderNodeBump"); _tbump.inputs["Strength"].default_value = 1.0; _tn.links.new(_tw.outputs["Fac"], _tbump.inputs["Height"]); _tn.links.new(_tbump.outputs["Normal"], _tb.inputs["Normal"])

def make_palm(seed, height):
    r = random.Random(seed); col = bpy.data.collections.new(f"PALM_{seed}")
    lean = Vector((r.uniform(-0.6, 0.6), r.uniform(-0.6, 0.6), 0))
    pts = [Vector((0, 0, 0)) + lean * (t / 10) ** 2 * height * 0.12 + Vector((0, 0, height * t / 10)) for t in range(11)]
    # trunk: tapered tube built with bmesh rings
    bm = bmesh.new(); rings = []
    for i, p in enumerate(pts):
        rad = 0.24 - 0.09 * (i / 10) + (0.05 if i == 0 else 0)
        ring = [bm.verts.new(p + Vector((math.cos(a) * rad, math.sin(a) * rad, 0))) for a in [k * 2 * math.pi / 12 for k in range(12)]]
        if rings:
            for k in range(12): bm.faces.new((rings[-1][k], rings[-1][(k + 1) % 12], ring[(k + 1) % 12], ring[k]))
        rings.append(ring)
    me = bpy.data.meshes.new("palm_trunk"); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    tr = bpy.data.objects.new("PalmTrunk", me); me.materials.append(M_PALM_TRUNK); col.objects.link(tr)
    top = pts[-1]
    # crown: fronds with paired leaflets
    bm = bmesh.new()
    nf = r.randint(16, 20)
    for f in range(nf):
        az = f * 2 * math.pi / nf + r.uniform(-0.2, 0.2)
        up = r.uniform(0.15, 0.85) if f % 3 else r.uniform(0.7, 1.1)
        L = r.uniform(3.6, 4.6)
        dirh = Vector((math.cos(az), math.sin(az), 0))
        side = Vector((-dirh.y, dirh.x, 0))
        segs = 26
        def rach(t):  # arching rachis: rises then droops
            return top + dirh * (L * t) + Vector((0, 0, L * (up * t - (0.55 + 0.25 * up) * t * t)))
        for s in range(2, segs):
            t = s / segs; p = rach(t); tang = (rach(min(1, t + 0.02)) - p).normalized()
            ll = 0.95 * math.sin(math.pi * min(1, t * 1.05)) + 0.15
            for sgn in (-1, 1):
                d = (side * sgn * 0.85 + Vector((0, 0, -0.55)) + tang * 0.35).normalized()
                tip = p + d * ll; w = 0.055 * ll / 1.1
                ww = tang * w
                v = [bm.verts.new(p - ww), bm.verts.new(p + ww), bm.verts.new(tip + ww * 0.2), bm.verts.new(tip - ww * 0.2)]
                bm.faces.new(v)
        # rachis itself
        prev = None
        for s in range(segs + 1):
            p = rach(s / segs); w = 0.05 * (1 - s / segs) + 0.01
            a = bm.verts.new(p - side * w); b2 = bm.verts.new(p + side * w)
            if prev: bm.faces.new((prev[0], prev[1], b2, a))
            prev = (a, b2)
    # coconut cluster
    me = bpy.data.meshes.new("palm_crown"); bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = True
    cr = bpy.data.objects.new("PalmCrown", me); me.materials.append(M_PALM_LEAF); col.objects.link(cr)
    for k in range(5):
        a = k * 1.3; cc = top + Vector((math.cos(a) * 0.28, math.sin(a) * 0.28, -0.35))
        me2 = bpy.data.meshes.new("nut"); bm2 = bmesh.new(); bmesh.ops.create_uvsphere(bm2, u_segments=10, v_segments=8, radius=0.14); bm2.to_mesh(me2); bm2.free()
        nut = bpy.data.objects.new("Nut", me2); nut.location = cc; me2.materials.append(M_PALM_TRUNK); col.objects.link(nut)
    return col
PALMS = [make_palm(s, h) for s, h in ((1, 8.5), (2, 9.5), (3, 7.5), (4, 10.5))]
def palm(x, y, s=1.0, col=None):
    return inst(R.choice(PALMS), x, y, 0.0, s * R.uniform(0.9, 1.1), col=col)

# ============================================================================= ENTRANCE (client: wide gate for two cars, bungalow at the side, fully fenced)
M_BROWN = flat("Sign_Brown", (0.20, 0.13, 0.08), rough=0.35)
M_SIGNPANEL = pbr("Sign_Panel", "white_plaster_02", tile=2.0, tint=(1.0, 0.97, 0.92), bump=0.25)
M_ORANGE_FRAME = flat("Orange_Frame", (0.95, 0.33, 0.02), rough=0.3, metal=0.2)
EDGE_ANG = math.atan2(p1.y - p0.y, p1.x - p0.x)          # estate front edge runs along the highway
def y_edge(x): return p0.y + (x - p0.x) * (p1.y - p0.y) / (p1.x - p0.x)
def frame_at(x, inset=0.0, z=0.0):
    """Empty on the front edge at x, local +X along the edge, local -Y facing the highway."""
    e = bpy.data.objects.new("Frame", None); e.location = (x, y_edge(x) + inset, z); e.rotation_euler = (0, 0, EDGE_ANG); C_BUILD.objects.link(e); return e
def parent_all(objs, par):
    for o in objs: o.parent = par

# ---------- 3D logo: traced from the brand artwork, extruded; front face carries the original colours
LP = json.load(open(f"{SP}/epe2/logo_polys.json"))
M_LOGO_FRONT = bpy.data.materials.new("Logo3D_Front"); M_LOGO_FRONT.use_nodes = True
_ln = M_LOGO_FRONT.node_tree; _lb = _ln.nodes["Principled BSDF"]; _li = _ln.nodes.new("ShaderNodeTexImage"); _li.image = bpy.data.images.load(LOGO, check_existing=True)
_li.extension = 'EXTEND'; _ln.links.new(_li.outputs["Color"], _lb.inputs["Base Color"]); _lb.inputs["Roughness"].default_value = 0.25
_lb.inputs["Coat Weight"].default_value = 0.6; _ln.links.new(_li.outputs["Color"], _lb.inputs["Emission Color"]); _lb.inputs["Emission Strength"].default_value = 0.15
M_LOGO_SIDE_O = flat("Logo3D_Side_Orange", (0.85, 0.28, 0.02), rough=0.3, metal=0.3)
M_LOGO_SIDE_G = flat("Logo3D_Side_Green", (0.18, 0.45, 0.05), rough=0.3, metal=0.2)
def logo3d(size, depth, col):
    par = bpy.data.objects.new("Logo3D", None); col.objects.link(par)
    for key, side in (("orange", M_LOGO_SIDE_O), ("green", M_LOGO_SIDE_G)):
        for i, part in enumerate(LP[key]):
            pg = Polygon([(x * size, y * size) for x, y in part["ext"]], [[(x * size, y * size) for x, y in h] for h in part["holes"]]).buffer(0)
            o = mesh_from_poly(f"Logo_{key}{i}", pg, 0, depth, None, col, sides=True)
            o.data.materials.append(M_LOGO_FRONT); o.data.materials.append(side)
            uv = o.data.uv_layers.new(name="UV")
            for poly in o.data.polygons:
                top = poly.normal.z > 0.5; poly.material_index = 0 if top else 1
                for li in poly.loop_indices:
                    co = o.data.vertices[o.data.loops[li].vertex_index].co
                    uv.data[li].uv = (co.x / size + 0.5, (co.y / size) / LP["aspect"] + 0.5)
            o.parent = par
    return par   # lies flat (front = +Z); caller rotates it upright

# ---------- gooseneck sign lamps (warm spots washing the sign face, like the Oyo walls)
M_LAMPHEAD = flat("Lamp_Head_Black", (0.02, 0.02, 0.02), rough=0.35, metal=0.6)
def gooseneck(par, lx, top_z, reach=0.75, power=140):
    pts = [(lx, 0.0, top_z), (lx, 0.0, top_z + 0.35), (lx, -0.25, top_z + 0.55), (lx, -reach, top_z + 0.5)]
    t = tube("Gooseneck", pts, 0.025, M_LAMPHEAD, C_BUILD, res=2); t.parent = par
    h = cyl("LampHead", (lx, -reach, top_z + 0.45), 0.08, 0.22, M_LAMPHEAD, C_BUILD, verts=12); h.parent = par
    g = cyl("LampGlow", (lx, -reach, top_z + 0.335), 0.065, 0.01, M_LED, C_BUILD, verts=12); g.parent = par
    ld = bpy.data.lights.new("SignSpot", 'SPOT'); ld.energy = power * 3.5; ld.spot_size = math.radians(80); ld.spot_blend = 0.6; ld.color = (1.0, 0.82, 0.6); ld.shadow_soft_size = 0.05
    lo = bpy.data.objects.new("SignSpot", ld); lo.location = (lx, -reach, top_z + 0.33)
    lo.rotation_euler = (math.radians(28), 0, 0); C_BUILD.objects.link(lo); lo.parent = par

# ---------- fonts for signage (DM Serif Display, SIL OFL)
FD = bpy.data.fonts.load(f"{SP}/assets/fonts/DMSerifDisplay-Regular.ttf")
FDI = bpy.data.fonts.load(f"{SP}/assets/fonts/DMSerifDisplay-Italic.ttf")
M_STONE = pbr("Stone_Clad", "concrete_panels", tile=1.2, tint=(0.70, 0.64, 0.56), bump=0.9)
M_CHARTEXT = flat("Sign_Text_Charcoal", (0.045, 0.04, 0.035), rough=0.3, metal=0.4)
M_SIGNFACE = flat("Sign_Face", (0.88, 0.85, 0.79), rough=0.55, emit=(1.0, 0.88, 0.70), es=0.08)
M_SCONCE = flat("Sconce_Glow", (1, 0.85, 0.6), emit=(1, 0.8, 0.55), es=12.0)
M_FRAME_BLK = flat("Window_Frame_Black", (0.015, 0.015, 0.017), rough=0.35, metal=0.5)

# ---------- bungalow gatehouse at the side of a wide entrance (stays inside the road corridor, clear of the 600 sqm plot)
GX0, GX1 = 137.0, 139.4            # thin gatehouse: half under the canopy, half into the 600 sqm
GATE_X0 = 127.3
MED = (GATE_X0 + GX0) / 2            # median splits IN and OUT equally
Z0 = Z_WALK; zb = Z0 + 0.35; H = 3.0
gh = frame_at((GX0 + GX1) / 2)
def L(x0, y0, z0, x1, y1, z1, mat, bev=0.0, name="GH"):
    o = box_at(name, x0, y0, z0, x1, y1, z1, mat, C_BUILD, bevel=bev); o.parent = gh; return o
w2 = (GX1 - GX0) / 2; d0, d1 = 0.35, 8.2
L(-w2 - 0.25, d0 - 0.25, 0, w2 + 0.25, d1 + 0.25, zb, M_STONE, name="GH_Plinth")
# shell: stone-clad lower band, white render above
for (x0, y0, x1, y1, nm) in ((-w2, d0, -w2 + 0.25, d1, "W"), (w2 - 0.25, d0, w2, d1, "E"), (-w2, d1 - 0.25, w2, d1, "N"), (-w2, d0, w2, d0 + 0.25, "S")):
    L(x0, y0, zb, x1, y1, zb + 0.95, M_STONE, name=f"GH_Stone_{nm}")
    L(x0, y0, zb + 0.95, x1, y1, zb + H, M_PLASTER, name=f"GH_Render_{nm}")
# front (south, facing the highway): wide black-framed window + timber sunshade
L(-w2 + 0.45, d0 - 0.02, zb + 1.05, w2 - 0.45, d0 + 0.27, zb + 2.55, M_FRAME_BLK, name="GH_FrontFrame")
L(-w2 + 0.52, d0 - 0.04, zb + 1.12, w2 - 0.52, d0 + 0.05, zb + 2.48, M_GLASS, name="GH_FrontGlass")
L(-0.03, d0 - 0.05, zb + 1.12, 0.03, d0 + 0.05, zb + 2.48, M_FRAME_BLK, name="GH_FrontMullion")
for k in range(5): L(-w2 + 0.4, d0 - 0.55 + 0.0, zb + 2.62 + k * 0.0, w2 - 0.4, d0 - 0.05, zb + 2.66, M_CLAD, name="GH_Sunshade") if k == 0 else None
for k in range(7): L(-w2 + 0.45 + k * ((2 * w2 - 0.9) / 6) - 0.03, d0 - 0.6, zb + 2.58, -w2 + 0.45 + k * ((2 * w2 - 0.9) / 6) + 0.03, d0 - 0.02, zb + 2.7, M_CLAD, name="GH_ShadeRib")
L(-w2 + 0.4, d0 - 0.18, zb + 1.0, w2 - 0.4, d0 + 0.02, zb + 1.05, M_STONE, name="GH_Sill")
# lane side (west): sliding service window with a ledge, timber feature panel
L(-w2 - 0.03, 1.4, zb + 1.0, -w2 + 0.28, 3.4, zb + 2.3, M_FRAME_BLK, name="GH_ServiceFrame")
L(-w2 - 0.05, 1.47, zb + 1.07, -w2 + 0.02, 3.33, zb + 2.23, M_GLASS, name="GH_ServiceGlass")
L(-w2 - 0.45, 1.3, zb + 0.95, -w2, 3.5, zb + 1.02, M_STONE, name="GH_Ledge")
L(-w2 - 0.6, 1.2, zb + 2.42, -w2, 3.6, zb + 2.5, M_ALU, name="GH_ServiceAwning")
L(-w2 - 0.03, 3.9, zb + 0.95, -w2 + 0.02, 5.9, zb + H, M_CLAD, name="GH_TimberPanel")
t = text("SECURITY", (-w2 - 0.04, 4.9, zb + 2.2), 0.24, M_STEEL, C_BUILD, font=FB, rot=(math.radians(90), 0, math.radians(-90)), extrude=0.06); t.parent = gh
# rear door with canopy, side window
L(-0.5, d1 - 0.05, zb, 0.5, d1 + 0.04, zb + 2.2, M_CLAD, name="GH_Door")
L(-0.8, d1, zb + 2.35, 0.8, d1 + 0.9, zb + 2.43, M_WHITE, name="GH_DoorCanopy")
L(w2 - 0.03, 2.4, zb + 1.3, w2 + 0.03, 4.0, zb + 2.3, M_GLASS_D, name="GH_EastWindow")
# interior + lighting
L(-w2 + 0.25, d0 + 0.25, zb, w2 - 0.25, d1 - 0.25, zb + 0.04, M_PATIO, name="GH_Floor")
L(-w2 + 0.4, 1.3, zb, -w2 + 0.95, 3.6, zb + 0.85, M_CLAD, name="GH_Desk")
L(-w2 + 0.6, d0 + 0.6, zb + H - 0.1, w2 - 0.6, d1 - 0.6, zb + H - 0.06, M_LED, name="GH_CeilLight")
# floating roof slab with dark fascia and LED soffit line
L(-w2 - 0.7, d0 - 0.75, zb + H + 0.1, w2 + 0.7, d1 + 0.6, zb + H + 0.38, M_WHITE, name="GH_Roof")
L(-w2 - 0.72, d0 - 0.77, zb + H + 0.24, w2 + 0.72, d1 + 0.62, zb + H + 0.4, M_CHAR, name="GH_RoofFascia")
L(-w2 - 0.6, d0 - 0.65, zb + H + 0.08, w2 + 0.6, d0 - 0.6, zb + H + 0.1, M_LED, name="GH_SoffitLED")
L(-w2, d0, zb + H, w2, d1, zb + H + 0.1, M_CHAR, name="GH_ShadowGap")
for xx in (-w2 + 0.22, w2 - 0.22):
    L(xx - 0.07, d0 - 0.1, zb + 2.0, xx + 0.07, d0 - 0.02, zb + 2.35, M_FRAME_BLK, name="GH_Sconce")
    L(xx - 0.05, d0 - 0.11, zb + 2.02, xx + 0.05, d0 - 0.09, zb + 2.33, M_SCONCE, name="GH_SconceGlow")
for xx in (-w2 - 0.05, w2 + 0.05):
    L(xx - 0.4, d0 - 1.0, 0, xx + 0.4, d0 - 0.4, 0.55, M_STONE, name="GH_Planter")
    L(xx - 0.34, d0 - 0.94, 0.55, xx + 0.34, d0 - 0.46, 0.95, M_FLOWERHEDGE, bev=0.12, name="GH_PlanterHedge")
L(w2 - 0.05, 2.0, zb + 2.0, w2 + 0.45, 2.9, zb + 2.6, M_WHITE, bev=0.02, name="GH_AC")

# ---------- canopy over the gate + gatehouse (client liked it)
CAN_X1 = (GX0 + GX1) / 2; cx_mid = (GATE_X0 + CAN_X1) / 2; cv = frame_at(cx_mid)
def CV(x0, y0, z0, x1, y1, z1, mat, name="CV", bev=0.0):
    o = box_at(name, x0, y0, z0, x1, y1, z1, mat, C_BUILD, bevel=bev); o.parent = cv; return o
half = (CAN_X1 - GATE_X0) / 2 + 0.6; CZ = 6.0
CV(-half + 0.05, 0.6, Z_WALK, -half + 0.95, 5.2, CZ, M_STONE, name="Canopy_Pier_W")
CV(-half - 0.6, -0.15, Z_WALK, -half + 0.1, 1.4, 2.6, M_STONE, name="Gate_LinkWall")
CV(-half - 0.65, -0.2, 2.6, -half + 0.15, 1.45, 2.72, M_CHAR, name="Gate_LinkCap")
CV(half - 1.0, 0.6, zb + H + 0.4, half - 0.1, 5.2, CZ, M_STONE, name="Canopy_Pier_E")
CV(-half - 0.2, -0.5, CZ, half + 0.2, 6.4, CZ + 0.5, M_WHITE, name="Canopy_Slab")
CV(-half - 0.22, -0.56, CZ + 0.05, half + 0.22, -0.5, CZ + 0.58, M_CHAR, name="Canopy_Fascia")
CV(-half + 0.3, -0.2, CZ - 0.02, half - 0.3, -0.1, CZ, M_LED, name="Canopy_LED")
t = text("Orange County", (0.55, -0.6, CZ + 0.31), 0.48, M_LABEL_O, C_BUILD, font=FD, rot=(math.radians(90), 0, 0), extrude=0.08); t.parent = cv
lg = logo3d(0.62, 0.06, C_BUILD); lg.parent = cv; lg.location = (-2.6, -0.62, CZ + 0.31); lg.rotation_euler = (math.radians(90), 0, 0)
for k in range(6):
    xx = -half + 1.3 + k * (2 * half - 2.6) / 5
    CV(xx - 0.12, 2.6, CZ - 0.03, xx + 0.12, 2.9, CZ, M_LEDW, name="Canopy_Downlight")

# ---------- black bar sliding gate (open, parked behind the wall); booms inside; CAD median behind
GW = GX0 - GATE_X0
gate_par = frame_at(GATE_X0 - GW / 2 - 0.2)
for i in range(int(GW / 0.2) + 1):
    o = box_at("GateBar", -GW / 2 + i * 0.2, 0.95, Z_WALK + 0.15, -GW / 2 + i * 0.2 + 0.05, 1.02, Z_WALK + 2.3, M_FRAME_BLK, C_BUILD); o.parent = gate_par
for zz in (0.15, 1.25, 2.25):
    o = box_at("GateRail", -GW / 2 - 0.05, 0.93, Z_WALK + zz, GW / 2 + 0.05, 1.04, Z_WALK + zz + 0.08, M_FRAME_BLK, C_BUILD); o.parent = gate_par
o = box_at("GateTrack", -GW / 2, 0.85, Z_ROAD, GW * 1.5 + 0.4, 1.1, Z_ROAD + 0.03, M_STEEL, C_BUILD); o.parent = gate_par
for (px, py, L_, sgn) in ((MED - 0.5, 12.4, MED - 0.5 - GATE_X0 - 0.3, -1), (GX0 - 0.4, 12.4, GX0 - 0.4 - MED - 0.6, -1)):
    box_at("Boom_Post", px - 0.18, py - 0.18, Z_WALK, px + 0.18, py + 0.18, Z_WALK + 1.05, M_ORANGE, C_BUILD, bevel=0.02)
    if px > MED:   # IN lane: boom raised
        cube("Boom_Arm", (px, py, Z_WALK + 0.95 + L_ / 2), (0.07, 0.07, L_), M_WHITE, C_BUILD); continue
    cube("Boom_Arm", (px + sgn * L_ / 2, py, Z_WALK + 0.95), (L_, 0.07, 0.07), M_WHITE, C_BUILD)
    for k in range(int(L_ / 0.6)):
        cube("Boom_Stripe", (px + sgn * (0.3 + k * 0.6), py, Z_WALK + 0.95), (0.25, 0.075, 0.075), M_ORANGE, C_BUILD)
mesh_from_poly("Median", LineString([(MED, 11.0), (MED, 30.0)]).buffer(0.56, cap_style=1), Z_ROAD, Z_WALK + 0.05, M_CURB, C_BUILD)
mesh_from_poly("Median_Planting", LineString([(MED, 11.7), (MED, 29.4)]).buffer(0.38, cap_style=1), Z_WALK, Z_WALK + 0.12, M_LAWN, C_BUILD)

# ---------- ONE sign, built into the security wall just west of the gate (Oyo style)
SG_X1 = GATE_X0 - 1.1; SG_X0 = SG_X1 - 7.2
sg = frame_at((SG_X0 + SG_X1) / 2); sw = (SG_X1 - SG_X0) / 2
def SG(x0, y0, z0, x1, y1, z1, mat, name="Sign"):
    o = box_at(name, x0, y0, z0, x1, y1, z1, mat, C_BUILD); o.parent = sg; return o
SH = 3.3
SG(-sw, -0.3, 0, sw, 0.3, 0.55, M_STONE, "Sign_Plinth")
for xx in (-sw, sw - 0.7):                                             # stone pillars that tie into the wall
    SG(xx, -0.38, 0, xx + 0.7, 0.38, SH + 0.35, M_STONE, "Sign_Pillar")
    SG(xx - 0.06, -0.44, SH + 0.35, xx + 0.76, 0.44, SH + 0.47, M_CHAR, "Sign_PillarCap")
SG(-sw + 0.7, -0.22, 0.55, sw - 0.7, 0.22, SH, M_CHAR, "Sign_Back")
SG(-sw + 0.85, -0.27, 0.72, sw - 0.85, -0.2, SH - 0.17, M_SIGNFACE, "Sign_Face")
SG(-sw + 0.7, -0.3, SH, sw - 0.7, 0.3, SH + 0.12, M_CHAR, "Sign_Coping")
SG(-sw + 0.9, -0.31, 0.62, sw - 0.9, -0.27, 0.66, M_LED, "Sign_UpLED")
zc = (0.72 + SH - 0.17) / 2
lg = logo3d(1.55, 0.09, C_BUILD); lg.parent = sg; lg.location = (-sw + 2.05, -0.28, zc + 0.02); lg.rotation_euler = (math.radians(90), 0, 0)
tx = 0.95
for (body, size, font, mat, dz, ext) in (("Welcome to", 0.30, FDI, M_CHARTEXT, 0.58, 0.10), ("Orange County", 0.56, FD, M_CHARTEXT, 0.02, 0.10),
                                         ("E P E   ·   L A G O S", 0.17, FB, M_CHARTEXT, -0.55, 0.10)):
    t = text(body, (tx, -0.29, zc + dz), size, mat, C_BUILD, font=font, rot=(math.radians(90), 0, 0), extrude=ext, bevel=0.008); t.parent = sg
SG(tx - 1.55, -0.29, zc - 0.33, tx + 1.55, -0.26, zc - 0.31, M_ORANGE_FRAME, "Sign_Rule")
for lx in (-sw + 1.6, 0.0, sw - 1.6):
    gooseneck(sg, lx, SH + 0.12, reach=0.6, power=110)
SG(-sw + 0.7, -0.95, 0, sw - 0.7, -0.3, 0.45, M_STONE, "Sign_Planter")
for i in range(12):
    e = inst(R.choice(FLOWERS), R.uniform(-sw + 0.9, sw - 0.9), R.uniform(-0.8, -0.45), 0.45, R.uniform(0.6, 0.85)); e.parent = sg
FW_X0, FW_X1 = SG_X0 - 0.05, SG_X1 + 0.05

# ---------- Oyo-style curved double street lamps lining the entrance road
def curved_lamp(x, y, flip=1):
    tube("CurvedLamp", [(x, y, Z_WALK), (x, y, 6.5), (x + flip * 0.4, y, 7.6), (x + flip * 1.3, y, 8.0), (x + flip * 1.9, y, 7.8)], 0.07, M_ALU, C_PROPS)
    tube("CurvedLamp2", [(x, y, 5.4), (x, y, 6.0), (x + flip * 0.35, y, 6.7), (x + flip * 1.1, y, 7.0), (x + flip * 1.6, y, 6.8)], 0.05, M_ALU, C_PROPS)
    for (hx, hz) in ((1.9, 7.75), (1.6, 6.75)):
        cyl("CL_head", (x + flip * hx, y, hz), 0.17, 0.12, M_LAMPHEAD, C_PROPS, verts=14)
        cyl("CL_glow", (x + flip * hx, y, hz - 0.065), 0.14, 0.01, M_LED, C_PROPS, verts=14)
for y in (17.0, 24.0, 31.0):
    curved_lamp(126.9, y, 1); curved_lamp(138.0, y, -1)

# ---------- perimeter fence: fully enclosed, runs behind the commercial plots (Block A + corner 600)
COMM = unary_union([p["poly"] for p in PLOTS if p["block"] == "A"]).buffer(0.7, join_style=2)
INNER = ESTATE.difference(COMM)
INNER = max(INNER.geoms, key=lambda g: g.area) if isinstance(INNER, MultiPolygon) else INNER
ring = list(INNER.simplify(0.35).exterior.coords)
def front_dist(x, y): return abs(y - y_edge(x))
def deco_fence(a, b, name):
    a, b = Vector(a), Vector(b); d = b - a; Ln = d.length; d.normalize()
    ln = LineString([tuple(a), tuple(b)])
    mesh_from_poly(name + "_Base", ln.buffer(0.16, cap_style=2), Z_ROAD - 0.02, 0.95, M_CREAM, C_BUILD)
    mesh_from_poly(name + "_BaseCap", ln.buffer(0.2, cap_style=2), 0.95, 1.02, M_CHAR, C_BUILD)
    k = max(1, int(Ln / 3.2))
    for i in range(k + 1):
        q = a + d * (Ln * i / k); cube(name + "_Pier", (q.x, q.y, 1.25), (0.5, 0.5, 2.5), M_CREAM, C_BUILD); cube(name + "_PierCap", (q.x, q.y, 2.55), (0.6, 0.6, 0.1), M_CHAR, C_BUILD)
    nb = int(Ln / 0.16)
    for i in range(nb):
        q = a + d * (Ln * (i + 0.5) / nb); cube(name + "_Rail", (q.x, q.y, 1.65), (0.04, 0.04, 1.26), M_ALU, C_BUILD)
    for zz in (1.08, 2.24): mesh_from_poly(name + "_Bar", ln.buffer(0.03, cap_style=2), zz, zz + 0.05, M_ALU, C_BUILD)
EXCL = [Polygon([(GATE_X0 - 1.0, y_edge(GATE_X0) - 2), (GX0, y_edge(GX0) - 2), (GX0, y_edge(GX0) + 2.4), (GATE_X0 - 1.0, y_edge(GATE_X0) + 2.4)]),
        box(GX0 - 0.3, y_edge(GX1) - 1.0, GX1 + 0.5, y_edge(GX1) + 6.0),
        Polygon([(FW_X0, y_edge(FW_X0) - 1.2), (FW_X1, y_edge(FW_X1) - 1.2), (FW_X1, y_edge(FW_X1) + 1.2), (FW_X0, y_edge(FW_X0) + 1.2)])]
EXU = unary_union(EXCL)
segs_built = 0
for i in range(len(ring) - 1):
    seg = LineString([ring[i], ring[i + 1]])
    if seg.length < 0.3: continue
    rest = seg.difference(EXU)
    for j, piece in enumerate(getattr(rest, "geoms", [rest])):
        if piece.is_empty or piece.length < 0.4: continue
        a, b = piece.coords[0], piece.coords[-1]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        wall_run(a, b, f"Fence{i}_{j}")
        segs_built += 1
# side fences closing the ends of the commercial strip (front stays open to the road)
for k, piece in enumerate(getattr(ESTATE.exterior.intersection(COMM.buffer(0.2)), "geoms", [])):
    for m in range(len(piece.coords) - 1):
        a, c = piece.coords[m], piece.coords[m + 1]
        if LineString([a, c]).length < 0.4: continue
        if front_dist((a[0] + c[0]) / 2, (a[1] + c[1]) / 2) < 3.0: continue
        wall_run(a, c, f"FenceComm{k}_{m}"); segs_built += 1
print("fence segments", segs_built, flush=True)

# ============================================================================= GYM + SUPERMART (open space)
OS = Polygon(json.load(open(f"{SP}/epe2/plan.json"))["open_space"])
mesh_from_poly("OpenSpace_Paving", OS.buffer(0.4), Z_ROAD, Z_WALK + 0.02, M_PAVERS, C_BUILD)
BX0, BX1, BY0, BY1, BH = 101.4, 113.4, 9.6, 26.2, 4.6
zf = Z_WALK + 0.02
box_at("Shop_Slab", BX0, BY0, Z_WALK, BX1 + 0.3, BY1, zf + 0.12, M_PANEL, C_BUILD)
zf += 0.12
box_at("Shop_Back", BX0, BY0, zf, BX0 + 0.3, BY1, zf + BH, M_CHAR, C_BUILD)
box_at("Shop_N", BX0, BY1 - 0.3, zf, BX1, BY1, zf + BH, M_CHAR, C_BUILD)
box_at("Shop_S_lo", BX0, BY0, zf, BX1, BY0 + 0.3, zf + 0.6, M_CHAR, C_BUILD)
box_at("Shop_S_glass", BX0 + 0.5, BY0 + 0.08, zf + 0.6, BX1 - 0.5, BY0 + 0.16, zf + BH - 0.7, M_GLASS, C_BUILD)
box_at("Shop_S_head", BX0, BY0, zf + BH - 0.7, BX1, BY0 + 0.3, zf + BH, M_CHAR, C_BUILD)
box_at("Shop_Divider", BX0, 17.6, zf, BX1 - 0.3, 17.8, zf + BH, M_PLASTER, C_BUILD)
box_at("Shop_E_glass", BX1 - 0.12, BY0 + 0.3, zf, BX1 - 0.04, BY1 - 0.3, zf + BH - 0.7, M_GLASS, C_BUILD)
for y in [BY0 + 0.3 + i * 2.05 for i in range(9)] + [17.7]:
    box_at("Shop_Mullion", BX1 - 0.16, y - 0.05, zf, BX1, y + 0.05, zf + BH - 0.7, M_ALU, C_BUILD)
box_at("Shop_E_head", BX1 - 0.3, BY0, zf + BH - 0.7, BX1, BY1, zf + BH, M_CHAR, C_BUILD)
box_at("Shop_Roof", BX0 - 0.3, BY0 - 0.3, zf + BH, BX1 + 0.3, BY1 + 0.3, zf + BH + 0.35, M_WHITE, C_BUILD)
box_at("Shop_Parapet_band", BX1 + 0.28, BY0 - 0.3, zf + BH - 0.15, BX1 + 0.34, BY1 + 0.3, zf + BH + 0.5, M_WHITE, C_BUILD)
box_at("Shop_Canopy", BX1, BY0 + 0.4, zf + BH - 1.0, BX1 + 2.4, BY1 - 0.4, zf + BH - 0.82, M_WHITE, C_BUILD)
box_at("Shop_CanopyLED", BX1 + 2.2, BY0 + 0.5, zf + BH - 1.02, BX1 + 2.3, BY1 - 0.5, zf + BH - 1.0, M_LED, C_BUILD)
box_at("Shop_OrangeLine", BX1 + 0.3, BY0 - 0.3, zf + BH + 0.4, BX1 + 0.36, BY1 + 0.3, zf + BH + 0.48, M_ORANGE, C_BUILD)
for (ycen, word, sz) in ((21.9, "SUPERMARKET", 0.78), (13.6, "GYM", 1.05)):
    text(word, (BX1 + 0.42, ycen, zf + BH + 0.05), sz, M_LABEL, C_BUILD, rot=(math.radians(90), 0, math.radians(90)), extrude=0.12)
text("GYM", ((BX0 + BX1) / 2, BY0 - 0.36, zf + BH - 0.35), 0.7, M_LABEL, C_BUILD, rot=(math.radians(90), 0, 0), extrude=0.12)
for i in range(3): box_at("Roof_AC", BX0 + 1.5 + i * 3.2, BY1 - 3.0, zf + BH + 0.35, BX0 + 3.0 + i * 3.2, BY1 - 1.8, zf + BH + 1.2, M_WHITE, C_BUILD, bevel=0.03)
box_at("Shop_Floor", BX0, BY0, zf, BX1, BY1, zf + 0.02, M_PATIO, C_BUILD)
for y0 in (BY0 + 0.6, 18.2):
    for i in range(3):
        box_at("Shop_CeilPanel", BX0 + 1.0 + i * 3.6, y0 + 0.4, zf + BH - 0.82, BX0 + 3.4 + i * 3.6, y0 + 7.0, zf + BH - 0.78, M_LEDW, C_BUILD)
# supermarket fit-out
GOODS = [flat(f"Goods{i}", c, rough=0.45) for i, c in enumerate([(0.85, 0.1, 0.08), (0.95, 0.75, 0.1), (0.1, 0.45, 0.2), (0.92, 0.92, 0.9), (0.15, 0.3, 0.75), (0.9, 0.45, 0.1)])]
for r_ in range(4):
    x = BX0 + 1.6 + r_ * 2.3
    box_at("Shelf", x - 0.35, 18.8, zf, x + 0.35, 25.0, zf + 1.9, M_WHITE, C_BUILD)
    for lvl in range(4):
        for k in range(14):
            yy = 18.95 + k * 0.43
            for sgn in (-1, 1):
                box_at("Item", x + sgn * 0.26 - 0.09, yy, zf + 0.25 + lvl * 0.45, x + sgn * 0.26 + 0.09, yy + 0.34, zf + 0.25 + lvl * 0.45 + R.uniform(0.18, 0.32), R.choice(GOODS), C_BUILD)
box_at("Fridge_wall", BX0 + 0.3, 18.0, zf, BX0 + 1.0, BY1 - 0.3, zf + 2.3, M_LEDW, C_BUILD)
box_at("Checkout", BX1 - 2.6, 19.0, zf, BX1 - 1.6, 21.2, zf + 1.0, M_CLAD, C_BUILD)
box_at("Checkout_top", BX1 - 2.65, 18.95, zf + 1.0, BX1 - 1.55, 21.25, zf + 1.05, M_WHITE, C_BUILD)
# gym fit-out: treadmills facing the glass, racks, benches, mirror
M_RUBBER = flat("Gym_Rubber", (0.04, 0.04, 0.045), rough=0.9); M_MIRROR = flat("Mirror", (0.9, 0.9, 0.9), rough=0.0, metal=1.0)
box_at("Gym_Floor", BX0 + 0.3, BY0 + 0.3, zf + 0.02, BX1 - 0.2, 17.6, zf + 0.04, M_RUBBER, C_BUILD)
box_at("Gym_Mirror", BX0 + 0.3, BY0 + 0.6, zf + 0.3, BX0 + 0.34, 17.2, zf + 2.6, M_MIRROR, C_BUILD)
for k in range(5):
    y = BY0 + 1.0 + k * 1.45; x = BX1 - 1.6
    box_at("TM_base", x - 0.9, y - 0.38, zf + 0.04, x + 0.9, y + 0.38, zf + 0.26, M_ALU, C_BUILD, bevel=0.03)
    box_at("TM_belt", x - 0.8, y - 0.26, zf + 0.26, x + 0.75, y + 0.26, zf + 0.28, M_BLACK, C_BUILD)
    for sgn in (-1, 1): box_at("TM_arm", x + 0.75, y + sgn * 0.34 - 0.03, zf + 0.26, x + 0.82, y + sgn * 0.34 + 0.03, zf + 1.3, M_STEEL, C_BUILD)
    box_at("TM_console", x + 0.7, y - 0.35, zf + 1.25, x + 0.9, y + 0.35, zf + 1.45, M_BLACK, C_BUILD)
    box_at("TM_screen", x + 0.69, y - 0.18, zf + 1.3, x + 0.7, y + 0.18, zf + 1.42, M_LEDW, C_BUILD)
for k in range(3):
    y = BY0 + 1.6 + k * 2.4; x = BX0 + 3.2
    box_at("Bench", x - 0.6, y - 0.18, zf + 0.04, x + 0.6, y + 0.18, zf + 0.48, M_BLACK, C_BUILD, bevel=0.05)
    for sgn in (-1, 1): box_at("RackPost", x + sgn * 0.7 - 0.04, y - 0.04, zf + 0.04, x + sgn * 0.7 + 0.04, y + 0.04, zf + 1.6, M_STEEL, C_BUILD)
    tube("Bar", [(x - 1.1, y, zf + 1.35), (x + 1.1, y, zf + 1.35)], 0.02, M_STEEL, C_BUILD)
    for sgn in (-1, 1): cyl("Plate", (x + sgn * 0.95, y, zf + 1.35), 0.22, 0.06, M_BLACK, C_BUILD, rot=(0, math.radians(90), 0))
box_at("DB_rack", BX0 + 0.6, 12.0, zf + 0.04, BX0 + 1.2, 16.4, zf + 0.85, M_STEEL, C_BUILD)
for k in range(9): cyl("DB", (BX0 + 0.9, 12.3 + k * 0.45, zf + 0.92), 0.08, 0.36, M_BLACK, C_BUILD, rot=(0, math.radians(90), 0))
# forecourt parking + planters + trees
for k in range(5):
    y = 11.0 + k * 3.0
    mesh_from_poly("ParkLine", LineString([(119.0, y), (125.5, y)]).buffer(0.06), Z_WALK + 0.02, Z_WALK + 0.03, M_LINE, C_BUILD, sides=False)
for (x, y) in ((116.0, 25.0), (116.0, 9.6)):
    box_at("Planter", x - 1.2, y - 0.6, Z_WALK, x + 1.2, y + 0.6, Z_WALK + 0.55, M_PANEL, C_BUILD)
    for i in range(6): inst(R.choice(FLOWERS), x + R.uniform(-1, 1), y + R.uniform(-0.4, 0.4), Z_WALK + 0.55, R.uniform(0.7, 1.0))
inst("island_tree_01", 100.5, 27.0, Z_WALK, 1.7); inst("island_tree_02", 104.0, 7.4, Z_WALK, 1.5)
for y in (10.4, 17.7, 25.4): inst("potted_plant_01", BX1 + 0.8, y, zf, 1.2)
for k in range(3): inst("modular_street_seating", 117.5, 13.5 + k * 4.5, Z_WALK, 1.0, rz=math.radians(90), col=C_PROPS)

# ============================================================================= FACILITIES: swimming pool & subordinates, football pitch above
FAC = Polygon(json.load(open(f"{SP}/epe2/plan.json"))["facility"])
fx0, fy0, fx1, fy1 = FAC.bounds
blocker = [p for p in PLOTS if p["poly"].centroid.x < fx1 and p["poly"].centroid.x > fx0 and fy0 < p["poly"].centroid.y < fy1 + 8]
ysplit = min(p["poly"].bounds[1] for p in blocker) if blocker else (fy0 + fy1) / 2
LOW = FAC.intersection(box(fx0 - 1, fy0 - 1, fx1 + 1, ysplit - 0.3))
UP = FAC.intersection(box(fx0 - 1, ysplit - 0.3, fx1 + 1, fy1 + 1))
print("facility split y", round(ysplit, 2), "low", [round(v, 1) for v in LOW.bounds], "up", [round(v, 1) for v in UP.bounds], flush=True)
mesh_from_poly("Pool_Patio", LOW.buffer(0.3), Z_ROAD, Z_WALK + 0.06, M_PATIO, C_BUILD)
lx0, ly0, lx1, ly1 = LOW.bounds; zp = Z_WALK + 0.06
# pool: centred in the strip, deck to the east, pool house + pergola bar to the west
PX0, PX1 = lx0 + 11.0, lx1 - 6.0; PY0, PY1 = ly0 + 2.0, ly1 - 2.2
pool_hole = box(PX0, PY0, PX1, PY1)
mesh_from_poly("Pool_Coping_ring", box(PX0 - 0.5, PY0 - 0.5, PX1 + 0.5, PY1 + 0.5).difference(pool_hole), zp, zp + 0.1, M_CURB, C_BUILD)
box_at("Pool_Basin_floor", PX0, PY0, zp - 1.6, PX1, PY1, zp - 1.5, M_POOLTILE, C_BUILD)
for (a, b_, c, d) in ((PX0 - 0.1, PY0, PX0, PY1), (PX1, PY0, PX1 + 0.1, PY1), (PX0, PY0 - 0.1, PX1, PY0), (PX0, PY1, PX1, PY1 + 0.1)):
    box_at("Pool_Basin_wall", a, b_, zp - 1.6, c, d, zp + 0.02, M_POOLTILE, C_BUILD)
box_at("Pool_Water", PX0 + 0.02, PY0 + 0.02, zp - 1.5, PX1 - 0.02, PY1 - 0.02, zp - 0.06, M_WATER, C_BUILD)
# hide the patio under the basin opening
pat = bpy.data.objects["Pool_Patio"]; _pm = pat.data; bpy.data.objects.remove(pat); bpy.data.meshes.remove(_pm)
mesh_from_poly("Pool_Patio", LOW.buffer(0.3).difference(box(PX0 - 0.5, PY0 - 0.5, PX1 + 0.5, PY1 + 0.5)), Z_ROAD, zp, M_PATIO, C_BUILD)
box_at("Pool_Deck", PX1 + 0.5, PY0 - 0.5, zp, lx1 - 0.6, PY1 + 0.5, zp + 0.08, M_DECK, C_BUILD)
for k in range(int((PX1 - PX0) / 3.0)):
    x = PX0 + 1.5 + k * 3.0; y = PY1 + 1.35
    lo = box_at("Lounger", x - 0.35, y - 0.95, zp + 0.25, x + 0.35, y + 0.95, zp + 0.38, M_WHITE, C_PROPS, bevel=0.04)
    box_at("Lounger_back", x - 0.35, y + 0.55, zp + 0.38, x + 0.35, y + 0.95, zp + 0.9, M_WHITE, C_PROPS, bevel=0.04)
    for sx_ in (-0.3, 0.3):
        for sy_ in (-0.85, 0.85): box_at("LoungerLeg", x + sx_ - 0.02, y + sy_ - 0.02, zp, x + sx_ + 0.02, y + sy_ + 0.02, zp + 0.25, M_STEEL, C_PROPS)
    if k % 2 == 0:
        cyl("Umbrella_pole", (x + 1.5, y, zp + 1.25), 0.03, 2.5, M_STEEL, C_PROPS)
        ume = bpy.data.meshes.new("umb"); bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=False, segments=8, radius1=1.4, radius2=0.05, depth=0.45); bm.to_mesh(ume); bm.free()
        uo = bpy.data.objects.new("Umbrella", ume); uo.location = (x + 1.5, y, zp + 2.45); ume.materials.append(M_ORANGE if k % 4 == 0 else M_WHITE); C_PROPS.objects.link(uo)
# pool house (changing rooms + toilets + juice bar) with pergola
HX0, HX1, HY0, HY1 = lx0 + 0.8, PX0 - 3.0, ly0 + 0.9, ly1 - 0.9
box_at("PH_body", HX0, HY0 + 2.0, zp, HX1, HY1, zp + 3.0, M_PLASTER, C_BUILD)
box_at("PH_clad", HX1 - 0.02, HY0 + 2.0, zp, HX1 + 0.04, HY1, zp + 3.0, M_CLAD, C_BUILD)
box_at("PH_roof", HX0 - 0.4, HY0 - 0.2, zp + 3.0, HX1 + 0.8, HY1 + 0.4, zp + 3.3, M_WHITE, C_BUILD)
for k in range(3): box_at("PH_door", HX0 + 0.8 + k * 2.2, HY0 + 1.96, zp, HX0 + 1.8 + k * 2.2, HY0 + 2.02, zp + 2.2, M_CLAD, C_BUILD)
text("CHANGING  ·  BAR", ((HX0 + HX1) / 2, HY0 - 0.23, zp + 3.15), 0.28, M_LABEL, C_BUILD, rot=(math.radians(90), 0, 0), extrude=0.05)
box_at("Bar_counter", HX0 + 0.6, HY0 + 0.2, zp, HX1 - 0.6, HY0 + 0.8, zp + 1.05, M_CLAD, C_BUILD)
for k in range(6): cyl("Bar_stool", (HX0 + 1.0 + k * ((HX1 - HX0 - 2) / 5), HY0 - 0.3, zp + 0.38), 0.18, 0.75, M_ALU, C_PROPS)
for k in range(5):
    box_at("Pergola_beam", HX1 + 0.3 + k * 0.5, HY0, zp + 2.6, HX1 + 0.4 + k * 0.5, HY1, zp + 2.75, M_CLAD, C_BUILD)
for (x, y) in ((HX1 + 0.4, HY0 + 0.2), (HX1 + 2.4, HY0 + 0.2), (HX1 + 0.4, HY1 - 0.2), (HX1 + 2.4, HY1 - 0.2)):
    box_at("Pergola_post", x - 0.08, y - 0.08, zp, x + 0.08, y + 0.08, zp + 2.6, M_CLAD, C_BUILD)
inst("outdoor_table_chair_set_01", HX1 + 1.4, (HY0 + HY1) / 2, zp, 1.0, col=C_PROPS)
inst("island_tree_03", lx0 + 1.2, ly0 + 1.2, zp, 2.0)
for k in range(8): inst(R.choice(FLOWERS), PX0 + 1 + k * 2.2, PY0 - 1.2, zp, 0.8)
# football pitch (5-a-side) in the upper part
ux0, uy0, ux1, uy1 = UP.bounds
mesh_from_poly("Pitch_Surround", UP.buffer(0.3), Z_ROAD, Z_WALK + 0.04, M_PAVERS, C_BUILD)
FX0, FX1, FY0, FY1 = ux0 + 1.2, ux1 - 1.2, uy0 + 1.2, uy1 - 1.2
box_at("Pitch_Turf", FX0, FY0, Z_WALK + 0.04, FX1, FY1, Z_WALK + 0.09, M_TURF, C_BUILD)
zl = Z_WALK + 0.095; w = 0.07
for (a, b_, c, d) in ((FX0 + 0.5, FY0 + 0.5, FX1 - 0.5, FY0 + 0.5 + w), (FX0 + 0.5, FY1 - 0.5 - w, FX1 - 0.5, FY1 - 0.5),
                     (FX0 + 0.5, FY0 + 0.5, FX0 + 0.5 + w, FY1 - 0.5), (FX1 - 0.5 - w, FY0 + 0.5, FX1 - 0.5, FY1 - 0.5)):
    box_at("PitchLine", a, b_, zl - 0.004, c, d, zl, M_LINE, C_BUILD)
long_x = (FX1 - FX0) >= (FY1 - FY0)
mx_, my_ = (FX0 + FX1) / 2, (FY0 + FY1) / 2
if long_x: box_at("PitchHalf", mx_ - w / 2, FY0 + 0.5, zl - 0.004, mx_ + w / 2, FY1 - 0.5, zl, M_LINE, C_BUILD)
else: box_at("PitchHalf", FX0 + 0.5, my_ - w / 2, zl - 0.004, FX1 - 0.5, my_ + w / 2, zl, M_LINE, C_BUILD)
mesh_from_poly("PitchCircle", Point(mx_, my_).buffer(2.0).difference(Point(mx_, my_).buffer(2.0 - w)), zl - 0.004, zl, M_LINE, C_BUILD, sides=False)
M_NET = flat("Net", (0.95, 0.95, 0.95), rough=0.6, alpha=0.35)
for end in (0, 1):
    if long_x:
        gx = FX0 + 0.5 if end == 0 else FX1 - 0.5; sgn = -1 if end == 0 else 1
        for gy in (my_ - 1.5, my_ + 1.5): cyl("GoalPost", (gx, gy, zl + 1.0), 0.05, 2.0, M_WHITE, C_BUILD, verts=10)
        cyl("GoalBar", (gx, my_, zl + 2.0), 0.05, 3.1, M_WHITE, C_BUILD, verts=10, rot=(math.radians(90), 0, 0))
        box_at("GoalNet", gx + sgn * 1.0 - 0.01, my_ - 1.5, zl, gx + sgn * 1.0 + 0.01, my_ + 1.5, zl + 2.0, M_NET, C_BUILD)
        mesh_from_poly("Box", box(min(gx, gx - sgn * 4), my_ - 3, max(gx, gx - sgn * 4), my_ + 3).exterior.buffer(w / 2), zl - 0.004, zl, M_LINE, C_BUILD, sides=False)
    else:
        gy = FY0 + 0.5 if end == 0 else FY1 - 0.5; sgn = -1 if end == 0 else 1
        for gx in (mx_ - 1.5, mx_ + 1.5): cyl("GoalPost", (gx, gy, zl + 1.0), 0.05, 2.0, M_WHITE, C_BUILD, verts=10)
        cyl("GoalBar", (mx_, gy, zl + 2.0), 0.05, 3.1, M_WHITE, C_BUILD, verts=10, rot=(0, math.radians(90), 0))
        box_at("GoalNet", mx_ - 1.5, gy + sgn * 1.0 - 0.01, zl, mx_ + 1.5, gy + sgn * 1.0 + 0.01, zl + 2.0, M_NET, C_BUILD)
# chain-link fence + floodlights around the pitch
M_FENCE = flat("ChainLink", (0.15, 0.17, 0.16), rough=0.5, metal=0.6, alpha=0.45)
fr = box(FX0 - 0.3, FY0 - 0.3, FX1 + 0.3, FY1 + 0.3).exterior
mesh_from_poly("Pitch_Fence", fr.buffer(0.02), Z_WALK + 0.04, Z_WALK + 3.6, M_FENCE, C_BUILD)
for t in [i / 16 for i in range(16)]:
    q = fr.interpolate(t, normalized=True); cyl("FencePost", (q.x, q.y, Z_WALK + 1.8), 0.04, 3.6, M_ALU, C_BUILD, verts=8)
for (x, y) in ((FX0 - 0.3, FY0 - 0.3), (FX1 + 0.3, FY0 - 0.3), (FX0 - 0.3, FY1 + 0.3), (FX1 + 0.3, FY1 + 0.3)):
    cyl("Flood_pole", (x, y, Z_WALK + 4.5), 0.09, 9.0, M_ALU, C_BUILD, verts=10)
    box_at("Flood_head", x - 0.5, y - 0.15, Z_WALK + 8.9, x + 0.5, y + 0.15, Z_WALK + 9.3, M_ALU, C_BUILD)
    box_at("Flood_face", x - 0.45, y - 0.17, Z_WALK + 8.95, x + 0.45, y - 0.15, Z_WALK + 9.25, M_LEDW, C_BUILD)
for k in range(2): inst("modular_street_seating", FX0 + 3 + k * 6, FY0 - 1.0, Z_WALK + 0.04, 0.9, rz=0, col=C_PROPS)

# ============================================================================= SOLAR STREET LIGHTS (product paper feature) + CCTV
def solar_light(x, y, ang):
    par = bpy.data.objects.new("SolarLight", None); par.location = (x, y, Z_WALK); par.rotation_euler = (0, 0, ang); C_PROPS.objects.link(par)
    ps = [cyl("SL_pole", (0, 0, 3.6), 0.07, 7.2, M_STEEL, C_PROPS, verts=10),
          box_at("SL_arm", 0, -0.03, 6.9, 1.5, 0.03, 6.96, M_STEEL, C_PROPS),
          box_at("SL_head", 1.0, -0.17, 6.82, 1.9, 0.17, 6.94, M_ALU, C_PROPS, bevel=0.02),
          box_at("SL_led", 1.05, -0.14, 6.80, 1.85, 0.14, 6.82, M_LED, C_PROPS)]
    pan = box_at("SL_panel", -0.55, -0.38, 7.25, 0.55, 0.38, 7.29, M_PANEL_S, C_PROPS); pan.rotation_euler = (0, math.radians(-22), 0); ps.append(pan)
    ps.append(box_at("SL_bracket", -0.04, -0.04, 7.1, 0.04, 0.04, 7.3, M_STEEL, C_PROPS))
    for p in ps: p.parent = par
# along road-facing sidewalk edges every ~30 m, arm pointing at the road
edge_lines = []
for g in (walk.geoms if isinstance(walk, MultiPolygon) else [walk]):
    edge_lines += [g.exterior] + list(g.interiors)
est_edge = ESTATE.exterior.buffer(3.0)
for ring in edge_lines:
    Ln = ring.length; n = int(Ln / 30)
    for i in range(n):
        q = ring.interpolate(i * Ln / n);
        if est_edge.contains(q) or q.y < 30 and 115 < q.x < 145: continue
        q2 = ring.interpolate(i * Ln / n + 0.5); t = Vector((q2.x - q.x, q2.y - q.y)).normalized(); nn = Vector((t.y, -t.x))
        test = Point(q.x + nn.x * 1.2, q.y + nn.y * 1.2)
        if walk.contains(test): nn = -nn
        solar_light(q.x - nn.x * 0.6, q.y - nn.y * 0.6, math.atan2(nn.y, nn.x))
# CCTV: gatehouse corners, canopy, estate corners
for (x, y, z, rz) in ((GX0 - 0.4, y_edge(GX0) - 0.1, zb + H - 0.05, math.radians(-135)), (GX1 + 0.4, y_edge(GX1) - 0.1, zb + H - 0.05, math.radians(-45)),
                      (GATE_X0 - 0.3, y_edge(GATE_X0) + 0.6, CZ - 0.05, math.radians(-120)), (1.0, 286.0, 2.95, math.radians(-45)),
                      (170.0, 282.5, 2.95, math.radians(-135)), (1.9, 30.0, 2.95, math.radians(45)), (169.9, 18.5, 2.95, math.radians(135))):
    inst("security_camera_01", x, y, z - 0.25, 1.6, rz=rz, col=C_PROPS)

# ============================================================================= VEGETATION
# palms only on the entrance median (client), double lamps between them like Oyo
for y in (13.0, 19.5, 26.0): palm(MED, y, 0.95)
for y in (16.2, 22.8):
    curved_lamp(MED, y, 1); curved_lamp(MED, y, -1)
def on_walk(x, off=1.25):
    return p0 + dvec * ((x - p0.x) / dvec.x) + nrm * off
for x in list(range(-60, -2, 6)) + list(range(174, 260, 6)):
    pass
# bush belt outside the walls (W, N, E) — tropical trees with warm flame-tree accents
TREE_SET = ["island_tree_01", "island_tree_02", "island_tree_03", "tree_small_02", "flame_tree", "gold_tree", "gold_cone"]
TW = [1, 1, 1, 3, 3, 3, 6]
# keep the ground-level camera views across the expressway clear
VIEW_CLEAR = box(30, -90, 230, -2)
def pick_tree(): return R.choices(TREE_SET, TW)[0]
def scatter(n, region_fn, smin, smax, extra=None, cluster=1):
    k = 0
    while k < n:
        cx_, cy_ = region_fn()
        for j in range(cluster):
            x, y = (cx_ + R.gauss(0, 5), cy_ + R.gauss(0, 5)) if cluster > 1 else (cx_, cy_)
            if ESTATE.buffer(4).contains(Point(x, y)) or strip(-4, 15).contains(Point(x, y)) or VIEW_CLEAR.contains(Point(x, y)): continue
            inst(pick_tree(), x, y, terrain_h(x, y), R.uniform(smin, smax)); k += 1
            if False: inst(R.choice(SHRUBS), x + R.uniform(-4, 4), y + R.uniform(-4, 4), terrain_h(x, y), R.uniform(1.2, 2.4))
scatter(45, lambda: (R.uniform(-90, -30), R.uniform(30, 330)), 2.0, 3.4)
scatter(45, lambda: (R.uniform(-60, 235), R.uniform(318, 370)), 2.0, 3.4)
scatter(45, lambda: (R.uniform(200, 260), R.uniform(10, 330)), 2.0, 3.4)
scatter(40, lambda: (R.uniform(-160, 330), R.uniform(-80, -32)), 1.8, 3.2)
scatter(500, lambda: (85 + math.cos(a := R.uniform(0, 6.283)) * (d := R.uniform(300, 800)), 140 + math.sin(a) * d), 3.0, 5.2, cluster=4)

exec(compile(open(f"{SP}/epe2/houses.py").read(), "houses.py", "exec"))
exec(compile(open(f"{SP}/epe2/extras.py").read(), "extras.py", "exec"))

# ============================================================================= CARS
M_CARP = [flat("CarPaint_W", (0.85, 0.85, 0.84), rough=0.2, metal=0.0, coat=1.0), flat("CarPaint_S", (0.45, 0.46, 0.48), rough=0.25, metal=0.9, coat=1.0),
          flat("CarPaint_K", (0.02, 0.02, 0.025), rough=0.2, metal=0.5, coat=1.0), flat("CarPaint_R", (0.45, 0.02, 0.02), rough=0.25, metal=0.6, coat=1.0)]
M_TIRE = flat("Tire", (0.02, 0.02, 0.02), rough=0.85); M_TAIL = flat("Tail", (0.8, 0.02, 0.02), emit=(1, 0.05, 0.02), es=6.0); M_HEAD = flat("Head", (1, 1, 1), emit=(1, 0.97, 0.9), es=6.0)
CAR_GLB = f"{SP}/assets/car/car.glb"
def load_car(name, recolor=None):
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=CAR_GLB)
    new = [o for o in bpy.data.objects if o not in before]
    col = bpy.data.collections.new(name)
    for o in new:
        for c in list(o.users_collection): c.objects.unlink(o)
        col.objects.link(o)
    if recolor:
        done = {}
        for o in new:
            if o.type != 'MESH': continue
            for sl in o.material_slots:
                m = sl.material
                if not m or not m.use_nodes: continue
                bsdf = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if not bsdf: continue
                bc = bsdf.inputs["Base Color"]
                r, g, bb, _ = bc.default_value
                if bc.is_linked or not (r > 0.25 and g < 0.12 and bb < 0.12): continue
                if m.name not in done:
                    m2 = m.copy(); bsdf2 = next(n for n in m2.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
                    bsdf2.inputs["Base Color"].default_value = (*recolor, 1); done[m.name] = m2
                sl.material = done[m.name]
    return col
def paint(src, name, rgb):
    """Sketchfab car with its body paint swapped."""
    nc = bpy.data.collections.new(name); cache = {}
    for o in L2[src].objects:
        n = o.copy(); nc.objects.link(n)
        for sl in n.material_slots:
            m = sl.material
            if m and "paint" in m.name.lower():
                if m.name not in cache:
                    m2 = m.copy(); b = m2.node_tree.nodes.get("Principled BSDF")
                    for l in list(b.inputs["Base Color"].links): m2.node_tree.links.remove(l)
                    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = 0.6
                    b.inputs["Roughness"].default_value = 0.25
                    try: b.inputs["Coat Weight"].default_value = 1.0
                    except Exception: pass
                    cache[m.name] = m2
                sl.link = 'OBJECT'; sl.material = cache[m.name]
    return nc
# Toyota Camry / Corolla and Lexus RX (Sketchfab, CC-BY: ItsDiyor, Merc_TV)
CAR_COLS = {"red": paint("C_camry", "Car_Camry_Red", (0.42, 0.015, 0.01)), "silver": paint("C_lexus", "Car_Lexus_Silver", (0.50, 0.51, 0.53)),
            "white": paint("C_corolla", "Car_Corolla_White", (0.85, 0.85, 0.84)), "black": paint("C_camry", "Car_Camry_Black", (0.015, 0.015, 0.018))}
M_CARP = ["white", "silver", "black", "red"]
def car(x, y, ang, paint, suv=False):
    o = bpy.data.objects.new("Car", None); o.instance_type = 'COLLECTION'; o.instance_collection = CAR_COLS[paint]
    o.location = (x, y, Z_ROAD); o.rotation_euler = (0, 0, ang + math.pi / 2); C_PROPS.objects.link(o)
    return o
CARS_MOVING = [(car((MED + GX0) / 2, 4.0, math.radians(90), "red"), Vector((0, 1, 0)), 5.0)]          # IN lane (drive on the right), going in
car(122.3, 12.5, math.radians(180), M_CARP[0], suv=True)     # parked at the shops
car(122.3, 18.5, math.radians(180), M_CARP[2])
CARS_MOVING.append((car(60.0, 5.5, math.radians(-5.2), M_CARP[3]), Vector((math.cos(math.radians(-5.2)), math.sin(math.radians(-5.2)), 0)), 13.0))
CARS_MOVING.append((car(205.0, -1.5, math.radians(174.8), M_CARP[0], suv=True), Vector((math.cos(math.radians(174.8)), math.sin(math.radians(174.8)), 0)), 13.0))
# cars drive through the video (frame 1 = the still pose); m/s at 24 fps
FR = 768
for ci, (o, d, v) in enumerate(CARS_MOVING):
    p = o.location.copy()
    keys = [(1, 0.0), (97, 0.0), (FR, v * (FR - 97) / 24)] if ci == 0 else [(1, 0.0), (FR, v * (FR - 1) / 24)]   # arriving car waits, then drives in on shot 2
    for (f, dist) in keys:
        o.location = p + d * dist; o.keyframe_insert("location", frame=f)
    act = o.animation_data.action
    fcs = [fc for ly in getattr(act, "layers", []) for st in ly.strips for cb in st.channelbags for fc in cb.fcurves] or list(getattr(act, "fcurves", []))
    for fc in fcs:
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    o.location = p

# ============================================================================= CAMERAS
def camera(name, loc, tgt, lens, fstop=None):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_end = 5000; cd.clip_start = 0.1
    c = bpy.data.objects.new(name, cd); c.location = loc
    c.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); C_CAM.objects.link(c)
    if fstop: cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop; cd.dof.focus_distance = (Vector(tgt) - Vector(loc)).length
    return c
camera("Aerial_Hero",     (225, -110, 175), (86, 132, 0), 32)
camera("Aerial_Rear",     (-30, 40, 70), (80, 150, 0), 28)
camera("Aerial_Special",  (100, 195, 62), (24, 262, 0), 30)
camera("Aerial_Front",    (88, -118, 118), (86, 112, 0), 28)
camera("Aerial_Entrance", (185, -42, 48), (118, 24, 0), 30)
camera("Gate_Front",      (132.0, -22.0, 1.7), (132.4, 8.0, 3.2), 26, 11)
camera("Gate_Angle",      (110.0, -14.0, 1.8), (134.0, 6.0, 3.0), 30, 11)
camera("Shops_Front",     (125.5, 29.5, 1.75), (112.5, 15.5, 2.6), 24, 11)
camera("Pool",            (127.5, 33.0, 6.0), (98.0, 42.0, 0.0), 24)
camera("Pitch_Pool_Aerial", (150.0, 18.0, 30.0), (110.0, 48.0, 0.0), 28)
camera("Avenue",          (134.0, 78.0, 1.8), (133.0, 200.0, 3.0), 30, 16)
camera("Avenue_Drone",    (133.0, 30.0, 26.0), (128.0, 150.0, 0.0), 26)
camera("Commercial_Strip", (58.0, -16.0, 6.0), (92.0, 20.0, 1.0), 26)
camera("Lights_CCTV",     (127.6, 3.0, 1.7), (MED, 26.0, 6.2), 22, 8)
camera("Aerial_Dusk",     (225, -110, 175), (86, 132, 0), 32)
sc.camera = bpy.data.objects["Aerial_Hero"]
# film: 8 shots x 4 s, hard cuts, each shot eased; keyed every frame
def ease(x): return x * x * (3 - 2 * x)
SHOTS = [  # (pos0, pos1, tgt0, tgt1, lens)
    ((132, -95, 45), (132.5, -38, 14), (132, 60, 0), (132.5, 10, 3.5), 30),          # 1 approach over the highway to the gate
    ((136.2, -14, 1.9), (135.4, 22, 2.1), (134.6, 30, 1.6), (134.4, 70, 1.8), 26),    # 2 follow the car in through the gate
    ((140, -6, 11), (126, 40, 8), (110, 18, 2.5), (110, 18, 2.5), 26),                # 3 sweep around the gym + supermart
    ((129, 31, 3.2), (125, 30, 2.6), (104, 42, 0.4), (100, 46, 0.4), 24),             # 4 pool slide
    ((150, 32, 7), (152, 22, 34), (108, 56, 0), (106, 50, 0), 26),                    # 5 crane up over the pitch + pool
    ((133, 60, 20), (133, 220, 24), (131, 120, 0), (130, 285, 0), 28),                # 6 glide up the main avenue over the plots
    ((100, 195, 50), (150, 110, 85), (24, 262, 0), (75, 170, 0), 28),               # 7 special 700 plot -> rise to reveal
    ((215, -60, 100), (190, -38, 84), (88, 118, 0), (88, 120, 0), 30),              # 8 hero aerial, slow push in
]
SL = FR // len(SHOTS)
cd = bpy.data.cameras.new("Video_Cam"); cd.lens = 28; cd.clip_end = 5000
vc = bpy.data.objects.new("Video_Cam", cd); C_CAM.objects.link(vc)
for f in range(1, FR + 1):
    k = min(len(SHOTS) - 1, (f - 1) // SL); u = ease(((f - 1) - k * SL) / (SL - 1))
    a0, a1, t0, t1, lens = SHOTS[k]
    loc = Vector(a0).lerp(Vector(a1), u); tg = Vector(t0).lerp(Vector(t1), u)
    vc.location = loc; vc.rotation_euler = (tg - loc).to_track_quat('-Z', 'Y').to_euler(); cd.lens = lens
    vc.keyframe_insert("location", frame=f); vc.keyframe_insert("rotation_euler", frame=f); cd.keyframe_insert("lens", frame=f)
sc.frame_start, sc.frame_end = 1, FR; sc.render.fps = 24
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.35

exec(compile(open(f"{SP}/epe2/people.py").read(), "people.py", "exec"))
# ============================================================================= RENDER SETTINGS
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.01; sc.cycles.samples = 128
sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 6
sc.cycles.transparent_max_bounces = 24; sc.cycles.sample_clamp_indirect = 6.0; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
for v in ("AgX",):
    try: sc.view_settings.view_transform = v
    except TypeError: pass
for lk in ("AgX - Base Contrast", "Base Contrast"):
    try: sc.view_settings.look = lk; break
    except TypeError: continue
sc.render.film_transparent = False
sc.view_settings.exposure = -1.95
try:
    sc.view_settings.use_white_balance = False; sc.view_settings.white_balance_temperature = 6500; sc.view_settings.white_balance_tint = 0
except AttributeError: pass
sc.cycles.use_fast_gi = True; sc.cycles.ao_bounces_render = 2; sc.world.light_settings.distance = 12
# finishing grade (the Lumion/D5 look): soft bloom, gentle warm grade, light vignette
cg = bpy.data.node_groups.new("Grade", "CompositorNodeTree"); sc.compositing_node_group = cg
rl = cg.nodes.new("CompositorNodeRLayers")
gl = cg.nodes.new("CompositorNodeGlare")
for k, v in (("Type", "Bloom"), ("Quality", "High"), ("Threshold", 3.0), ("Smoothness", 0.2), ("Strength", 0.08), ("Size", 0.4)):
    try: gl.inputs[k].default_value = v
    except Exception: pass
cv = cg.nodes.new("CompositorNodeCurveRGB")
cm = cv.mapping; c = cm.curves[3]; c.points[0].location = (0.0, 0.02); c.points[1].location = (1.0, 1.0)
c.points.new(0.25, 0.22); c.points.new(0.75, 0.79)
rc = cm.curves[0]; rc.points.new(0.5, 0.515); bc = cm.curves[2]; bc.points.new(0.5, 0.49); cm.update()
el = cg.nodes.new("CompositorNodeEllipseMask")
try:
    el.inputs["Size"].default_value = (1.25, 1.25)
except Exception: pass
bl = cg.nodes.new("CompositorNodeBlur")
try: bl.inputs["Size"].default_value = (300, 300)
except Exception: pass
mx = cg.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
vg = cg.nodes.new("ShaderNodeMapRange"); vg.inputs["To Min"].default_value = 0.82; vg.inputs["To Max"].default_value = 1.0
go = cg.nodes.new("NodeGroupOutput"); cg.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
L = cg.links.new
L(rl.outputs["Image"], gl.inputs["Image"]); L(gl.outputs["Image"], cv.inputs["Image"])
L(el.outputs["Mask"], bl.inputs["Image"]); L(bl.outputs["Image"], vg.inputs["Value"])
mx.inputs[0].default_value = 1.0
L(cv.outputs["Image"], mx.inputs[6]); L(vg.outputs["Result"], mx.inputs[7]); L(mx.outputs[2], go.inputs[0])
sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transparent_max_bounces = 16
print("BUILD COMPLETE objects", len(bpy.data.objects), flush=True)
