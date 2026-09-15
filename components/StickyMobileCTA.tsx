"use client";

import { useEffect, useState } from "react";
import { contact } from "@/content/orange-county";
import { telHref, whatsappHref } from "@/lib/site";

/**
 * Mobile primary (AGENTS.md rule 5). Hidden until the hero has scrolled past,
 * so it never covers the hero's own calls to action. Both targets are 56px.
 */
export function StickyMobileCTA() {
  const [visible, setVisible] = useState(false);
  const phone = contact.phones[0];

  useEffect(() => {
    const hero = document.getElementById("explore");
    if (!hero) return;
    const observer = new IntersectionObserver(([entry]) => setVisible(!entry.isIntersecting), { threshold: 0 });
    observer.observe(hero);
    return () => observer.disconnect();
  }, []);

  if (!whatsappHref && !phone) return null;

  return (
    <div
      className={`fixed inset-x-0 bottom-0 z-40 grid grid-cols-2 gap-px border-t border-oc-ink/10 bg-oc-ink/10 transition-transform duration-500 ease-out md:hidden ${
        visible ? "translate-y-0" : "translate-y-full"
      }`}
      style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
    >
      {whatsappHref ? (
        <a href={whatsappHref} rel="noopener noreferrer" className="flex min-h-14 items-center justify-center bg-oc-orange font-mono text-[0.6875rem] uppercase tracking-[0.12em] text-oc-ink">
          WhatsApp
        </a>
      ) : null}
      {phone ? (
        <a href={telHref(phone)} rel="noopener noreferrer" className="flex min-h-14 items-center justify-center bg-oc-ink-deep font-mono text-[0.6875rem] uppercase tracking-[0.12em] text-oc-paper">
          Call
        </a>
      ) : null}
    </div>
  );
}
