# Neighbourhood houses around the estate (client: houses around, none sharing our fence).
# Six prototypes (bungalows + duplexes, each in its own walled compound) instanced on loose street grids.
C_HPROTO = bpy.data.collections.new("HouseProtos")
M_ROOF = [flat("Roof_Red", (0.42, 0.10, 0.06), rough=0.6), flat("Roof_Grey", (0.22, 0.23, 0.25), rough=0.55),
          flat("Roof_Brown", (0.28, 0.16, 0.09), rough=0.6), flat("Roof_Blue", (0.10, 0.18, 0.32), rough=0.5)]
M_HWALL = [M_CREAM, M_PLASTER, flat("Wall_Peach", (0.86, 0.66, 0.50), rough=0.8), flat("Wall_Sand", (0.80, 0.72, 0.58), rough=0.8)]
M_HGATE = flat("Compound_Gate", (0.10, 0.10, 0.11), rough=0.5, metal=0.6)
def hip_roof(name, w, d, z, h, mat, col):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= w + 1.2; v.co.y *= d + 1.2
        if v.co.z > 0:
            v.co.z = h
            if w >= d: v.co.y = 0; v.co.x *= max(0.05, (w - d) / w)
            else: v.co.x = 0; v.co.y *= max(0.05, (d - w) / d)
        else: v.co.z = 0
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); me.materials.append(mat); o.location.z = z; col.objects.link(o); return o
def proto(i, w, d, storeys, wall, roof):
    col = bpy.data.collections.new(f"House{i}"); C_HPROTO.children.link(col)
    H = 3.2 * storeys
    box_at("H_Body", -w / 2, -d / 2, 0, w / 2, d / 2, H, wall, col)
    box_at("H_Plinth", -w / 2 - 0.1, -d / 2 - 0.1, 0, w / 2 + 0.1, d / 2 + 0.1, 0.45, M_CHAR if i % 2 else M_STONE, col)
    if storeys == 2: box_at("H_Band", -w / 2 - 0.15, -d / 2 - 0.15, 3.1, w / 2 + 0.15, d / 2 + 0.15, 3.3, M_WHITE, col)
    hip_roof("H_Roof", w, d, H, 2.0, roof, col)
    for s in range(storeys):
        z0 = 0.9 + s * 3.2
        for k in range(int(w // 3.2)):
            x = -w / 2 + 1.6 + k * 3.2
            for sy in (-1, 1): box_at("H_Win", x - 0.7, sy * d / 2 - 0.06, z0, x + 0.7, sy * d / 2 + 0.06, z0 + 1.4, M_GLASS_D, col)
        for k in range(int(d // 3.4)):
            y = -d / 2 + 1.7 + k * 3.4
            for sx in (-1, 1): box_at("H_Win", sx * w / 2 - 0.06, y - 0.6, z0, sx * w / 2 + 0.06, y + 0.6, z0 + 1.4, M_GLASS_D, col)
    box_at("H_Door", -0.6, -d / 2 - 0.08, 0.45, 0.6, -d / 2 + 0.02, 2.6, M_CLAD, col)
    box_at("H_Porch", -1.8, -d / 2 - 2.4, 2.9, 1.8, -d / 2, 3.1, M_WHITE, col)
    for sx in (-1.6, 1.6): box_at("H_PorchCol", sx - 0.15, -d / 2 - 2.3, 0, sx + 0.15, -d / 2 - 2.0, 2.9, M_WHITE, col)
    # walled compound with a black gate (typical Lagos plot)
    cw, cd_ = w / 2 + 4.5, d / 2 + 5.5
    for (x0, y0, x1, y1) in ((-cw, cd_ - 0.2, cw, cd_), (-cw, -cd_, -cw + 0.2, cd_), (cw - 0.2, -cd_, cw, cd_), (-cw, -cd_, -2.0, -cd_ + 0.2), (2.0, -cd_, cw, -cd_ + 0.2)):
        box_at("H_Fence", x0, y0, 0, x1, y1, 2.1, wall, col); box_at("H_FenceCap", x0 - 0.05, y0 - 0.05, 2.1, x1 + 0.05, y1 + 0.05, 2.2, M_CHAR, col)
    box_at("H_Gate", -2.0, -cd_, 0.05, 2.0, -cd_ + 0.12, 2.0, M_HGATE, col)
    box_at("H_Yard", -cw, -cd_, 0.0, cw, cd_, 0.06, M_PAVERS, col)
    return col
PROTOS = [proto(0, 12, 10, 1, M_HWALL[0], M_ROOF[0]), proto(1, 14, 11, 2, M_HWALL[1], M_ROOF[1]), proto(2, 11, 9, 1, M_HWALL[2], M_ROOF[2]),
          proto(3, 13, 12, 2, M_HWALL[3], M_ROOF[3]), proto(4, 15, 10, 1, M_HWALL[1], M_ROOF[0]), proto(5, 12, 11, 2, M_HWALL[0], M_ROOF[2])]
C_HOUSES = sub("09_Neighbourhood")
KEEP_OUT = ESTATE.buffer(30).union(strip(-12, 26)).union(VIEW_CLEAR)
def neighbourhood(xs, ys, rot):
    n = 0
    for x in xs:
        for y in ys:
            if R.random() < 0.80: continue
            px, py = x + R.uniform(-3, 3), y + R.uniform(-3, 3)
            if KEEP_OUT.intersects(Point(px, py).buffer(13)): continue
            e = inst(R.choice(PROTOS), px, py, terrain_h(px, py), 1.0, rz=rot + R.choice((0, math.pi)) + R.uniform(-0.04, 0.04), col=C_HOUSES); n += 1
            if R.random() < 0.5: inst(pick_tree(), px + R.uniform(-9, 9), py + R.choice((-13, 13)), terrain_h(px, py), R.uniform(1.6, 2.6))
    return n
nh = neighbourhood(range(-110, -30, 30), range(-10, 330, 32), math.radians(90))      # west
nh += neighbourhood(range(-100, 280, 32), range(330, 400, 32), 0)                      # north
nh += neighbourhood(range(205, 290, 30), range(-10, 330, 32), math.radians(90))       # east
nh += neighbourhood(range(-60, 320, 32), range(-110, -40, 30), math.radians(-5.2))   # across the highway
print("houses", nh, flush=True)
