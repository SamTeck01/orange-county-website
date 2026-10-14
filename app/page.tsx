import Image from "next/image";
import { estates, oyo } from "@/content/estates";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";

/**
 * The entry: a chooser over the estate aerial. Every visitor picks a branch
 * first; each branch is its own page at /oyo and /epe.
 */
export default function Home() {
  const backdrop = oyo.media.hero;

  return (
    <main id="main-content" className="relative isolate flex min-h-svh items-center justify-center overflow-hidden bg-oc-ink-deep px-4 py-10 text-oc-paper">
      {backdrop.src ? (
        <Image src={backdrop.src} alt="" fill priority sizes="100vw" placeholder="blur" blurDataURL={blurFor(backdrop.src)} className="-z-20 scale-105 object-cover blur-[6px]" />
      ) : null}
      <div aria-hidden="true" className="absolute inset-0 -z-10 bg-oc-ink-deep/70" />

      <section role="dialog" aria-modal="true" aria-labelledby="chooser-title" className="w-full max-w-3xl bg-oc-paper p-5 text-oc-ink sm:p-8 md:p-10">
        <div className="flex items-center gap-3">
          {assets.logo.src ? <Image src={assets.logo.src} alt={assets.logo.alt} width={40} height={40} className="h-10 w-10 object-contain" /> : null}
          <p className="font-mono text-[0.6875rem] uppercase tracking-[0.18em] text-oc-ink-soft">{oyo.developer.name}</p>
        </div>

        <h1 id="chooser-title" className="mt-6 font-serif text-h1 leading-[0.95]">
          Which Orange County
          <br />
          would you like to see?
        </h1>

        <ul className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2 md:mt-10 md:gap-4">
          {estates.map((estate) => (
            <li key={estate.slug}>
              <a href={`/${estate.slug}`} className="group relative isolate flex aspect-[4/3] items-end overflow-hidden bg-oc-ink-deep p-5 text-oc-paper focus-visible:outline-offset-4 sm:aspect-[4/5]">
                {estate.media.hero.src ? (
                  <Image
                    src={estate.slug === "epe" ? (estate.media.positioning.src ?? estate.media.hero.src) : estate.media.hero.src}
                    alt=""
                    fill
                    sizes="(min-width: 640px) 360px, 92vw"
                    placeholder="blur"
                    blurDataURL={blurFor(estate.media.hero.src)}
                    className="-z-20 object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                  />
                ) : null}
                <span aria-hidden="true" className="absolute inset-0 -z-10 bg-gradient-to-t from-oc-ink-deep/90 via-oc-ink-deep/30 to-transparent" />
                <span className="flex w-full items-end justify-between gap-4">
                  <span>
                    <span className="block font-serif text-h2 leading-none">Orange County {estate.label}</span>
                    <span className="mt-2 block font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper/75">{estate.area}</span>
                  </span>
                  <span aria-hidden="true" className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-oc-orange text-oc-ink transition-transform duration-500 group-hover:translate-x-1">
                    →
                  </span>
                </span>
              </a>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
