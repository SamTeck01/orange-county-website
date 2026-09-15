"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import type { MediaAsset } from "@/content/assets";
import { blurFor } from "@/lib/media";

export type MasterplanModel = string | null;

/**
 * A lightbox, not an interactive plan. Nothing on the masterplan is clickable
 * per plot: the site must never imply that a particular plot is available.
 */
export function MasterplanViewer({ model, poster }: { model: MasterplanModel; poster: MediaAsset }) {
  const [open, setOpen] = useState(false);
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open]);

  if (!poster.src) return null;

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Enlarge the masterplan"
        className="group relative block aspect-[16/10] w-full overflow-hidden rounded-[20px] border border-oc-paper/12 bg-oc-ink md:aspect-[16/9] md:rounded-[24px]"
      >
        <Image
          src={poster.src}
          alt={poster.alt}
          fill
          loading="lazy"
          sizes="100vw"
          placeholder="blur"
          blurDataURL={blurFor(poster.src)}
          className="object-contain p-3 transition-transform duration-700 ease-out group-hover:scale-[1.02] md:p-6"
        />
        <span
          aria-hidden="true"
          className="absolute bottom-4 right-4 inline-flex h-11 w-11 items-center justify-center rounded-full bg-oc-orange text-oc-ink transition-transform duration-500 ease-out group-hover:scale-110"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" className="h-4 w-4">
            <path d="M4 10V4h6M20 14v6h-6M20 10V4h-6M4 14v6h6" />
          </svg>
        </span>
      </button>

      {open ? (
        <div role="dialog" aria-modal="true" aria-label="Masterplan" className="fixed inset-0 z-[60] flex flex-col bg-oc-ink-deep/97">
          <div className="flex items-center justify-between px-gut py-4">
            <p className="max-w-[60ch] font-mono text-[0.625rem] uppercase leading-relaxed tracking-[0.16em] text-oc-paper/65">Masterplan</p>
            <button ref={closeRef} type="button" onClick={() => setOpen(false)} aria-label="Close masterplan" className="inline-flex h-11 w-11 items-center justify-center font-mono text-2xl leading-none text-oc-paper">
              ×
            </button>
          </div>
          <div className="relative flex-1">
            <Image src={poster.src} alt={poster.alt} fill sizes="96vw" placeholder="blur" blurDataURL={blurFor(poster.src)} className="object-contain p-3 md:p-8" />
          </div>
        </div>
      ) : null}

      {/* Reserved for a future orbit viewer. The model is intentionally null. */}
      {model ? <span hidden data-model={model} /> : null}
    </>
  );
}
