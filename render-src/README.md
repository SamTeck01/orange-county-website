# Epe render sources

Blender (bpy 5.x, Cycles CPU) scripts that build and render the Epe scene.

- `run_build.py` → runs `build.py` (which execs `build_parts.py`, `houses.py`, `extras.py`, `people.py`) and saves `epe.blend`.
- `build_lib2.py` → builds `lib2.blend` from the downloaded Fab/Sketchfab/Renderpeople assets ("OC Epe assets" Drive folder).
- `f_render.py` + `run_final.sh` → 4K stills (16 shots) then the 768-frame video. `web_shots.py` → quick web shots.
- `final/` → finished renders (JPEG q90): 01–11 are final; 12–16 were not yet rendered.

Not included (too large / external): `epe.blend` (680 MB), `lib2.blend` (220 MB), Poly Haven assets (`assets/ph`),
fonts, layout JSON from the PDF, Rocketbox avatars. Paths in the scripts point at the original scratchpad (`SP`).
