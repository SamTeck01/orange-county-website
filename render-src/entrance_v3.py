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
    ld = bpy.data.lights.new("SignSpot", 'SPOT'); ld.energy = power; ld.spot_size = math.radians(70); ld.spot_blend = 0.6; ld.color = (1.0, 0.82, 0.6); ld.shadow_soft_size = 0.05
    lo = bpy.data.objects.new("SignSpot", ld); lo.location = (lx, -reach, top_z + 0.33)
    lo.rotation_euler = (math.radians(28), 0, 0); C_BUILD.objects.link(lo); lo.parent = par

# ---------- the bungalow gatehouse at the side (CAD square), gate opening beside it
GX0, GX1 = 134.6, 138.4
GY0, GY1 = y_edge(136.5) + 0.15, y_edge(136.5) + 5.3
Z0 = Z_WALK; zb = Z0 + 0.15; H = 3.1
gh = frame_at(136.5)
def L(x0, y0, z0, x1, y1, z1, mat, bev=0.0, name="GH"):
    o = box_at(name, x0, y0, z0, x1, y1, z1, mat, C_BUILD, bevel=bev); o.parent = gh; return o
w2 = (GX1 - GX0) / 2; d0, d1 = 0.15, 5.3
L(-w2 - 0.3, d0 - 0.3, Z_ROAD - Z_ROAD, w2 + 0.3, d1 + 0.3, zb - Z_ROAD, M_PANEL, name="GH_Plinth")
L(-w2, d0, zb, -w2 + 0.22, d1, zb + H, M_CLAD, name="GH_Wall_W_clad")                 # faces the gate lane
L(w2 - 0.2, d0, zb, w2, d1, zb + H, M_PLASTER, name="GH_Wall_E")
L(-w2, d1 - 0.2, zb, w2, d1, zb + H, M_PLASTER, name="GH_Wall_N")
L(-w2, d0, zb, w2, d0 + 0.2, zb + 0.9, M_PLASTER, name="GH_Wall_S_lo")
L(-w2 + 0.25, d0 + 0.06, zb + 0.9, w2 - 0.25, d0 + 0.12, zb + H - 0.3, M_GLASS, name="GH_Glass_S")
for xx in (-w2 + 0.25, 0, w2 - 0.25): L(xx - 0.04, d0 + 0.03, zb + 0.9, xx + 0.04, d0 + 0.15, zb + H - 0.3, M_ALU, name="GH_Mullion")
L(-w2, d0, zb + H - 0.3, w2, d0 + 0.2, zb + H, M_PLASTER, name="GH_Header")
L(-w2 - 0.02, 1.4, zb + 1.0, -w2 + 0.24, 3.6, zb + 2.3, M_GLASS_D, name="GH_SideWindow")   # guard window onto the gate lane
L(-w2 + 0.3, 0.6, zb, -w2 + 0.9, 4.6, zb + 0.85, M_CLAD, name="GH_Desk")
L(-w2, d0, zb, w2, d1, zb + 0.05, M_PATIO, name="GH_Floor")
L(-w2 + 0.6, d0 + 0.6, zb + H - 0.12, w2 - 0.6, d1 - 0.6, zb + H - 0.08, M_LED, name="GH_CeilLight")
L(w2 - 0.05, 2.0, zb + 2.0, w2 + 0.45, 2.9, zb + 2.6, M_WHITE, bev=0.02, name="GH_AC")
t = text("SECURITY", (0, d0 - 0.02, zb + H - 0.15), 0.26, M_LABEL, C_BUILD, rot=(math.radians(90), 0, 0), extrude=0.05); t.parent = gh

# ---------- canopy over the gate opening and the gatehouse (the design the client liked)
GATE_X0, GATE_X1 = 127.3, GX0                         # 7.3 m clear: two cars pass side by side
cx_mid = (GATE_X0 + GX1) / 2; cv = frame_at(cx_mid)
def CV(x0, y0, z0, x1, y1, z1, mat, name="CV", bev=0.0):
    o = box_at(name, x0, y0, z0, x1, y1, z1, mat, C_BUILD, bevel=bev); o.parent = cv; return o
half = (GX1 - GATE_X0) / 2 + 0.6; CZ = 5.6
CV(-half + 0.1, 0.2, Z_WALK, -half + 1.0, 4.8, CZ, M_PANEL, name="Canopy_Pier_W")
CV(half - 1.0, 0.2, zb + H, half - 0.1, 4.8, CZ, M_PANEL, name="Canopy_Pier_E")
CV(-half - 0.2, -0.8, CZ, half + 0.2, 5.9, CZ + 0.55, M_WHITE, name="Canopy_Slab")
CV(-half - 0.22, -0.86, CZ + 0.05, half + 0.22, -0.8, CZ + 0.62, M_CHAR, name="Canopy_Fascia")
CV(-half + 0.3, -0.5, CZ - 0.02, half - 0.3, -0.4, CZ, M_LED, name="Canopy_LED")
t = text("ORANGE COUNTY", (0.9, -0.88, CZ + 0.34), 0.42, M_LABEL_O, C_BUILD, font=FS, rot=(math.radians(90), 0, 0), extrude=0.08); t.parent = cv
lg = logo3d(0.62, 0.06, C_BUILD); lg.parent = cv; lg.location = (-2.9, -0.9, CZ + 0.34); lg.rotation_euler = (math.radians(90), 0, 0)
for k in range(6):                                    # down-lights under the canopy
    CV(-half + 1.4 + k * (2 * half - 2.8) / 5 - 0.12, 2.3, CZ - 0.03, -half + 1.4 + k * (2 * half - 2.8) / 5 + 0.12, 2.6, CZ, M_LEDW, name="Canopy_Downlight")

# ---------- sliding gate (parks behind the feature wall when open), boom barriers inside
gate_par = frame_at(GATE_X0 - 4.1, inset=0.0)
for i in range(38):
    o = box_at("GateBar", -3.8 + i * 0.2, 1.05, Z_WALK + 0.15, -3.8 + i * 0.2 + 0.05, 1.12, Z_WALK + 2.25, M_ALU, C_BUILD); o.parent = gate_par
for zz in (0.15, 1.2, 2.2):
    o = box_at("GateRail", -3.85, 1.03, Z_WALK + zz, 3.85, 1.14, Z_WALK + zz + 0.08, M_ALU, C_BUILD); o.parent = gate_par
o = box_at("GateTrack", -8, 0.95, Z_ROAD, 8, 1.2, Z_ROAD + 0.03, M_STEEL, C_BUILD); o.parent = gate_par
for (px, py, L_, sgn) in ((132.7, 10.0, 4.4, -1), (138.0, 10.0, 4.3, -1)):
    box_at("Boom_Post", px - 0.18, py - 0.18, Z_WALK, px + 0.18, py + 0.18, Z_WALK + 1.05, M_ORANGE, C_BUILD, bevel=0.02)
    cube("Boom_Arm", (px + sgn * L_ / 2, py, Z_WALK + 0.95), (L_, 0.07, 0.07), M_WHITE, C_BUILD)
    for k in range(int(L_ / 0.6)):
        cube("Boom_Stripe", (px + sgn * (0.3 + k * 0.6), py, Z_WALK + 0.95), (0.25, 0.075, 0.075), M_ORANGE, C_BUILD)
mesh_from_poly("Median", LineString([(132.7, 9.6), (132.7, 20.2)]).buffer(0.56, cap_style=1), Z_ROAD, Z_WALK + 0.05, M_CURB, C_BUILD)
mesh_from_poly("Median_Planting", LineString([(132.7, 10.6), (132.7, 19.6)]).buffer(0.38, cap_style=1), Z_WALK, Z_WALK + 0.12, M_LAWN, C_BUILD)

# ---------- feature wall west of the gate: 3D logo + "Welcome to ORANGE COUNTY · Epe, Lagos", lit from above
FW_X0, FW_X1 = 111.6, GATE_X0 - 0.4
fw = frame_at((FW_X0 + FW_X1) / 2); fl = (FW_X1 - FW_X0) / 2; FH = 3.1
def FWB(x0, y0, z0, x1, y1, z1, mat, name="FW", bev=0.0):
    o = box_at(name, x0, y0, z0, x1, y1, z1, mat, C_BUILD, bevel=bev); o.parent = fw; return o
FWB(-fl - 0.2, -0.55, Z_ROAD - 0.02, fl + 0.2, 0.55, 0.45, M_PANEL, name="FW_Base")
FWB(-fl, -0.32, 0.45, fl, 0.32, FH, M_SIGNPANEL, name="FW_Wall")
FWB(-fl - 0.1, -0.4, FH, fl + 0.1, 0.4, FH + 0.14, M_CHAR, name="FW_Cap")
FWB(-fl + 0.25, -0.36, 0.7, fl - 0.25, -0.33, 0.78, M_ORANGE_FRAME, name="FW_FrameB")
FWB(-fl + 0.25, -0.36, FH - 0.32, fl - 0.25, -0.33, FH - 0.24, M_ORANGE_FRAME, name="FW_FrameT")
for xx in (-fl + 0.25, fl - 0.33): FWB(xx, -0.36, 0.7, xx + 0.08, -0.33, FH - 0.24, M_ORANGE_FRAME, name="FW_FrameS")
FWB(-fl + 0.4, -0.35, 0.5, fl - 0.4, -0.33, 0.55, M_LED, name="FW_UpLED")
lg = logo3d(2.05, 0.12, C_BUILD); lg.parent = fw; lg.location = (fl - 1.75, -0.36, 1.85); lg.rotation_euler = (math.radians(90), 0, 0)
tx_c = -1.4
for (body, size, mat, z, font, ext) in (("Welcome to", 0.38, M_BROWN, 2.42, FS, 0.08), ("ORANGE COUNTY", 0.72, M_LABEL_O, 1.78, FS, 0.12),
                                         ("E P E   ·   L A G O S", 0.24, M_BROWN, 1.18, FB, 0.08)):
    t = text(body, (tx_c, -0.37, z), size, mat, C_BUILD, font=font, rot=(math.radians(90), 0, 0), extrude=ext, bevel=0.012); t.parent = fw
for xx in (tx_c - 3.2, tx_c + 3.2):
    FWB(xx - 1.0, -0.36, 1.165, xx + 1.0, -0.34, 1.195, M_ORANGE_FRAME, name="FW_Rule")
for lx in [-fl + 1.0 + k * (2 * fl - 2.0) / 5 for k in range(6)]:
    gooseneck(fw, lx, FH + 0.14)
for i in range(16):                                   # flower bed along the wall base
    e = inst(R.choice(FLOWERS), R.uniform(-fl, fl), R.uniform(-1.25, -0.7), Z_ROAD + 0.4, R.uniform(0.7, 1.0)); e.parent = fw
FWB(-fl, -1.45, Z_ROAD - 0.02, fl, -0.55, 0.4, M_PANEL, name="FW_Planter")

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
EXCL = [Polygon([(GATE_X0 - 0.4, y_edge(GATE_X0) - 2), (GX0, y_edge(GX0) - 2), (GX0, y_edge(GX0) + 2.2), (GATE_X0 - 0.4, y_edge(GATE_X0) + 2.2)]),
        box(GX0 - 0.2, y_edge(GX1) - 1.0, GX1 + 0.4, y_edge(GX1) + 5.6),
        Polygon([(FW_X0 - 0.1, y_edge(FW_X0) - 1.2), (FW_X1 + 0.1, y_edge(FW_X1) - 1.2), (FW_X1 + 0.1, y_edge(FW_X1) + 1.2), (FW_X0 - 0.1, y_edge(FW_X0) + 1.2)])]
EXU = unary_union(EXCL)
segs_built = 0
for i in range(len(ring) - 1):
    seg = LineString([ring[i], ring[i + 1]])
    if seg.length < 0.3: continue
    rest = seg.difference(EXU)
    for j, piece in enumerate(getattr(rest, "geoms", [rest])):
        if piece.is_empty or piece.length < 0.4: continue
        a, b = piece.coords[0], piece.coords[-1]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if front_dist(mx, my) < 1.2: deco_fence(a, b, f"Front{i}_{j}")
        else: wall_run(a, b, f"Fence{i}_{j}")
        segs_built += 1
print("fence segments", segs_built, flush=True)
