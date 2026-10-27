import bpy, sys, time, os
D = "/tmp/claude-0/-home-user-orange-county-website/79bc8f36-fcdf-57d9-86dc-616179bddea7/scratchpad/epe2"
mode = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.open_mainfile(filepath=f"{D}/epe.blend")
sc = bpy.context.scene; sc.render.use_persistent_data = False; sc.cycles.use_auto_tile = True; sc.cycles.tile_size = 1024
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '8'; sc.render.image_settings.compression = 15
labels = bpy.data.collections["03_Labels"]
import math
SKY = next(n for n in sc.world.node_tree.nodes if n.type == 'TEX_SKY'); BASE = (SKY.sun_elevation, sc.view_settings.exposure)
def dusk(on):
    # evening: sun just above the horizon, lamps carry the scene
    SKY.sun_elevation = math.radians(2.5) if on else BASE[0]
    sc.view_settings.exposure = BASE[1] + (1.6 if on else 0.0)
    fill = bpy.data.objects.get("ShadowFill")
    if fill: fill.data.energy = 1.5 if on else 9.0
STILLS = [("Aerial_Hero", "01_Estate_Aerial", True), ("Gate_Front", "02_Gate_Front", False), ("Gate_Angle", "03_Gate_Angle", False),
          ("Aerial_Entrance", "04_Entrance_Drone", True), ("Shops_Front", "05_Gym_Supermart", False), ("Pool", "06_Swimming_Pool", False),
          ("Pitch_Pool_Aerial", "07_Pitch_and_Pool", True), ("Avenue", "08_Main_Avenue", False), ("Avenue_Drone", "09_Avenue_Drone", True),
          ("Aerial_Special", "10_Special_700sqm", True), ("Aerial_Rear", "11_Estate_West_Aerial", True), ("Aerial_Front", "12_Estate_Front_Aerial", True),
          ("Aerial_Hero", "13_Estate_Aerial_Clean", False),
          ("Commercial_Strip", "14_Commercial_Plots", True), ("Lights_CCTV", "15_Street_Lights_CCTV", False), ("Aerial_Dusk", "16_Estate_Dusk", True)]
if mode == "stills":
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.cycles.samples = 32; sc.cycles.adaptive_threshold = 0.02
    for cam, name, lab in STILLS:
        path = f"{D}/web2/{name}.png"
        if os.path.exists(path): continue
        t = time.time(); sc.frame_set(1); sc.render.use_motion_blur = False; sc.camera = bpy.data.objects[cam]; labels.hide_render = not lab
        dusk(cam == 'Aerial_Dusk')
        sc.render.filepath = path; bpy.ops.render.render(write_still=True)
        print("STILL_DONE", name, round(time.time() - t), flush=True)
else:
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.cycles.samples = 40; sc.cycles.adaptive_threshold = 0.012
    sc.camera = bpy.data.objects["Video_Cam"]; labels.hide_render = False
    for f in range(sc.frame_start, sc.frame_end + 1):
        path = f"{D}/frames/f_{f:04d}.png"
        if os.path.exists(path): continue
        t = time.time(); sc.frame_set(f); sc.render.filepath = path; bpy.ops.render.render(write_still=True)
        print("FRAME", f, round(time.time() - t), flush=True)
print("ALL_DONE", mode, flush=True)
