# Oyo-style finishing: zebra crossings at every junction, denser tree clusters near the estate.
from shapely.prepared import prep
ROADS = ESTATE.buffer(-0.4).difference(walk.buffer(0.05)); PR = prep(ROADS)
def extent(x, y, dx, dy, lim=40):
    n = 0
    for s in (1, -1):
        k = 0
        while k < lim and PR.contains(Point(x + s * dx * (k + 1), y + s * dy * (k + 1))): k += 1
        n += k
    return n
# junction cells: road runs on in both axes from here
pts = []
minx, miny, maxx, maxy = ROADS.bounds
for gx in range(int(minx), int(maxx) + 1, 2):
    for gy in range(int(miny), int(maxy) + 1, 2):
        if PR.contains(Point(gx, gy)) and extent(gx, gy, 1, 0) > 16 and extent(gx, gy, 0, 1) > 16:
            pts.append((gx, gy))
print("roads area", round(ROADS.area), "jpts", len(pts), "walk", round(walk.area), flush=True)
JCT = unary_union([Point(p).buffer(1.5) for p in pts])
JCT = list(JCT.geoms) if hasattr(JCT, "geoms") else [JCT]
def zebra(cx, cy, horiz, width):
    # stripes run along the traffic direction, laid across the road
    n = int(width / 1.0)
    for i in range(n):
        o = -width / 2 + 0.5 + i * 1.0
        x0, y0 = (cx - 1.4, cy + o - 0.25) if horiz else (cx + o - 0.25, cy - 1.4)
        x1, y1 = (cx + 1.4, cy + o + 0.25) if horiz else (cx + o + 0.25, cy + 1.4)
        box_at("Zebra", x0, y0, Z_ROAD, x1, y1, Z_ROAD + 0.012, M_LINE, C_GROUND)
nz = 0
for j in JCT:
    c = j.centroid; minx_, miny_, maxx_, maxy_ = j.buffer(6).bounds
    for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        # step out of the junction along this arm, put the crossing where the road narrows to its normal width
        for step in range(4, 22):
            x, y = c.x + dx * step, c.y + dy * step
            if not PR.contains(Point(x, y)): break
            w = extent(x, y, abs(dy), abs(dx), 8)
            if w < 14:
                # first narrow point is the junction mouth; set the crossing 2 m further along
                x2, y2 = x + dx * 2, y + dy * 2
                if PR.contains(Point(x2, y2)):
                    zebra(x2, y2, dx != 0, max(4, extent(x2, y2, abs(dy), abs(dx), 8)))
                    nz += 1
                break
print("zebra crossings", nz, flush=True)

# denser Oyo-like clusters of warm and green trees in a ring 20-70 m out
for k in range(48):
    a = R.uniform(0, 6.283); d = R.uniform(115, 175)
    cx_, cy_ = 85 + math.cos(a) * d * 0.75, 140 + math.sin(a) * d * 1.15
    for j in range(R.randint(8, 16)):
        x, y = cx_ + R.gauss(0, 7), cy_ + R.gauss(0, 7)
        if ESTATE.buffer(18).contains(Point(x, y)) or strip(-12, 26).contains(Point(x, y)) or VIEW_CLEAR.contains(Point(x, y)): continue
        inst(R.choices(["gold_cone", "flame_tree", "gold_tree", "tree_small_02", "island_tree_01"], [6, 2, 2, 3, 1])[0], x, y, terrain_h(x, y), R.uniform(1.8, 3.0))

# Oyo-style planting: one neat clipped hedge with a flower band in front, only at the foot of the walls by the gate
M_BEDFLOWERS = M_FLOWERHEDGE.copy(); M_GATEHEDGE = M_FLOWERHEDGE.copy()
for m, th, vs, ns in ((M_BEDFLOWERS, 0.60, 26.0, 9.0), (M_GATEHEDGE, 0.97, 9.0, 14.0)):
    for n in m.node_tree.nodes:
        if n.type == 'MATH' and n.operation == 'GREATER_THAN': n.inputs[1].default_value = th
        if n.type == 'TEX_VORONOI': n.inputs["Scale"].default_value = vs
        if n.type == 'TEX_NOISE': n.inputs["Scale"].default_value = ns
for (x0, x1) in ((SG_X0 - 14.0, SG_X1 + 0.2), (GX1 + 0.6, GX1 + 22.0)):
    def band(d0, d1, z1, mat, nm):
        pts = [(x0, y_edge(x0) - d1), (x1, y_edge(x1) - d1), (x1, y_edge(x1) - d0), (x0, y_edge(x0) - d0)]
        o = mesh_from_poly(nm, Polygon(pts), Z_WALK, z1, mat, C_BUILD)
        if o:
            bv = o.modifiers.new("round", 'BEVEL'); bv.width = 0.15; bv.segments = 4
    band(0.05, 0.6, Z_WALK + 0.8, M_GATEHEDGE, "Gate_Hedge")
    band(0.6, 1.1, Z_WALK + 0.38, M_BEDFLOWERS, "Gate_Flowers")
