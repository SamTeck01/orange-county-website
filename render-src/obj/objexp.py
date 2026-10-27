import bpy
bpy.ops.wm.open_mainfile(filepath="epe2/epe.blend")
# heavy instanced sources: decimate so the OBJ stays openable (trees were 1M polys each)
import bmesh, random
random.seed(1); seen=set(); dg=bpy.context.evaluated_depsgraph_get()
for o in bpy.data.objects:
    if o.instance_type=='COLLECTION' and o.instance_collection:
        for m in o.instance_collection.all_objects:
            if m.type!='MESH' or m.name in seen or len(m.data.polygons)<=1200: continue
            seen.add(m.name); n0=len(m.data.polygons)
            d=m.modifiers.new("dec",'DECIMATE'); d.ratio=max(0.004,1200/n0)
            dg.update(); me=bpy.data.meshes.new_from_object(m.evaluated_get(dg)); m.modifiers.remove(d)
            bm=bmesh.new(); bm.from_mesh(me)
            if len(bm.faces)>1600:   # leaf cards don't collapse: thin them instead
                keep=1600/len(bm.faces); bmesh.ops.delete(bm, geom=[f for f in bm.faces if random.random()>keep], context='FACES')
            loose=[e for e in bm.edges if not e.link_faces]; bmesh.ops.delete(bm, geom=loose, context='EDGES')
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
            bm.to_mesh(me); bm.free(); m.data=me
            print("DEC",m.name,n0,len(me.polygons),flush=True)

# OBJ can't carry node colours: bake a flat base colour into each procedural material
def upstream(node, seen):
    if node in seen: return
    seen.add(node)
    for i in node.inputs:
        for l in i.links: upstream(l.from_node, seen)
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    b=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if not b: continue
    bc=b.inputs["Base Color"]
    if not bc.is_linked: continue
    ns=set(); upstream(bc.links[0].from_node, ns)
    imgs=[n for n in ns if n.type=='TEX_IMAGE' and n.image]
    if bc.links[0].from_node.type=='TEX_IMAGE': continue
    if imgs:
        import colorsys, numpy as np
        im=imgs[0].image
        try:
            px=np.array(im.pixels[:]).reshape(-1,4)[::97]; px=px[px[:,3]>0.5] if (px[:,3]>0.5).any() else px
            c=list(px[:,:3].mean(0))
        except Exception: c=[0.3,0.4,0.2]
        for n in ns:
            if n.type=='HUE_SAT':
                h,sa,v=colorsys.rgb_to_hsv(*c); h=(h+n.inputs["Hue"].default_value-0.5)%1; sa=min(1,sa*n.inputs["Saturation"].default_value); v=v*n.inputs["Value"].default_value
                c=list(colorsys.hsv_to_rgb(h,sa,v))
            elif n.type in('MIX','MIX_RGB'):
                cs=[tuple(i.default_value)[:3] for i in n.inputs if i.type=='RGBA' and not i.is_linked]
                if cs:
                    fac=n.inputs[0].default_value if n.inputs[0].type=='VALUE' else 0.5
                    bt=getattr(n,'blend_type','MIX')
                    c=[a*b for a,b in zip(c,cs[0])] if bt=='MULTIPLY' else [a*(1-fac)+b*fac for a,b in zip(c,cs[0])]
        a_link=b.inputs["Alpha"].is_linked
        mat.node_tree.links.remove(bc.links[0]); bc.default_value=(*c,1)
        al=b.inputs["Alpha"]
        if al.is_linked and al.links[0].from_node.type!='TEX_IMAGE':
            an=set(); upstream(al.links[0].from_node, an); ai=[n for n in an if n.type=='TEX_IMAGE']
            if ai: mat.node_tree.links.remove(al.links[0]); mat.node_tree.links.new(ai[0].outputs["Color"], al)
        continue
    cols=[]
    for n in ns:
        if n.type=='RGB': cols.append(tuple(n.outputs[0].default_value)[:3])
        if n.type=='VALTORGB': cols += [tuple(e.color)[:3] for e in n.color_ramp.elements]
        for i in n.inputs:
            if i.type=='RGBA' and not i.is_linked: cols.append(tuple(i.default_value)[:3])
    if not cols: continue
    c=[sum(x[k] for x in cols)/len(cols) for k in range(3)]
    mat.node_tree.links.remove(bc.links[0]); bc.default_value=(*c,1)
# text labels -> mesh
for o in list(bpy.data.collections["03_Labels"].all_objects):
    if o.type in('FONT','CURVE'):
        me=bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()))
        n=bpy.data.objects.new(o.name+"_m",me); n.matrix_world=o.matrix_world
        for c in o.users_collection: c.objects.link(n)
        o.hide_render=True; o.hide_viewport=True; o.hide_set(True)
bpy.data.collections["07_Cameras"].hide_viewport=True
for o in bpy.context.view_layer.objects: o.select_set(False)
for o in bpy.context.view_layer.objects:
    if o.visible_get() and o.type in('MESH','EMPTY'): o.select_set(True)
bpy.ops.wm.obj_export(filepath="objout/Orange_County_Epe_3D/Orange County Epe.obj", export_selected_objects=True, apply_modifiers=True, export_materials=True, path_mode='COPY', forward_axis='NEGATIVE_Z', up_axis='Y', export_triangulated_mesh=False)
print("OBJ_DONE",flush=True)
