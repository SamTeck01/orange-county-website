import bpy, math
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath="objout/Orange_County_Epe_3D/Orange County Epe.obj", forward_axis='NEGATIVE_Z', up_axis='Y')
sc=bpy.context.scene; print("OBJS",len(sc.objects),flush=True)
w=bpy.data.worlds.new("w"); sc.world=w; w.color=(0.6,0.7,0.8)
s=bpy.data.lights.new("s",'SUN'); s.energy=3; so=bpy.data.objects.new("s",s); so.rotation_euler=(0.7,0,2.6); sc.collection.objects.link(so)
cd=bpy.data.cameras.new("c"); c=bpy.data.objects.new("c",cd); sc.collection.objects.link(c); sc.camera=c
from mathutils import Vector
c.location=(225,-110,175); c.rotation_euler=(Vector((86,132,0))-c.location).to_track_quat('-Z','Y').to_euler(); cd.lens=30; cd.clip_end=5000
sc.render.engine='CYCLES'; sc.cycles.samples=8; sc.render.resolution_x,sc.render.resolution_y=1280,720
sc.render.filepath="/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/objchk.png"; bpy.ops.render.render(write_still=True); print("CHK_DONE")
