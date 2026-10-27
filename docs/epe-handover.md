# Orange County Epe: 3D renders, film and website handover

Read this first to continue the Epe render and video work. AGENTS.md still governs the website.

## Where things live
- Website: repo `SamTeck01/orange-county-website`, site changes go to `main`.
- Render sources and deliverables: branch `claude/epe-render-sources`, folder `render-src/`
  (never put render sources on main).
  - `render-src/final/`: delivered stills 01–16 (01–11 4K, 12–16 1080p), films, posters.
    Latest film: `Orange_County_Epe_Film_1080.mp4` (57 s, anti-flicker, 1080p, original track "Golden Hour").
  - Blender scripts: `build.py`, `build_parts.py`, `extras.py`, `houses.py`, `people.py`, `build_lib2.py`
    (asset library), `f_render.py` (stills), `film.py` (video: shot list `S`), `dissolve.py`, `hq.sh`, `deflick.sh`.
  - `music/cool.py`: current score (args: duration, comma-separated cut times). `music/compose.py`: older soft score.
  - `obj/objexp.py`, `obj/objpack.sh`: OBJ+MTL+textures export (same format as the Oyo designer's file).
- Large binaries (`epe.blend` ~680 MB, `lib.blend`, `lib2.blend`, Fab/Sketchfab/Renderpeople assets) are NOT in git.
  They were built in a cloud scratchpad that gets wiped. Assets came from the owner's Google Drive folder "OC Epe assets".
  To rebuild: download the assets, run `build_lib2.py` then `run_build.py`/`build.py` with Blender's bpy (Python module, Blender 5.x).
- The owner has: the Drive folder "Orange County Epe – Final Renders" (images + film), `Orange_County_Epe_3D.zip` (OBJ).

## Look the owner approved (keep it)
- Oyo-style look, which is the benchmark: darker natural daylight, light soft shadows, sun from the front, no glowing whites
  (exposure −1.7, AgX, low bloom).
- Two-tone green plots; cream Montserrat labels that sit inside the plots and never overflow (Block G).
- Orange and gold autumn tree clusters outside the estate; a few houses around, none touching the fence.
- No stray plants: just a neat hedge and flower band at the gate walls; palms only on the entrance median.
- Car drives IN through the RIGHT lane (left is out, right is in).
- Shots show the estate, not the surroundings. Commercial plots must read clearly.

## Known limits / open items
- The machine is CPU-only (no graphics card), so renders are slow, and it restarts when idle. Renders resume from saved frames.
  Keep a watcher running that auto-restarts `hq.sh`.
- The film was rendered at 14 samples per pixel, which gives slight flicker and a plastic look. The proper fix is a re-render at
  1080p with more samples on a GPU or render farm (~2–4 h on RTX 3060+; ~40 h on CPU). `deflick.sh` only reduces the flicker.
- The network blocks archive.org file servers and pixabay, so music is composed in code (`music/cool.py`).
- The owner prefers short, direct updates, previews before big renders, and "high quality, not low quality".
