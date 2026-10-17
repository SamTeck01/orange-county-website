"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import type { MediaAsset } from "@/content/assets";
import { blurFor } from "@/lib/media";

type Status = "idle" | "loading" | "ready" | "error";

/**
 * Poster first; three.js and the model are only fetched after the button is
 * pressed, so the section costs nothing on page load.
 */
export function EstateModelViewer({ src, poster }: { src: string; poster: MediaAsset }) {
  const [status, setStatus] = useState<Status>("idle");
  const [progress, setProgress] = useState(0);
  const mountRef = useRef<HTMLDivElement>(null);
  const resetRef = useRef<() => void>(() => {});

  useEffect(() => {
    if (status !== "loading") return;
    const mount = mountRef.current;
    if (!mount) return;
    let disposed = false;
    let cleanup = () => {};

    (async () => {
      const THREE = await import("three");
      const { OrbitControls } = await import("three/examples/jsm/controls/OrbitControls.js");
      const { GLTFLoader } = await import("three/examples/jsm/loaders/GLTFLoader.js");
      if (disposed) return;

      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(mount.clientWidth, mount.clientHeight);
      renderer.outputColorSpace = THREE.SRGBColorSpace;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.0;
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      mount.appendChild(renderer.domElement);
      renderer.domElement.style.touchAction = "none";

      const scene = new THREE.Scene();
      scene.background = new THREE.Color("#bcd3e6");
      scene.fog = new THREE.Fog("#bcd3e6", 380, 900);
      scene.add(new THREE.HemisphereLight("#eaf2ff", "#3d4a2a", 1.6));
      const sun = new THREE.DirectionalLight("#fff4e2", 2.4);
      sun.position.set(-160, 220, 260);
      sun.castShadow = true;
      sun.shadow.mapSize.set(2048, 2048);
      Object.assign(sun.shadow.camera, { left: -220, right: 220, top: 220, bottom: -220, near: 10, far: 900 });
      sun.shadow.bias = -0.0005;
      scene.add(sun);

      const camera = new THREE.PerspectiveCamera(38, mount.clientWidth / mount.clientHeight, 1, 4000);
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.maxPolarAngle = Math.PI * 0.46;
      controls.minDistance = 25;
      controls.maxDistance = 650;
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.5;
      controls.addEventListener("start", () => (controls.autoRotate = false));

      const gltf = await new GLTFLoader().loadAsync(src, (event) => {
        if (event.total) setProgress(Math.round((event.loaded / event.total) * 100));
      });
      if (disposed) return;
      gltf.scene.traverse((node) => {
        const mesh = node as import("three").Mesh;
        if (mesh.isMesh) {
          mesh.castShadow = true;
          mesh.receiveShadow = true;
        }
      });
      scene.add(gltf.scene);
      // Wide field under the model so its edge melts into the fog.
      const field = new THREE.Mesh(new THREE.PlaneGeometry(4000, 4000), new THREE.MeshStandardMaterial({ color: "#1d3010", roughness: 1 }));
      field.rotation.x = -Math.PI / 2;
      field.position.set(85, -0.2, -140);
      field.receiveShadow = true;
      scene.add(field);

      // Model is in metres, Y-up; the estate is centred near (85, 0, -140).
      const centre = new THREE.Vector3(85, 0, -140);
      const home = () => {
        controls.target.copy(centre);
        camera.position.set(215, 165, 60);
        controls.autoRotate = true;
        controls.update();
      };
      home();
      resetRef.current = home;

      const onResize = () => {
        camera.aspect = mount.clientWidth / mount.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(mount.clientWidth, mount.clientHeight);
      };
      window.addEventListener("resize", onResize);
      renderer.setAnimationLoop(() => {
        controls.update();
        renderer.render(scene, camera);
      });
      setStatus("ready");

      cleanup = () => {
        window.removeEventListener("resize", onResize);
        renderer.setAnimationLoop(null);
        controls.dispose();
        scene.traverse((node) => {
          const mesh = node as import("three").Mesh;
          if (!mesh.isMesh) return;
          mesh.geometry.dispose();
          for (const material of [mesh.material].flat()) material.dispose();
        });
        renderer.dispose();
        renderer.domElement.remove();
      };
    })().catch(() => {
      if (!disposed) setStatus("error");
    });

    return () => {
      disposed = true;
      cleanup();
    };
  }, [status === "idle" || status === "error" ? null : "active", src]); // eslint-disable-line react-hooks/exhaustive-deps

  const active = status === "loading" || status === "ready";

  return (
    <div className="relative aspect-[4/5] w-full overflow-hidden rounded-[20px] border border-oc-paper/12 bg-oc-ink sm:aspect-[16/10] md:aspect-[16/9] md:rounded-[24px]">
      <div ref={mountRef} className="absolute inset-0" />

      {status !== "ready" ? (
        <>
          {poster.src ? <Image src={poster.src} alt={poster.alt} fill loading="lazy" sizes="100vw" placeholder="blur" blurDataURL={blurFor(poster.src)} className="object-cover" /> : null}
          <span aria-hidden="true" className="absolute inset-0 bg-gradient-to-t from-oc-ink-deep via-oc-ink-deep/55 to-oc-ink-deep/5" />
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 px-gut text-center">
            {status === "loading" ? (
              <p className="font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-oc-paper" role="status">
                Loading the estate… {progress}%
              </p>
            ) : (
              <>
                <button
                  type="button"
                  onClick={() => setStatus("loading")}
                  className="inline-flex min-h-[52px] items-center gap-3 rounded-full bg-oc-orange px-7 font-mono text-[0.75rem] uppercase tracking-[0.16em] text-oc-ink transition-transform duration-300 ease-out hover:scale-105"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" className="h-5 w-5" aria-hidden="true">
                    <path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z" />
                    <path d="M12 12l8-4.5M12 12v9M12 12L4 7.5" />
                  </svg>
                  Explore in 3D
                </button>
                <p className="max-w-[34ch] text-sm text-oc-paper/75">
                  {status === "error" ? "The 3D view could not load. Please try again." : "Drag to turn, pinch or scroll to zoom."}
                </p>
              </>
            )}
          </div>
        </>
      ) : null}

      {active ? (
        <div className="absolute right-3 top-3 flex gap-2">
          {status === "ready" ? (
            <button type="button" onClick={() => resetRef.current()} className="inline-flex min-h-11 items-center rounded-full bg-oc-ink-deep/70 px-4 font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper backdrop-blur">
              Reset view
            </button>
          ) : null}
          <button type="button" onClick={() => setStatus("idle")} aria-label="Close the 3D view" className="inline-flex h-11 w-11 items-center justify-center rounded-full bg-oc-ink-deep/70 font-mono text-xl text-oc-paper backdrop-blur">
            ×
          </button>
        </div>
      ) : null}
    </div>
  );
}
