"use client";

import { useEffect, useRef, useState } from "react";
import Image from "next/image";
import { contact } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { estateName, whatsappHref } from "@/lib/site";

const nav = [
  { label: "The estate", href: "#positioning" },
  { label: "Features", href: "#features" },
  { label: "Location", href: "#location" },
  { label: "Masterplan", href: "#masterplan" },
  { label: "Pricing", href: "#pricing" },
];

export function Header() {
  const [solid, setSolid] = useState(false);
  const [open, setOpen] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);

  /* One state flip, not one per frame: the header solidifies when the hero
     leaves the viewport. IntersectionObserver, not a scroll handler. */
  useEffect(() => {
    const hero = document.getElementById("explore");
    if (!hero) {
      setSolid(true);
      return;
    }
    const observer = new IntersectionObserver(([entry]) => setSolid(!entry.isIntersecting), { rootMargin: "-72px 0px 0px 0px" });
    observer.observe(hero);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open]);

  const tel = contact.phones[0] ? `tel:+234${contact.phones[0].replace(/^0/, "")}` : null;

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-colors duration-500 ${
        solid ? "border-b border-oc-line bg-oc-paper/90 text-oc-ink backdrop-blur-md" : "border-b border-transparent text-oc-paper"
      }`}
    >
      <div className="mx-auto flex max-w-shell items-center justify-between gap-6 px-gut py-3.5 md:py-4">
        <a href="#explore" className="flex items-center gap-2.5 font-serif text-lg leading-none tracking-tight md:text-xl">
          <Image src={assets.logo.src ?? ""} alt={assets.logo.alt} width={36} height={36} sizes="36px" className="h-8 w-8 object-contain md:h-9 md:w-9" />
          {estateName}
        </a>

        <nav aria-label="Sections" className="hidden items-center gap-8 lg:flex">
          {nav.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className={`font-mono text-[0.6875rem] uppercase tracking-[0.14em] transition-opacity duration-300 hover:opacity-60 ${solid ? "text-oc-ink-soft" : "text-oc-paper/80"}`}
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          {whatsappHref ? (
            <a
              href={whatsappHref}
              rel="noopener noreferrer"
              className="hidden min-h-11 items-center bg-oc-orange px-5 font-mono text-[0.6875rem] uppercase tracking-[0.12em] text-oc-ink transition-colors duration-300 hover:bg-oc-orange-deep md:inline-flex"
            >
              Enquire
            </a>
          ) : null}

          <button
            type="button"
            onClick={() => setOpen(true)}
            aria-label="Open menu"
            aria-expanded={open}
            className="inline-flex h-11 w-11 items-center justify-center lg:hidden"
          >
            <span aria-hidden="true" className="relative block h-2.5 w-6">
              <span className={`absolute inset-x-0 top-0 h-px ${solid ? "bg-oc-ink" : "bg-oc-paper"}`} />
              <span className={`absolute inset-x-0 bottom-0 h-px ${solid ? "bg-oc-ink" : "bg-oc-paper"}`} />
            </span>
          </button>
        </div>
      </div>

      {open ? (
        <div ref={panelRef} role="dialog" aria-modal="true" aria-label="Menu" className="fixed inset-0 z-50 flex flex-col bg-oc-ink-deep text-oc-paper lg:hidden">
          <div className="flex items-center justify-between px-gut py-3.5">
            <span className="font-serif text-lg">{estateName}</span>
            <button type="button" onClick={() => setOpen(false)} aria-label="Close menu" className="inline-flex h-11 w-11 items-center justify-center font-mono text-2xl leading-none">
              ×
            </button>
          </div>

          <nav aria-label="Sections" className="flex flex-1 flex-col justify-center gap-1 px-gut pb-16">
            {nav.map((item, index) => (
              <a
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="flex items-baseline gap-4 border-b border-oc-paper/10 py-4 font-serif text-h2"
              >
                <span className="font-mono text-[0.625rem] tracking-[0.16em] text-oc-orange">{String(index + 1).padStart(2, "0")}</span>
                {item.label}
              </a>
            ))}
          </nav>

          <div className="grid grid-cols-2 gap-px border-t border-oc-paper/15 bg-oc-paper/15">
            {whatsappHref ? (
              <a href={whatsappHref} rel="noopener noreferrer" className="flex min-h-14 items-center justify-center bg-oc-orange font-mono text-[0.6875rem] uppercase tracking-[0.12em] text-oc-ink">
                WhatsApp
              </a>
            ) : null}
            {tel ? (
              <a href={tel} rel="noopener noreferrer" className="flex min-h-14 items-center justify-center bg-oc-ink-deep font-mono text-[0.6875rem] uppercase tracking-[0.12em] text-oc-paper">
                Call
              </a>
            ) : null}
          </div>
        </div>
      ) : null}
    </header>
  );
}
