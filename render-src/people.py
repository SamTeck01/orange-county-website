# 3D people: Microsoft Rocketbox avatars (MIT licence) + Rocketbox motion-capture clips.
# Walkers move through the video (root motion detrended, then driven along a path); others idle/talk in place.
RB = "/home/user/rb/repo/Assets"
C_PPL = sub("08_People")
FR_END = sc.frame_end if sc.frame_end > 1 else 240

def fcurves_of(act):
    try:
        if act.fcurves: return list(act.fcurves)
    except AttributeError: pass
    out = []
    for ly in getattr(act, "layers", []):
        for st in ly.strips:
            for cb in st.channelbags: out += list(cb.fcurves)
    return out

def assign_action(ob, act):
    ob.animation_data_create(); ob.animation_data.action = act
    try:
        if act.slots and ob.animation_data.action_slot is None: ob.animation_data.action_slot = act.slots[0]
    except AttributeError: pass

ANIM = {}
def load_anim(name, kind):
    key = (name, kind)
    if key in ANIM: return ANIM[key]
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=f"{RB}/Animations/all_animations_max_motextr_{kind}/{name}.max.fbx")
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == 'ARMATURE'); act = arm.animation_data.action
    f0, f1 = act.frame_range
    disp = Vector((0, 0, 0)); root = None
    if kind == "xy":
        # root bone = the one whose location travels furthest; measure world displacement over one cycle
        rpb = next(pb for pb in arm.pose.bones if pb.parent is None)
        sc.frame_set(int(f0)); a = arm.matrix_world @ rpb.head
        sc.frame_set(int(f1)); b = arm.matrix_world @ rpb.head
        root = rpb.name; disp = b - a
        disp.z = 0
        # detrend that bone's location curves so the clip walks in place (bob and sway kept)
        for fc in fcurves_of(act):
            if fc.data_path == f'pose.bones["{root}"].location':
                kp = fc.keyframe_points
                if len(kp) < 2: continue
                v0, v1 = kp[0].co.y, kp[-1].co.y; t0, t1 = kp[0].co.x, kp[-1].co.x
                if abs(v1 - v0) > 1e-4:
                    for k in kp:
                        dv = (v1 - v0) * (k.co.x - t0) / max(1e-6, (t1 - t0))
                        k.co.y -= dv; k.handle_left.y -= dv; k.handle_right.y -= dv
    for fc in fcurves_of(act):
        if not any(m.type == 'CYCLES' for m in fc.modifiers): fc.modifiers.new('CYCLES')
    act.use_fake_user = True
    sc.frame_set(1)
    for o in new: bpy.data.objects.remove(o, do_unlink=True)
    ANIM[key] = (act, disp, f1 - f0)
    return ANIM[key]

def fix_materials(avatar, meshes):
    """Rocketbox FBX texture paths do not resolve on import: rebuild each material from the Textures folder."""
    tdir = f"{RB}/Avatars/Adults/{avatar}/Textures"
    files = os.listdir(tdir)
    def tex(stem):
        f = next((f for f in files if f.lower().startswith(stem.lower())), None)
        return bpy.data.images.load(f"{tdir}/{f}", check_existing=True) if f else None
    for m in meshes:
        for slot in m.material_slots:
            mt = slot.material
            if not mt: continue
            base = mt.name.split(".")[0]                     # e.g. m006_body / m006_head / m006_opacity
            part = base.rsplit("_", 1)[-1]
            pref = base.rsplit("_", 1)[0]
            nm = bpy.data.materials.new(f"RB_{avatar}_{part}"); nm.use_nodes = True
            nt = nm.node_tree; b = nt.nodes["Principled BSDF"]
            src = "head" if part == "opacity" else part
            ci = tex(f"{pref}_{src}_color"); ni = tex(f"{pref}_{src}_normal"); si = tex(f"{pref}_{src}_specular")
            if ci:
                n = nt.nodes.new("ShaderNodeTexImage"); n.image = ci; nt.links.new(n.outputs["Color"], b.inputs["Base Color"])
            if ni:
                n = nt.nodes.new("ShaderNodeTexImage"); n.image = ni; ni.colorspace_settings.name = 'Non-Color'
                nmn = nt.nodes.new("ShaderNodeNormalMap"); nmn.inputs["Strength"].default_value = 0.8
                nt.links.new(n.outputs["Color"], nmn.inputs["Color"]); nt.links.new(nmn.outputs["Normal"], b.inputs["Normal"])
            if si:
                n = nt.nodes.new("ShaderNodeTexImage"); n.image = si; si.colorspace_settings.name = 'Non-Color'
                inv = nt.nodes.new("ShaderNodeInvert"); nt.links.new(n.outputs["Color"], inv.inputs["Color"])
                mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.35; mr.inputs["To Max"].default_value = 0.9
                nt.links.new(inv.outputs["Color"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
            b.inputs["Subsurface Weight"].default_value = 0.08 if part in ("head", "body") else 0.0
            if part == "opacity":
                oi = tex(f"{pref}_opacity_color")
                if oi:
                    n = nt.nodes.new("ShaderNodeTexImage"); n.image = oi; oi.colorspace_settings.name = 'Non-Color'
                    nt.links.new(n.outputs["Color"], b.inputs["Alpha"]); nm.surface_render_method = 'DITHERED'
            slot.material = nm

FACE0 = None   # avatar's forward heading at rest, derived from the walk clip
def person(avatar, anim, kind, x, y, z, heading_deg, walk_dist=0.0, phase=0):
    global FACE0
    act, disp, cyc = load_anim(anim, kind)
    if kind == "xy" and FACE0 is None: FACE0 = math.atan2(disp.y, disp.x)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=f"{RB}/Avatars/Adults/{avatar}/Export/{avatar}.fbx")
    new = [o for o in bpy.data.objects if o not in before]
    arm = next(o for o in new if o.type == 'ARMATURE')
    meshes = [o for o in new if o.type == 'MESH']
    for o in new:
        if o.type == 'EMPTY': bpy.data.objects.remove(o, do_unlink=True); continue
        for c in list(o.users_collection): c.objects.unlink(o)
        C_PPL.objects.link(o)
    fix_materials(avatar, meshes)
    root = bpy.data.objects.new(f"P_{avatar}", None); C_PPL.objects.link(root)
    arm.parent = root
    h = math.radians(heading_deg)
    root.rotation_euler = (0, 0, h - (FACE0 if FACE0 is not None else -math.pi / 2))
    assign_action(arm, act)
    # offset the cycle so people are not in lock-step
    if phase:
        tr = arm.animation_data.nla_tracks.new(); st = tr.strips.new("clip", 1 - phase, act); st.repeat = 40
        arm.animation_data.action = None
    if kind == "xy" and walk_dist:
        speed = disp.length / max(1, cyc)                       # metres per frame of the original clip
        d = Vector((math.cos(h), math.sin(h), 0))
        root.location = (x, y, z); root.keyframe_insert("location", frame=1)
        root.location = Vector((x, y, z)) + d * speed * (FR_END - 1); root.keyframe_insert("location", frame=FR_END)
        for fc in fcurves_of(root.animation_data.action):
            for k in fc.keyframe_points: k.interpolation = 'LINEAR'
    else:
        root.location = (x, y, z)
    return root

if os.path.isdir(RB):
    W = "xy"; S = "static"
    # avenue couple + pavement walkers (moving)
    person("Male_Adult_04", "m_walk_neutral_01", W, 128.6, 31.0, Z_WALK, 90, walk_dist=1, phase=3)
    person("Female_Party_02", "f_walk_neutral_01", W, 129.3, 31.6, Z_WALK, 90, walk_dist=1, phase=9)
    person("Male_Adult_12", "m_walk_neutral_02", W, 137.2, 68.0, Z_WALK, -90, walk_dist=1, phase=14)
    person("Female_Adult_06", "f_walk_stroll_01", W, 137.4, 44.0, Z_WALK, -90, walk_dist=1, phase=5)
    # pedestrians on the highway walkway in front of the sign wall
    q = on_walk(104.0, 1.2); person("Male_Adult_17", "m_walk_neutral_01", W, q.x, q.y, 0.14, math.degrees(EDGE_ANG), walk_dist=1, phase=20)
    q = on_walk(120.0, 1.6); person("Female_Adult_11", "f_walk_neutral_01", W, q.x, q.y, 0.14, math.degrees(EDGE_ANG) + 180, walk_dist=1, phase=11)
    # gatehouse guard, shop front, forecourt group, poolside
    person("Male_Adult_15", "m_idle_neutral_01", S, GX0 - 0.6, y_edge(GX0) + 2.6, Z_WALK, 180)
    # photoreal Renderpeople at the shop forecourt (posed scans face -Y)
    def rp(name, x, y, z, heading_deg):
        inst(L2[name], x, y, z, 1.0, rz=math.radians(heading_deg) + math.pi / 2, col=C_PPL)
    rp("RP_dennis", 114.8, 20.0, Z_WALK + 0.02, 0)
    rp("RP_mei", 118.6, 23.2, Z_WALK + 0.02, -60)
    rp("RP_fabienne", 119.6, 21.9, Z_WALK + 0.02, 120)
    rp("RP_178", 116.2, 13.0, Z_WALK + 0.02, 200)
    person("Male_Adult_12", "m_idle_neutral_03", S, lx1 - 4.0, PY1 + 2.6, zp + 0.08, -150)
    person("Female_Adult_06", "f_idle_neutral_03", S, PX0 + 4.0, PY0 - 1.3, zp, 80)
    person("Male_Adult_04", "m_gestic_talk_neutral_01", S, FX0 + 4.0, FY0 + 3.0, Z_WALK + 0.09, 30)
    person("Male_Adult_17", "m_idle_neutral_01", S, FX0 + 6.5, FY0 + 4.2, Z_WALK + 0.09, 210)
    print("people placed", len([o for o in C_PPL.objects if o.type == 'ARMATURE']), flush=True)
