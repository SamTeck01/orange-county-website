"use client";

import Image from "next/image";
import { useState } from "react";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/**
 * The film is 14.9MB. The <video> element is not rendered at all until the
 * poster is clicked, so nothing downloads on page load — preload="none" alone
 * is not reliable across browsers.
 */
function Film() {
  const [playing, setPlaying] = useState(false);
  const film = assets.film;
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

export function Gallery() {
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
          <Film />
        </div>
      </Shell>

      {/* Rail runs past the right edge so it reads as continuing, not cropped. */}
      <div data-reveal style={{ "--i": 4 } as React.CSSProperties} className="edge-fade-r mt-4 md:mt-5">
        <ul className="flex snap-x snap-mandatory gap-4 overflow-x-auto px-gut pb-3 md:gap-5 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {assets.gallery.map((shot, index) =>
            shot.src ? (
              <li key={shot.src} className="w-[78vw] shrink-0 snap-start sm:w-[54vw] lg:w-[32vw]">
                <figure className="relative aspect-[4/3] overflow-hidden rounded-[16px]">
                  <Image
                    src={shot.src}
                    alt={shot.alt}
                    fill
                    loading="lazy"
                    sizes="(min-width: 1024px) 32vw, (min-width: 640px) 54vw, 78vw"
                    placeholder="blur"
                    blurDataURL={blurFor(shot.src)}
                    className="object-cover"
                  />
                  <span aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-[16px] border border-oc-paper/12" />
                  <figcaption className="absolute left-3 top-3 font-mono text-[0.625rem] tracking-[0.16em] text-oc-paper/70">{String(index + 1).padStart(2, "0")}</figcaption>
                </figure>
              </li>
            ) : null,
          )}
        </ul>
      </div>
    </InView>
  );
}
