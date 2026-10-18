# =============================================================================
# ORANGE COUNTY EPE — full scene builder (Blender 5.x, Cycles)
# Layout: exact plot polygons from SAKA_EPE_LAYOUT (vector PDF).
# Client notes: Block B = right 450 column; Block A + bottom-right 600 are
# commercial and face out to the road; open space = gym + supermart;
# facilities = swimming pool & subordinates with a football pitch above it;
# gatehouse = bungalow at the CAD square; 600 & 700 sqm plots are special.
# =============================================================================
import bpy, bmesh, json, math, random, os, sys
from mathutils import Vector, Matrix, Euler
from mathutils.geometry import tessellate_polygon
from shapely.geometry import Polygon, MultiPolygon, LineString, Point, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

SP = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad"
LAY, TEX, HDRI = f"{SP}/layout", f"{SP}/assets/ph/tex", f"{SP}/assets/ph/hdri"
LIB = f"{SP}/epe2/lib.blend"
LOGO = "/home/user/orange-county-website/public/brand/orange-county-logo.png"
FONT_B = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FONT_S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
R = random.Random(2026)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'
FB = bpy.data.fonts.load(FONT_B); FS = bpy.data.fonts.load(FONT_S)

def coll(name, parent=None):
    c = bpy.data.collections.new(name); (parent or sc.collection).children.link(c) if parent else sc.collection.children.link(c); return c
C_ROOT = bpy.data.collections.new("OrangeCounty_Epe"); sc.collection.children.link(C_ROOT)
def sub(n):
    c = bpy.data.collections.new(n); C_ROOT.children.link(c); return c
C_GROUND, C_PLOTS, C_LABELS, C_BUILD, C_VEG, C_PROPS, C_CAM = (sub(n) for n in
    ("01_Ground_Roads", "02_Plots", "03_Labels", "04_Buildings", "05_Vegetation", "06_Props", "07_Cameras"))

# ----------------------------------------------------------------------------- layout
LJ = json.load(open(f"{LAY}/regions.json")); XF = json.load(open(f"{LAY}/xf.json"))
S, X0, Y1 = XF["S"], XF["X0"], XF["Y1"]
def M(p): return ((p[0] - X0) * S, (Y1 - p[1]) * S)
ESTATE = orient(Polygon([M(p) for p in LJ["estate"]]).buffer(0), 1.0)
regs = []
for o in LJ["regions"]:
    poly = orient(Polygon([M(p) for p in o["coords"]]).buffer(0), 1.0)
    regs.append(dict(kind=o["kind"], m2=o["m2"], poly=poly))

def split_poly(poly, n):
    """CAD regions where a division line was missing: split along the long axis into n equal plots."""
    x0, y0, x1, y1 = poly.bounds; out = []
    for i in range(n):
        if (x1 - x0) > (y1 - y0): b = box(x0 + (x1 - x0) * i / n, y0 - 1, x0 + (x1 - x0) * (i + 1) / n, y1 + 1)
        else: b = box(x0 - 1, y0 + (y1 - y0) * i / n, x1 + 1, y0 + (y1 - y0) * (i + 1) / n)
        out.append(poly.intersection(b))
    return out

PLOTS, OPEN_SPACE, FACILITY, SPECIAL700 = [], None, None, None
for r in regs:
    k, a = r["kind"], r["m2"]
    if k == "g": FACILITY = r["poly"]; continue
    if k == "none":
        if a > 3000: continue                       # road network
        if 650 < a < 900: SPECIAL700 = r["poly"]; continue
        OPEN_SPACE = r["poly"]; continue
    size = {"b": 300, "c": 450, "r": 600}[k]
    n = max(1, round(a / (size + 20)))
    for p in (split_poly(r["poly"], n) if n > 1 else [r["poly"]]):
        PLOTS.append(dict(size=size, poly=orient(p.buffer(0.55, join_style=2), 1.0)))
PLOTS.append(dict(size=700, poly=orient(SPECIAL700.buffer(0.55, join_style=2), 1.0)))

# Block assignment (client: B = right 450 column; A = bottom row, commercial; others named by us)
def block_of(p):
    c = p["poly"].centroid; x, y, s = c.x, c.y, p["size"]
    if s == 700: return "700"
    if y < 30: return "A"                      # bottom row (estate edge slants) + the corner commercial 600
    if x > 138: return "B" if s == 450 else "C"
    if x > 82: return "D" if s == 300 else "E"
    if x < 31: return "G"
    if y > 250: return "F"
    return "H" if s == 450 else "I"
for p in PLOTS: p["block"] = block_of(p)
for b in sorted(set(p["block"] for p in PLOTS)):
    key = (lambda p: p["poly"].centroid.x) if b == "A" else (lambda p: (round(p["poly"].centroid.y / 6), p["poly"].centroid.x))
    ps = sorted([p for p in PLOTS if p["block"] == b], key=key)
    for i, p in enumerate(ps, 1): p["num"] = i
print("plots", len(PLOTS), {b: sum(1 for p in PLOTS if p["block"] == b) for b in sorted(set(p["block"] for p in PLOTS))})

# ----------------------------------------------------------------------------- mesh helpers
def mesh_from_poly(name, geom, z0, z1, mat, col, sides=True):
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    verts, faces = [], []
    for pg in polys:
        if pg.is_empty or pg.area < 0.01: continue
        pg = orient(pg, 1.0)
        rings = [list(pg.exterior.coords)[:-1]] + [list(h.coords)[:-1] for h in pg.interiors]
        rings3 = [[Vector((x, y, z1)) for x, y in r] for r in rings]
        base = len(verts); flat = [v for r in rings3 for v in r]; verts += flat
        for tri in tessellate_polygon(rings3): faces.append([base + i for i in tri])
        if sides:
            off = base
            for r in rings3:
                n = len(r)
                bot0 = len(verts); verts += [Vector((v.x, v.y, z0)) for v in r]
                for i in range(n):
                    j = (i + 1) % n
                    faces.append([off + i, bot0 + i, bot0 + j, off + j])
                off += n
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], faces); me.validate()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o)
    if mat: me.materials.append(mat)
    return o

def cube(name, loc, size, mat, col, rot=(0, 0, 0), bevel=0.0):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    if bevel: bmesh.ops.bevel(bm, geom=bm.edges[:] + bm.verts[:], offset=bevel, segments=3, affect='EDGES')
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc; o.rotation_euler = rot
    if mat: me.materials.append(mat)
    col.objects.link(o); return o

def box_at(name, x0, y0, z0, x1, y1, z1, mat, col, bevel=0.0):
    return cube(name, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)), mat, col, bevel=bevel)

def cyl(name, loc, r, h, mat, col, verts=16, rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=r, depth=h)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); o.location = loc; o.rotation_euler = rot; me.materials.append(mat); col.objects.link(o); return o

def tube(name, pts, r, mat, col, res=3):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = res; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, c in zip(sp.points, pts): p.co = (c[0], c[1], c[2], 1)
    o = bpy.data.objects.new(name, cu); o.data.materials.append(mat); col.objects.link(o); return o

def text(body, loc, size, mat, col, font=None, rot=(0, 0, 0), extrude=0.08, align='CENTER', bevel=0.01):
    cu = bpy.data.curves.new("T_" + body[:12], 'FONT'); cu.body = body; cu.size = size; cu.font = font or FB
    cu.extrude = size * extrude; cu.bevel_depth = size * bevel; cu.align_x = align; cu.align_y = 'CENTER'
    o = bpy.data.objects.new("T_" + body[:12], cu); o.location = loc; o.rotation_euler = rot
    cu.materials.append(mat); col.objects.link(o); return o

# ----------------------------------------------------------------------------- materials
def _nodes(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    return m, nt, nt.nodes["Principled BSDF"]

def pbr(name, tex, tile=2.0, tint=None, rough_mul=1.0, bump=1.0, var=0.0, var_scale=0.05, proj='BOX'):
    """Poly Haven PBR set, box-projected in object space (objects are built in world metres)."""
    m, nt, b = _nodes(name)
    d = f"{TEX}/{tex}"
    files = {k: next((f"{d}/{f}" for f in os.listdir(d) if f"_{k}_" in f), None) for k in ("Diffuse", "nor_gl", "Rough", "AO")}
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1 / tile,) * 3
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    def img(path, noncolor):
        n = nt.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(path, check_existing=True)
        if noncolor: n.image.colorspace_settings.name = 'Non-Color'
        n.projection = proj; n.projection_blend = 0.25; nt.links.new(mp.outputs["Vector"], n.inputs["Vector"]); return n
    col_out = None
    if files["Diffuse"]:
        di = img(files["Diffuse"], False); col_out = di.outputs["Color"]
        if tint:
            mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs["Factor"].default_value = 1
            nt.links.new(col_out, mx.inputs[6]); mx.inputs[7].default_value = (*tint, 1); col_out = mx.outputs[2]
        if var:
            nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = var_scale; nz.inputs["Detail"].default_value = 3
            geo = nt.nodes.new("ShaderNodeNewGeometry"); nt.links.new(geo.outputs["Position"], nz.inputs["Vector"])
            rp = nt.nodes.new("ShaderNodeValToRGB"); rp.color_ramp.elements[0].color = ((1 - var),) * 3 + (1,); rp.color_ramp.elements[1].color = ((1 + var * 0.6),) * 3 + (1,)
            nt.links.new(nz.outputs["Fac"], rp.inputs["Fac"])
            mv = nt.nodes.new("ShaderNodeMix"); mv.data_type = 'RGBA'; mv.blend_type = 'MULTIPLY'; mv.inputs["Factor"].default_value = 1
            nt.links.new(col_out, mv.inputs[6]); nt.links.new(rp.outputs["Color"], mv.inputs[7]); col_out = mv.outputs[2]
        nt.links.new(col_out, b.inputs["Base Color"])
    if files["Rough"]:
        ro = img(files["Rough"], True)
        if rough_mul != 1.0:
            mm = nt.nodes.new("ShaderNodeMath"); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = rough_mul
            nt.links.new(ro.outputs["Color"], mm.inputs[0]); nt.links.new(mm.outputs[0], b.inputs["Roughness"])
        else: nt.links.new(ro.outputs["Color"], b.inputs["Roughness"])
    if files["nor_gl"] and bump > 0:
        no = img(files["nor_gl"], True); nm = nt.nodes.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = bump
        nt.links.new(no.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    return m

def flat(name, rgb, rough=0.5, metal=0.0, emit=None, es=0.0, alpha=1.0, transmission=0.0, ior=1.45, coat=0.0):
    m, nt, b = _nodes(name)
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = es
    if alpha < 1: b.inputs["Alpha"].default_value = alpha; m.surface_render_method = 'BLENDED'
    if transmission: b.inputs["Transmission Weight"].default_value = transmission; b.inputs["IOR"].default_value = ior
    if coat: b.inputs["Coat Weight"].default_value = coat
    return m

M_LAWN    = pbr("Lawn", "leafy_grass", tile=3.0, tint=(0.70, 0.95, 0.50), bump=0.6, var=0.12, var_scale=0.08)
M_WILD    = pbr("Wild_Ground", "leafy_grass", tile=9.0, tint=(0.05, 0.10, 0.03), bump=0.4, var=0.10, var_scale=0.01)
M_ASPHALT = pbr("Asphalt", "asphalt_02", tile=5.0, tint=(0.24, 0.26, 0.32), bump=0.6)
M_PAVERS  = pbr("Pavers", "concrete_pavement", tile=2.0, tint=(0.95, 0.95, 0.93), bump=0.4)
M_CURB    = pbr("Curb", "concrete_pavement", tile=1.5, tint=(1.0, 1.0, 1.0), bump=0.4)
M_PLASTER = pbr("Plaster_White", "white_plaster_02", tile=2.5, tint=(1.0, 0.98, 0.94), bump=0.5)
M_CREAM   = pbr("Plaster_Cream", "white_plaster_02", tile=2.5, tint=(0.93, 0.86, 0.74), bump=0.5)
M_DECK    = pbr("Wood_Deck", "wood_floor_deck", tile=2.0, tint=(0.95, 0.85, 0.75), bump=0.6)
M_POOLTILE= pbr("Pool_Tile", "blue_floor_tiles_01", tile=1.2, bump=0.5)
M_CLAD    = pbr("Wood_Clad", "wood_planks_grey", tile=2.0, tint=(0.75, 0.55, 0.40), bump=0.6)
M_PANEL   = pbr("Concrete_Panel", "concrete_panels", tile=3.0, tint=(0.55, 0.56, 0.58), bump=0.5)
M_PATIO   = pbr("Patio", "patio_tiles", tile=2.0, tint=(1.0, 0.97, 0.92), bump=0.5)
M_LATERITE= pbr("Laterite", "forrest_ground_01", tile=4.0, tint=(0.95, 0.55, 0.35), bump=0.6)
M_GLASS   = flat("Glass", (0.6, 0.7, 0.72), rough=0.02, transmission=1.0, ior=1.5)
M_GLASS_D = flat("Glass_Dark", (0.10, 0.13, 0.15), rough=0.05, metal=0.2, coat=1.0)
M_ALU     = flat("Aluminium_Dark", (0.06, 0.06, 0.065), rough=0.35, metal=0.9)
M_STEEL   = flat("Steel", (0.55, 0.56, 0.58), rough=0.3, metal=1.0)
M_BLACK   = flat("Matte_Black", (0.02, 0.02, 0.02), rough=0.6)
M_CHAR    = flat("Charcoal", (0.06, 0.065, 0.07), rough=0.55)
M_WHITE   = flat("White", (0.62, 0.62, 0.60), rough=0.6)
M_ORANGE  = flat("OC_Orange", (1.0, 0.24, 0.0), rough=0.35)
M_GREEN   = flat("OC_Green", (0.0, 0.22, 0.04), rough=0.4)
M_LABEL   = flat("Label_White", (1, 1, 1), rough=0.3, emit=(1, 1, 1), es=0.35)
M_LABEL_O = flat("Label_Orange", (1.0, 0.28, 0.0), rough=0.4, emit=(1, 0.22, 0.0), es=0.3)
M_LED     = flat("LED_Warm", (1, 0.9, 0.75), emit=(1, 0.85, 0.65), es=8.0)
M_LEDW    = flat("LED_Cool", (1, 1, 1), emit=(1, 0.98, 0.95), es=12.0)
M_PANEL_S = flat("Solar_Panel", (0.02, 0.04, 0.10), rough=0.15, metal=0.4, coat=1.0)
M_LINE    = flat("Line_White", (0.95, 0.95, 0.93), rough=0.6)
M_TURF    = pbr("Turf", "leafy_grass", tile=1.2, tint=(0.35, 0.75, 0.30), bump=0.3)
M_WATER = bpy.data.materials.new("Pool_Water"); M_WATER.use_nodes = True
_nt = M_WATER.node_tree; _b = _nt.nodes["Principled BSDF"]
_b.inputs["Base Color"].default_value = (0.02, 0.42, 0.55, 1); _b.inputs["Roughness"].default_value = 0.03; _b.inputs["IOR"].default_value = 1.333
_b.inputs["Coat Weight"].default_value = 1.0; _b.inputs["Coat Roughness"].default_value = 0.02
_b.inputs["Subsurface Weight"].default_value = 0.6; _b.inputs["Subsurface Radius"].default_value = (0.2, 0.9, 1.2); _b.inputs["Subsurface Scale"].default_value = 0.4
_wn = _nt.nodes.new("ShaderNodeTexNoise"); _wn.inputs["Scale"].default_value = 2.5; _wn.inputs["Detail"].default_value = 5
_wb = _nt.nodes.new("ShaderNodeBump"); _wb.inputs["Strength"].default_value = 0.12
_nt.links.new(_wn.outputs["Fac"], _wb.inputs["Height"]); _nt.links.new(_wb.outputs["Normal"], _b.inputs["Normal"]); _nt.links.new(_wb.outputs["Normal"], _b.inputs["Coat Normal"])
M_LOGO = bpy.data.materials.new("Logo"); M_LOGO.use_nodes = True
_nt = M_LOGO.node_tree; _b = _nt.nodes["Principled BSDF"]; _im = _nt.nodes.new("ShaderNodeTexImage"); _im.image = bpy.data.images.load(LOGO)
_nt.links.new(_im.outputs["Color"], _b.inputs["Base Color"]); _nt.links.new(_im.outputs["Alpha"], _b.inputs["Alpha"])
_nt.links.new(_im.outputs["Color"], _b.inputs["Emission Color"]); _b.inputs["Emission Strength"].default_value = 0.25
M_LOGO.surface_render_method = 'BLENDED'
# mowing stripes on lawns: multiply by a soft wave along x
def add_stripes(m, period=3.2, lo=0.86, hi=1.10, axis='X'):
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; src = b.inputs["Base Color"].links[0].from_socket
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sep.inputs[0])
    mth = nt.nodes.new("ShaderNodeMath"); mth.operation = 'SINE'
    sc_ = nt.nodes.new("ShaderNodeMath"); sc_.operation = 'MULTIPLY'; sc_.inputs[1].default_value = math.pi / period
    nt.links.new(sep.outputs[axis], sc_.inputs[0]); nt.links.new(sc_.outputs[0], mth.inputs[0])
    rp = nt.nodes.new("ShaderNodeMapRange"); rp.inputs["From Min"].default_value = -1; rp.inputs["To Min"].default_value = lo; rp.inputs["To Max"].default_value = hi
    nt.links.new(mth.outputs[0], rp.inputs["Value"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs["Factor"].default_value = 1
    nt.links.new(src, mx.inputs[6]); nt.links.new(rp.outputs["Result"], mx.inputs[7]); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
add_stripes(M_LAWN, 3.4, 0.84, 1.10, 'Y')
add_stripes(M_TURF, 2.0, 0.88, 1.10, 'X')

# ----------------------------------------------------------------------------- terrain + world
# rolling land beyond 220 m so the horizon is not a flat plate
def terrain():
    size, n = 3000, 300
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=n, y_segments=n, size=size / 2)
    cx, cy = 85, 140
    for v in bm.verts:
        v.co.x += cx; v.co.y += cy
        d = math.hypot(v.co.x - cx, v.co.y - cy)
        w = min(1.0, max(0.0, (d - 260) / 500))
        h = (math.sin(v.co.x * 0.006) * math.cos(v.co.y * 0.005) * 9 + math.sin(v.co.x * 0.013 + 1.7) * 5 + math.cos(v.co.y * 0.011 + 0.4) * 6)
        v.co.z = -0.05 + max(0, h + 6) * w * 1.6
    me = bpy.data.meshes.new("Terrain"); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new("Terrain", me); me.materials.append(M_WILD); C_GROUND.objects.link(o)
terrain()

world = bpy.data.worlds.new("Sky"); sc.world = world; world.use_nodes = True; wn = world.node_tree; wn.nodes.clear()
# Oyo look: physical sky, warm late-afternoon sun low in the south-west, clear blue sky
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = 'MULTIPLE_SCATTERING'
SUN_ELEV = math.radians(30); SUN_ROT = math.radians(SUN_ROT_DEG if 'SUN_ROT_DEG' in globals() else 195)
sky.sun_elevation = SUN_ELEV; sky.sun_rotation = SUN_ROT; sky.sun_intensity = 1.0; sky.sun_size = math.radians(7.0)
try: sky.air_density = 1.0; sky.aerosol_density = 0.4
except Exception: pass
bg = wn.nodes.new("ShaderNodeBackground"); bg.inputs["Strength"].default_value = SKY_STRENGTH if 'SKY_STRENGTH' in globals() else 0.22
out = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(sky.outputs["Color"], bg.inputs["Color"]); wn.links.new(bg.outputs[0], out.inputs["Surface"])
# soft fill so the shadows stay light, like the Oyo renders (no shadows of its own)
fl = bpy.data.lights.new("ShadowFill", 'SUN'); fl.energy = FILL_E if 'FILL_E' in globals() else 9.0; fl.color = (0.92, 0.95, 1.0)
fl.use_shadow = False; fo = bpy.data.objects.new("ShadowFill", fl); fo.rotation_euler = (math.radians(10), 0, SUN_ROT + math.pi); sc.collection.objects.link(fo)

# ----------------------------------------------------------------------------- estate base, highway
Z_ROAD, Z_WALK, Z_LAWN = 0.08, 0.22, 0.30
mesh_from_poly("Estate_Road", ESTATE.buffer(0.3), -0.05, Z_ROAD, M_ASPHALT, C_GROUND)
# highway: the estate's south edge extended, 11 m wide (CAD), plus laterite shoulders + drain
p0 = Vector((1.43, 15.36)); p1 = Vector((170.75, 0.0)); dvec = (p1 - p0).normalized(); nrm = Vector((dvec.y, -dvec.x))  # points south
A = p0 - dvec * 700; B = p1 + dvec * 700
def strip(off0, off1):
    return Polygon([tuple(A + nrm * off0), tuple(B + nrm * off0), tuple(B + nrm * off1), tuple(A + nrm * off1)])
mesh_from_poly("Walkway", strip(0.0, 2.5), -0.1, 0.14, M_PAVERS, C_GROUND)
mesh_from_poly("Walkway_Curb", strip(2.3, 2.55), -0.1, 0.17, M_CURB, C_GROUND)
mesh_from_poly("Highway", strip(2.5, 11.0), -0.05, Z_ROAD - 0.02, M_ASPHALT, C_GROUND)
mesh_from_poly("Shoulder_S", strip(11.0, 14.5), -0.1, 0.03, M_LATERITE, C_GROUND)
# lane markings
L = (B - A).length
for i in range(0, int(L / 9)):
    a = A + dvec * (i * 9) + nrm * 6.75; b_ = a + dvec * 4.5
    mesh_from_poly(f"HwDash{i}", LineString([tuple(a), tuple(b_)]).buffer(0.08, cap_style=2), Z_ROAD - 0.02, Z_ROAD - 0.005, M_LINE, C_GROUND, sides=False)
for off in (2.85, 10.65):
    mesh_from_poly(f"HwEdge{off}", LineString([tuple(A + nrm * off), tuple(B + nrm * off)]).buffer(0.07, cap_style=2), Z_ROAD - 0.02, Z_ROAD - 0.005, M_LINE, C_GROUND, sides=False)

# ----------------------------------------------------------------------------- blocks: sidewalks, curbs, lawns, plot edges
groups = {}
for p in PLOTS: groups.setdefault(p["block"], []).append(p["poly"])
islands = unary_union([pg.buffer(0.3) for pg in [p["poly"] for p in PLOTS]] + [OPEN_SPACE.buffer(0.9), FACILITY.buffer(0.9)])
islands = [g for g in (islands.geoms if isinstance(islands, MultiPolygon) else [islands])]
walk = unary_union([g.buffer(1.6, join_style=1) for g in islands]).intersection(ESTATE.buffer(-0.05))
mesh_from_poly("Sidewalks", walk, Z_ROAD - 0.02, Z_WALK, M_PAVERS, C_GROUND)
curb = walk.difference(walk.buffer(-0.28))
mesh_from_poly("Curbs", curb, Z_ROAD - 0.02, Z_WALK + 0.04, M_CURB, C_GROUND, sides=True)
lawns = unary_union([p["poly"] for p in PLOTS])
M_LAWN_L = pbr("Lawn_Light", "leafy_grass", tile=3.0, tint=(0.22, 0.48, 0.20), bump=0.4, var=0.06, var_scale=0.08)
M_LAWN_D = pbr("Lawn_Deep", "leafy_grass", tile=3.0, tint=(0.11, 0.27, 0.09), bump=0.4, var=0.06, var_scale=0.08)
for blk in set(p["block"] for p in PLOTS):
    ps = sorted([p for p in PLOTS if p["block"] == blk], key=lambda p: p["num"])
    for par in (0, 1):
        g = unary_union([p["poly"] for p in ps if p["num"] % 2 == par])
        if not g.is_empty: mesh_from_poly(f"Plot_Lawns_{blk}{par}", g, Z_WALK - 0.02, Z_LAWN, M_LAWN_L if par else M_LAWN_D, C_PLOTS)
def flower_hedge():
    m = bpy.data.materials.new("Flower_Hedge"); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 9.0
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (1.0, 0.18, 0.02, 1); el[1].position = 1.0; el[1].color = (1.0, 0.75, 0.05, 1)
    el.new(0.5).color = (1.0, 0.30, 0.02, 1)
    nt.links.new(vo.outputs["Color"], ramp.inputs["Fac"])
    no = nt.nodes.new("ShaderNodeTexNoise"); no.inputs["Scale"].default_value = 14.0; nt.links.new(tc.outputs["Object"], no.inputs["Vector"])
    th = nt.nodes.new("ShaderNodeMath"); th.operation = 'GREATER_THAN'; th.inputs[1].default_value = 0.80; nt.links.new(no.outputs["Fac"], th.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'; mx.inputs[6].default_value = (0.012, 0.045, 0.006, 1)
    nt.links.new(th.outputs[0], mx.inputs[0]); nt.links.new(ramp.outputs["Color"], mx.inputs[7]); nt.links.new(mx.outputs[2], bs.inputs["Base Color"])
    bs.inputs["Roughness"].default_value = 0.8
    bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.8; nt.links.new(no.outputs["Fac"], bu.inputs["Height"]); nt.links.new(bu.outputs["Normal"], bs.inputs["Normal"])
    return m
M_FLOWERHEDGE = flower_hedge()
HWY = LineString([tuple(p0), tuple(p1)])
def hedge_lines(p):
    # commercial plots: hedges on the sides only, the road front stays open
    if p["block"] != "A": return [p["poly"].exterior]
    cs = list(p["poly"].exterior.coords); out = []
    for a, c in zip(cs[:-1], cs[1:]):
        seg = LineString([a, c])
        if HWY.distance(seg.centroid) > 6.0: out.append(seg)
    return out
edges = unary_union([ln.buffer(0.3, cap_style=1, join_style=1) for p in PLOTS for ln in hedge_lines(p)])
mesh_from_poly("Plot_FlowerHedges", edges, Z_WALK, Z_LAWN + 0.8, M_FLOWERHEDGE, C_PLOTS)

# ----------------------------------------------------------------------------- perimeter wall (W, N, E). South is open: Block A + commercial face out.
ex = list(ESTATE.exterior.coords)
def wall_run(a, b, name):
    a, b = Vector(a), Vector(b); d = (b - a); L = d.length; d.normalize(); n = Vector((-d.y, d.x))
    ln = LineString([tuple(a), tuple(b)])
    mesh_from_poly(name, ln.buffer(0.13, cap_style=2), 0, 2.45, M_CREAM, C_BUILD)
    mesh_from_poly(name + "_Cap", ln.buffer(0.2, cap_style=2), 2.45, 2.55, M_CREAM, C_BUILD)
    k = int(L / 4.0)
    for i in range(k + 1):
        q = a + d * (L * i / max(k, 1))
        cube(name + "_Pier", (q.x, q.y, 1.35), (0.45, 0.45, 2.7), M_CREAM, C_BUILD)
        cube(name + "_PierCap", (q.x, q.y, 2.75), (0.55, 0.55, 0.1), M_CHAR, C_BUILD)
        cyl(name + "_Post", (q.x, q.y, 3.2), 0.025, 0.9, M_STEEL, C_BUILD, verts=6)
    for h in (2.95, 3.2, 3.45):   # electric fence wires
        tube(name + "_Wire", [(a.x, a.y, h), (b.x, b.y, h)], 0.006, M_STEEL, C_BUILD, res=1)
corners = sorted(ex[:-1], key=lambda p: (p[0], -p[1]))
# perimeter fence: built in build_parts.py (fully enclosed, runs behind the commercial plots)

# ----------------------------------------------------------------------------- labels (Oyo style: big white letters standing on the plots)
# Oyo style: cream letters in a rounded bold face, standing upright on the plots
FL = bpy.data.fonts.load(f"{SP}/assets/fonts/Montserrat-700.ttf")
M_LABEL = flat("Label_Cream", (0.80, 0.75, 0.66), rough=0.6)
UP = (math.radians(90), 0, 0)
def lab(body, x, y, size, mat=None, depth=0.06):
    o = text(body, (x, y, Z_LAWN + size * 0.36), size, mat or M_LABEL, C_LABELS, font=FL, rot=UP, extrude=depth, bevel=0.0)
    o.data.space_character = 1.0; return o
for b, polys in groups.items():
    u = unary_union(polys); c = u.centroid
    if b == "700":
        lab("700 SQM", c.x, c.y + 2, 3.4, M_LABEL_O); lab("SPECIAL PLOT", c.x, c.y - 3.0, 2.0)
        continue
    big = 7.5 if b != "A" else 5.0
    w = u.bounds[2] - u.bounds[0]
    big = min(big, (w - 3.0) / 4.6)   # "BLOCK X" is ~4.6x its size wide; keep it inside the block
    lab(f"BLOCK {b}", c.x, c.y + (3.0 if b == 'A' else 0), big)
    if b == "A": lab("COMMERCIAL PLOTS", c.x, c.y - 4.0, 2.4)
    if b in ("C", "E", "F"): lab("600 SQM", c.x, c.y - 7.0, 2.6, M_LABEL_O)
M_NUM = flat("Label_Num", (0.82, 0.81, 0.79), rough=0.6)
for p in PLOTS:
    if p["size"] == 700: continue
    c = p["poly"].centroid
    if p["block"] == "A" and p["size"] == 600:
        lab("COMMERCIAL PLOT", c.x, c.y + 2.5, 2.2); lab("600 SQM", c.x, c.y - 2.0, 2.6, M_LABEL_O)
        continue
    lab(str(p["num"]), c.x, c.y, 3.4, M_NUM, depth=0.03)

with open(f"{SP}/epe2/plan.json", "w") as f:
    json.dump(dict(open_space=list(OPEN_SPACE.exterior.coords), facility=list(FACILITY.exterior.coords),
                   plots=[dict(b=p["block"], n=p["num"], s=p["size"], c=tuple(p["poly"].centroid.coords[0])) for p in PLOTS]), f)
print("BASE DONE", flush=True)
exec(compile(open(f"{SP}/epe2/build_parts.py").read(), "build_parts.py", "exec"))
