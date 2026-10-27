"use client";

import Image from "next/image";
import { useState } from "react";
import type { Estate } from "@/content/estates";
import { blurFor } from "@/lib/media";
import { Lightbox } from "@/components/Gallery";

type Letter = Estate["letters"][number];

/**
 * An official letter set as an editorial split: the scan on one side, its
 * finding quoted verbatim on the other. Tapping the scan opens it full screen.
 */
export function LetterViewer({ letter }: { letter: Letter }) {
  const [open, setOpen] = useState(false);
  if (!letter.image.src) return null;

  return (
    <div className="mt-20 grid items-center gap-10 border-t border-oc-paper/15 pt-14 md:mt-28 md:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)] md:gap-20 md:pt-20">
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label={`View the letter: ${letter.subject}`}
        className="group relative mx-auto block aspect-[1600/2318] w-full max-w-[22rem] overflow-hidden bg-oc-paper shadow-[0_30px_80px_-30px_rgba(0,0,0,0.7)] md:-rotate-2 md:transition-transform md:duration-500 md:hover:rotate-0"
      >
        <Image src={letter.image.src} alt={letter.image.alt} fill loading="lazy" sizes="(min-width: 768px) 22rem, 90vw" placeholder="blur" blurDataURL={blurFor(letter.image.src)} className="object-cover" />
      </button>

      <div>
        <p className="font-mono text-[0.6875rem] uppercase tracking-[0.18em] text-oc-orange">{letter.issuer}</p>
        <p className="mt-6 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-oc-paper/55">Re: {letter.subject}</p>
        <p className="mt-4 font-serif text-h2 leading-[1.05]">
          <span aria-hidden="true" className="text-oc-orange">“</span>
          {letter.finding}
          <span aria-hidden="true" className="text-oc-orange">”</span>
        </p>
        <p className="mt-6 font-mono text-[0.6875rem] tracking-[0.12em] text-oc-paper/55">
          {letter.reference} · {letter.date}
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <button type="button" onClick={() => setOpen(true)} className="inline-flex min-h-11 items-center rounded-full bg-oc-orange px-6 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-oc-ink transition-transform duration-300 hover:scale-105">
            View letter
          </button>
          <a href={letter.pdf} download className="inline-flex min-h-11 items-center rounded-full border border-oc-paper/30 px-6 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-oc-paper transition-colors hover:border-oc-paper">
            Download PDF
          </a>
        </div>
      </div>

      {open ? <Lightbox shots={[letter.image]} index={0} onIndex={() => {}} onClose={() => setOpen(false)} label="Letter" /> : null}
    </div>
  );
}
