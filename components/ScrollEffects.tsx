"use client";

import { useEffect } from "react";
import { useReducedMotion } from "@/lib/useReducedMotion";

/**
 * Every scroll-driven effect on the site, in one rAF loop that writes CSS
 * custom properties. Nothing here touches React state — a setState per frame
 * would re-render the tree 60 times a second (AGENTS.md rule 6).
 *
 * The loop is split into read → compute → write. That split is the whole
 * point: a style write invalidates layout, so reading a rect after writing
 * forces the browser to lay the page out again. Interleaving them meant one
 * forced reflow per card per frame, which is what made the stack feel like it
 * was dragging behind the scroll on slower devices.
 */
export function ScrollEffects() {
  const reduced = useReducedMotion();

  useEffect(() => {
    if (reduced) return;

    let frame = 0;
    let cards: HTMLElement[] = [];
    /* Heights are cached, not read per frame. offsetHeight is itself a
       layout-forcing read, and a card's height only changes on resize or when
       an image finishes loading — both of which a ResizeObserver catches. */
    let heights: number[] = [];

    const measure = () => {
      heights = cards.map((card) => card.offsetHeight);
    };

    const update = () => {
      frame = 0;

      // ---- READ ----------------------------------------------------------
      const hero = document.getElementById("explore");
      const heroRect = hero?.getBoundingClientRect() ?? null;
      const tops = cards.map((card) => card.getBoundingClientRect().top);

      // ---- COMPUTE -------------------------------------------------------
      const heroProgress = heroRect
        ? Math.min(1, Math.max(0, -heroRect.top / Math.max(1, heroRect.height)))
        : 0;

      /* A card's exit is driven by how far the NEXT card has slid over it.
         Measuring the overlap directly avoids runway arithmetic, and
         getBoundingClientRect() on a stuck element returns its stuck
         position — exactly the value we want to compare. */
      const exits = cards.map((_, i) => {
        if (i === cards.length - 1) return 0;
        const height = heights[i] || 1;
        const covered = tops[i] + height - tops[i + 1];
        return Math.min(1, Math.max(0, covered / height));
      });

      // ---- WRITE ---------------------------------------------------------
      if (hero) {
        hero.style.setProperty("--hero-parallax", `${heroProgress * 9}%`);
        hero.style.setProperty("--hero-progress", `${heroProgress}`);
      }
      for (let i = 0; i < cards.length; i += 1) {
        cards[i].style.setProperty("--exit", exits[i].toFixed(3));
      }
    };

    const onScroll = () => {
      if (!frame) frame = window.requestAnimationFrame(update);
    };

    cards = Array.from(document.querySelectorAll<HTMLElement>("[data-stack-card]"));
    measure();
    update();

    const observer = new ResizeObserver(() => {
      measure();
      onScroll();
    });
    cards.forEach((card) => observer.observe(card));

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });

    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, [reduced]);

  return null;
}
