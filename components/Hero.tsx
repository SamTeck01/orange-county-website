"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { positioning } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { entryPrice, estateName, locationLine, plotSizes, surveyStatus, titleStatus, whatsappHref } from "@/lib/site";
import { Action } from "@/components/primitives";
import { useReducedMotion } from "@/lib/useReducedMotion";

/** Facts only — every value here is read from content/orange-county.ts. */
const rail = [
  { label: "Plots from", value: entryPrice.display },
  { label: "Sizes", value: `${plotSizes} sqm` },
  { label: "Title", value: titleStatus },
  { label: "Survey", value: surveyStatus },
];

function HeroMedia() {
  const reduced = useReducedMotion();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [failed, setFailed] = useState(false);
  const video = assets.heroVideo;

  useEffect(() => {
    const node = videoRef.current;
    if (!node || reduced || window.matchMedia("(max-width: 767px)").matches) return;
    // Some browsers reject autoplay even when muted (iOS Low Power Mode).
    // If it rejects, fall through to the still so the frame is never empty.
    const attempt = node.play();
    if (attempt) attempt.catch(() => setFailed(true));
  }, [reduced]);

  const showStill = reduced || failed || !video.src;

  if (showStill) {
    return assets.hero.src ? (
      <Image
        src={assets.hero.src}
        alt={assets.hero.alt}
        fill
        priority
        sizes="100vw"
        placeholder="blur"
        blurDataURL={blurFor(assets.hero.src)}
        className="object-cover"
        style={{ objectPosition: assets.hero.focal }}
      />
    ) : (
      <div aria-hidden="true" className="absolute inset-0 bg-oc-green-deep" />
    );
  }

  return (
    <>
      <div className="absolute inset-0 md:hidden">
        {assets.hero.src ? <Image src={assets.hero.src} alt={assets.hero.alt} fill priority sizes="100vw" placeholder="blur" blurDataURL={blurFor(assets.hero.src)} className="object-cover" style={{ objectPosition: assets.hero.focal }} /> : null}
      </div>
      <video ref={videoRef} className="absolute inset-0 hidden h-full w-full object-cover md:block" src={video.src ?? undefined} poster={video.poster ?? undefined} muted loop playsInline autoPlay preload="metadata" disablePictureInPicture aria-hidden="true" tabIndex={-1} onError={() => setFailed(true)} />
    </>
  );
}

export function Hero() {
  return (
    <>
    <section
      id="explore"
      aria-label={`${estateName} — ${locationLine}`}
      className="relative isolate flex min-h-svh flex-col overflow-hidden bg-oc-ink-deep text-oc-paper [--hero-parallax:0%] [--hero-progress:0] [--hero-scale:1.04]"
    >
      <div className="hero-media z-0">
        <HeroMedia />
      </div>
      <div aria-hidden="true" className="hero-grade absolute inset-0 z-[1]" />

      {/* Composition: type sits in the lower-left, where the grade is deepest
          and the aerial is darkest. Legibility is compositional, not a wash. */}
      <div className="is-in relative z-10 flex flex-1 items-end px-gut pb-6 pt-28 md:pb-10 md:pt-32">
        <div className="mx-auto w-full max-w-shell">
          <p className="mask mb-5 md:mb-7" style={{ "--i": 0 } as React.CSSProperties}>
            <span className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-oc-paper/75">{locationLine}</span>
          </p>

          <h1 className="max-w-[8ch] font-serif text-[clamp(3.6rem,17vw,7rem)] leading-[0.84] text-oc-paper md:max-w-none md:text-display">
            <span className="mask" style={{ "--i": 1 } as React.CSSProperties}>
              <span>{estateName.split(" ")[0]}</span>
            </span>
            <span className="mask md:pl-[0.14em]" style={{ "--i": 2 } as React.CSSProperties}>
              <span>{estateName.split(" ").slice(1).join(" ")}</span>
            </span>
          </h1>

          <div className="mt-6 flex items-start gap-3 md:mt-9 md:gap-5">
            <span aria-hidden="true" className="rule-draw mt-[0.85em] h-px w-10 shrink-0 origin-left bg-oc-orange md:w-16" style={{ "--i": 3 } as React.CSSProperties} />
            <p data-reveal style={{ "--i": 4 } as React.CSSProperties} className="max-w-[26ch] font-serif text-h2 italic leading-[1.05] text-oc-paper/95">
              {positioning.tagline}
            </p>
          </div>

          <div data-reveal style={{ "--i": 5 } as React.CSSProperties} className="mt-9 flex flex-col gap-2.5 sm:flex-row md:mt-12">
            <Action href="#positioning" variant="primary" className="w-full sm:w-auto">
              Explore the estate
            </Action>
            {whatsappHref ? (
              <Action href={whatsappHref} variant="ghost-dark" className="w-full sm:w-auto">
                Talk to an agent
              </Action>
            ) : null}
          </div>
        </div>
      </div>

      <div
        aria-hidden="true"
        className="hero-scroll-cue pointer-events-none absolute bottom-[7.5rem] right-gut z-10 hidden h-14 w-px md:block"
        style={{ opacity: "calc(1 - min(1, var(--hero-progress) * 6))" }}
      >
        <span />
      </div>
    </section>

      <div className="hero-facts overflow-hidden border-b border-oc-line bg-oc-paper text-oc-ink" aria-label="Estate facts">
        <div className="hero-facts-track flex min-w-max items-center gap-10 py-4 md:gap-16 md:py-5">
          {[...rail, ...rail].map((item, index) => (
            <div
              key={`${item.label}-${index}`}
              className="flex items-baseline gap-3 whitespace-nowrap px-1 font-mono text-[0.6875rem] uppercase tracking-[0.14em]"
              /* Second copy of the rail exists only so the marquee loops
                 seamlessly; hide it from assistive tech so the four facts are
                 not announced twice. */
              aria-hidden={index >= rail.length ? true : undefined}
            >
              <span className="text-oc-ink-soft">{item.label}</span>
              <span className="text-oc-green">{item.value}</span>
              <span aria-hidden="true" className="text-oc-orange">/</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
