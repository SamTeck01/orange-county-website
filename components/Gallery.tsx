"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import type { MediaAsset } from "@/content/assets";
import type { Estate } from "@/content/estates";
import { blurFor } from "@/lib/media";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/**
 * Films run 15-36MB. The <video> element is not rendered at all until the
 * poster is clicked, so nothing downloads on page load — preload="none" alone
 * is not reliable across browsers.
 */
function Film({ estate }: { estate: Estate }) {
  const [playing, setPlaying] = useState(false);
  const film = estate.media.film;
  if (!film.src) return null;

  if (playing) {
    return (
      <video
        className="h-full w-full bg-oc-ink-deep object-cover"
        src={film.src}
        poster={film.poster ?? undefined}
        controls
        autoPlay
        playsInline
        preload="none"
        aria-label={film.label}
      />
    );
  }

  return (
    <button type="button" onClick={() => setPlaying(true)} aria-label={`Play the ${film.label}`} className="group relative block h-full w-full overflow-hidden bg-oc-ink-deep">
      {film.poster ? (
        <Image
          src={film.poster}
          alt=""
          fill
          loading="lazy"
          sizes="100vw"
          placeholder="blur"
          blurDataURL={blurFor(film.poster)}
          className="object-cover transition-transform duration-[1200ms] ease-out group-hover:scale-[1.03]"
        />
      ) : null}
      <span aria-hidden="true" className="absolute inset-0 bg-oc-ink-deep/25 transition-colors duration-500 group-hover:bg-oc-ink-deep/10" />

      <span aria-hidden="true" className="absolute left-1/2 top-1/2 flex h-16 w-16 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-oc-orange transition-transform duration-500 ease-out group-hover:scale-110 md:h-20 md:w-20">
        <svg viewBox="0 0 24 24" className="ml-0.5 h-5 w-5 md:h-6 md:w-6" fill="currentColor" aria-hidden="true">
          <path d="M8 5v14l11-7z" />
        </svg>
      </span>

      <span className="absolute bottom-5 left-5 font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper/85 md:bottom-7 md:left-7">60-second flythrough</span>
    </button>
  );
}

/** Full-screen viewer for one gallery image: arrows, swipe, Esc to close. */
export function Lightbox({ shots, index, onIndex, onClose, label = "Gallery" }: { shots: MediaAsset[]; index: number; onIndex: (i: number) => void; onClose: () => void; label?: string }) {
  const closeRef = useRef<HTMLButtonElement>(null);
  const touchX = useRef<number | null>(null);
  const count = shots.length;
  const go = (step: number) => onIndex((index + step + count) % count);
  const shot = shots[index];

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      if (event.key === "ArrowRight") onIndex((index + 1) % count);
      if (event.key === "ArrowLeft") onIndex((index - 1 + count) % count);
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [index, count, onIndex, onClose]);

  useEffect(() => {
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();
    return () => {
      document.body.style.overflow = "";
    };
  }, []);

  if (!shot?.src) return null;

  // Portalled to <body>: the section's `isolate` would otherwise trap it under the header.
  return createPortal(
    <div role="dialog" aria-modal="true" aria-label={label} className="fixed inset-0 z-[100] flex flex-col bg-oc-ink-deep/97 text-oc-paper">
      <div className="flex items-center justify-between px-gut py-3">
        <p className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper/65" aria-live="polite">
          {count > 1 ? `${String(index + 1).padStart(2, "0")} / ${String(count).padStart(2, "0")}` : label}
        </p>
        <button ref={closeRef} type="button" onClick={onClose} aria-label={`Close ${label.toLowerCase()}`} className="inline-flex h-11 w-11 items-center justify-center font-mono text-2xl leading-none text-oc-paper">
          ×
        </button>
      </div>

      <div
        className="relative flex-1"
        onTouchStart={(event) => (touchX.current = event.touches[0].clientX)}
        onTouchEnd={(event) => {
          if (touchX.current === null) return;
          const dx = event.changedTouches[0].clientX - touchX.current;
          if (Math.abs(dx) > 40) go(dx < 0 ? 1 : -1);
          touchX.current = null;
        }}
      >
        <Image key={shot.src} src={shot.src} alt={shot.alt} fill sizes="100vw" placeholder="blur" blurDataURL={blurFor(shot.src)} className="object-contain px-2 md:px-20" />
        {count > 1 ? (
          <>
            <button type="button" onClick={() => go(-1)} aria-label="Previous image" className="absolute left-2 top-1/2 inline-flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full bg-oc-ink-deep/60 text-oc-paper backdrop-blur transition-colors hover:bg-oc-orange hover:text-oc-ink md:left-5 md:h-12 md:w-12">
              ←
            </button>
            <button type="button" onClick={() => go(1)} aria-label="Next image" className="absolute right-2 top-1/2 inline-flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full bg-oc-ink-deep/60 text-oc-paper backdrop-blur transition-colors hover:bg-oc-orange hover:text-oc-ink md:right-5 md:h-12 md:w-12">
              →
            </button>
          </>
        ) : null}
      </div>

      <p className="px-gut py-4 text-center text-sm text-oc-paper/70">{shot.alt}</p>
    </div>,
    document.body,
  );
}

export function Gallery({ estate }: { estate: Estate }) {
  const assets = { gallery: estate.media.gallery };
  const shots = assets.gallery.filter((shot) => shot.src);
  const [open, setOpen] = useState<number | null>(null);
  return (
    <InView as="section" id="gallery" aria-label="Film and gallery" className="relative isolate overflow-hidden bg-oc-ink py-sec text-oc-paper" amount={0.08}>
      <div aria-hidden="true" className="card-noise absolute inset-0 -z-10 opacity-40" />

      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["See it", "move."]} size="h1" className="max-w-[12ch] text-oc-paper" />
          <Eyebrow index={2} className="md:pb-3">
            Film &amp; Gallery
          </Eyebrow>
        </div>

        <div data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-10 aspect-[16/10] overflow-hidden rounded-[20px] md:mt-14 md:aspect-[16/9] md:rounded-[24px]">
          <Film estate={estate} />
        </div>
      </Shell>

      {/* Rail runs past the right edge so it reads as continuing, not cropped. */}
      <div data-reveal style={{ "--i": 4 } as React.CSSProperties} className="edge-fade-r mt-4 md:mt-5">
        <ul className="flex snap-x snap-mandatory gap-4 overflow-x-auto px-gut pb-3 md:gap-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {shots.map((shot, index) =>
            shot.src ? (
              <li key={shot.src} className="w-[78vw] shrink-0 snap-start sm:w-[54vw] lg:w-[32vw]">
                <button type="button" onClick={() => setOpen(index)} aria-label={`View image ${index + 1}: ${shot.alt}`} className="group block w-full">
                <figure className="relative aspect-[4/3] overflow-hidden rounded-[16px]">
                  <Image
                    src={shot.src}
                    alt={shot.alt}
                    fill
                    loading="lazy"
                    sizes="(min-width: 1024px) 32vw, (min-width: 640px) 54vw, 78vw"
                    placeholder="blur"
                    blurDataURL={blurFor(shot.src)}
                    className="object-cover transition-transform duration-700 ease-out group-hover:scale-[1.04]"
                  />
                  <span aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-[16px] border border-oc-paper/12" />
                  <span aria-hidden="true" className="absolute bottom-3 right-3 inline-flex h-9 w-9 items-center justify-center rounded-full bg-oc-ink-deep/55 text-oc-paper backdrop-blur transition-colors duration-300 group-hover:bg-oc-orange group-hover:text-oc-ink">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" className="h-4 w-4">
                      <path d="M4 10V4h6M20 14v6h-6M20 10V4h-6M4 14v6h6" />
                    </svg>
                  </span>
                  <figcaption className="absolute left-3 top-3 font-mono text-[0.625rem] tracking-[0.16em] text-oc-paper/70">{String(index + 1).padStart(2, "0")}</figcaption>
                </figure>
                </button>
              </li>
            ) : null,
          )}
        </ul>
      </div>

      {open !== null ? <Lightbox shots={shots} index={open} onIndex={setOpen} onClose={() => setOpen(null)} /> : null}
    </InView>
  );
}
