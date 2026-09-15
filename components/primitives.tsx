"use client";

import { useEffect, useRef, type ElementType, type HTMLAttributes, type ReactNode } from "react";

/* ------------------------------------------------------------------
   InView — the single reveal mechanic for the site.
   Adds `is-in` once, then disconnects. CSS does the rest via
   [data-reveal] / .mask / .rule-draw. No React state, no re-render.
   ------------------------------------------------------------------ */

type InViewProps = {
  as?: ElementType;
  children: ReactNode;
  /** 0–1 of the element that must be visible. Large sections want a low value. */
  amount?: number;
} & HTMLAttributes<HTMLElement>;

export function InView({ as: Tag = "div", children, amount = 0.15, ...rest }: InViewProps) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      node.classList.add("is-in");
      return;
    }
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        node.classList.add("is-in");
        observer.disconnect();
      },
      { threshold: amount, rootMargin: "0px 0px -8% 0px" },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, [amount]);

  return (
    <Tag ref={ref} {...rest}>
      {children}
    </Tag>
  );
}

/* ------------------------------------------------------------------
   Typography
   ------------------------------------------------------------------ */

/** Small mono label. The site's only uppercase voice. */
export function Eyebrow({
  children,
  tone = "orange",
  className = "",
  index = 0,
}: {
  children: ReactNode;
  tone?: "orange" | "ink" | "paper" | "green";
  className?: string;
  index?: number;
}) {
  const tones = {
    orange: "text-oc-orange",
    ink: "text-oc-ink-soft",
    paper: "text-oc-paper/70",
    green: "text-oc-green",
  };
  return (
    <p
      data-reveal
      style={{ "--i": index } as React.CSSProperties}
      className={`font-mono text-[0.6875rem] uppercase leading-none tracking-[0.18em] ${tones[tone]} ${className}`}
    >
      {children}
    </p>
  );
}

/**
 * Display heading with a per-line masked reveal.
 * Instrument Serif is never set in all-caps at display size — the caps have
 * no optical correction and read cheap. Pass sentence case.
 */
export function Heading({
  lines,
  size = "h1",
  className = "",
  offset = 0,
  as: Tag = "h2",
}: {
  lines: string[];
  size?: "display" | "h1" | "h2";
  className?: string;
  offset?: number;
  as?: ElementType;
}) {
  const sizes = { display: "text-display", h1: "text-h1", h2: "text-h2" };
  return (
    <Tag className={`font-serif ${sizes[size]} ${className}`}>
      {lines.map((line, i) => (
        <span key={line + i} className="mask" style={{ "--i": i + offset } as React.CSSProperties}>
          <span>{line}</span>
        </span>
      ))}
    </Tag>
  );
}

/** Hairline that draws itself left-to-right when its section enters. */
export function Rule({ tone = "line", className = "", index = 0 }: { tone?: "line" | "orange" | "paper"; className?: string; index?: number }) {
  const tones = { line: "bg-oc-line", orange: "bg-oc-orange", paper: "bg-oc-paper/25" };
  return <span aria-hidden="true" style={{ "--i": index } as React.CSSProperties} className={`rule-draw block h-px w-full ${tones[tone]} ${className}`} />;
}

/* ------------------------------------------------------------------
   Controls
   ------------------------------------------------------------------ */

type ActionProps = {
  href: string;
  children: ReactNode;
  variant?: "primary" | "ghost" | "ghost-dark";
  className?: string;
} & Omit<HTMLAttributes<HTMLAnchorElement>, "children">;

/** 44px minimum target, everywhere, no exceptions. */
export function Action({ href, children, variant = "primary", className = "", ...rest }: ActionProps) {
  const variants = {
    primary: "bg-oc-orange text-oc-ink hover:bg-oc-orange-deep",
    ghost: "border border-oc-line text-oc-ink hover:border-oc-ink/40 hover:bg-oc-ink/[0.03]",
    "ghost-dark": "border border-oc-paper/35 text-oc-paper hover:border-oc-paper hover:bg-oc-paper/10",
  };
  const external = href.startsWith("http") || href.startsWith("tel:") || href.startsWith("mailto:");
  return (
    <a
      href={href}
      {...(external ? { rel: "noopener noreferrer" } : {})}
      className={`group inline-flex min-h-12 items-center justify-center gap-2.5 px-6 font-mono text-[0.6875rem] font-medium uppercase tracking-[0.12em] transition-colors duration-300 ${variants[variant]} ${className}`}
      {...rest}
    >
      {children}
    </a>
  );
}

/** Small green chip with a white uppercase label — carried over from the deck. */
export function Chip({ className = "", children }: { className?: string; children: ReactNode }) {
  return (
    <span className={`inline-flex min-h-7 items-center bg-oc-green px-2.5 py-1 font-mono text-[0.625rem] font-medium uppercase tracking-[0.1em] text-white ${className}`}>
      {children}
    </span>
  );
}

/** Consistent page shell: max width + fluid gutters. */
export function Shell({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <div className={`mx-auto w-full max-w-shell px-gut ${className}`}>{children}</div>;
}
