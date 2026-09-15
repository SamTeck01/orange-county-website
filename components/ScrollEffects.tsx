"use client";

import { useEffect } from "react";
import { useReducedMotion } from "@/lib/useReducedMotion";

/**
 * Every scroll-driven effect on the site, in one rAF loop that writes CSS
 * custom properties. Nothing here touches React state — a setState per frame
 * would re-render the tree 60 times a second (AGENTS.md rule 6).
 */
export function ScrollEffects() {
  const reduced = useReducedMotion();

  useEffect(() => {
    if (reduced) return;

    let frame = 0;
    let cards: HTMLElement[] = [];
    const collect = () => {
      cards = Array.from(document.querySelectorAll<HTMLElement>("[data-stack-card]"));
    };

    const update = () => {
      frame = 0;

      /* Hero — slow parallax on the media bed, and a progress value the
         scroll cue fades against. */
      const hero = document.getElementById("explore");
      if (hero) {
        const rect = hero.getBoundingClientRect();
        const progress = Math.min(1, Math.max(0, -rect.top / Math.max(1, rect.height)));
        hero.style.setProperty("--hero-parallax", `${progress * 9}%`);
        hero.style.setProperty("--hero-progress", `${progress}`);
      }

      /* Feature stack — a card's exit is driven by how far the NEXT card has
         slid over it. Measuring the overlap directly avoids doing runway
         arithmetic, and getBoundingClientRect() on a stuck element returns
         its stuck position, which is exactly what we want to compare. */
      for (let i = 0; i < cards.length; i += 1) {
        const card = cards[i];
        const next = cards[i + 1];
        if (!next) {
          card.style.setProperty("--exit", "0");
          continue;
        }
        const rect = card.getBoundingClientRect();
        // Scale is applied to this card, so use the untransformed height.
        const height = card.offsetHeight || rect.height;
        const covered = rect.top + height - next.getBoundingClientRect().top;
        const exit = Math.min(1, Math.max(0, covered / Math.max(1, height)));
        card.style.setProperty("--exit", exit.toFixed(4));
      }
    };

    const onScroll = () => {
      if (!frame) frame = window.requestAnimationFrame(update);
    };

    collect();
    update();

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });

    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, [reduced]);

  return null;
}
