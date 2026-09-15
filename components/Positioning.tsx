import Image from "next/image";
import { developer, positioning } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { Eyebrow, InView, Rule, Shell } from "@/components/primitives";

/* The body is one sentence ending in an attribution. Split it so the
   attribution can be set as a credit line — the words are untouched. */
const marker = " Developed by ";
const cut = positioning.body.indexOf(marker);
const statement = cut > -1 ? positioning.body.slice(0, cut).trim() : positioning.body;
const credit = cut > -1 ? positioning.body.slice(cut).trim() : null;

export function Positioning() {
  return (
    <InView as="section" id="positioning" aria-label="About the estate" className="bg-oc-paper py-sec-lg text-oc-ink" amount={0.12}>
      <Shell>
        <div className="grid grid-cols-1 gap-10 md:grid-cols-12 md:gap-12">
          <div className="md:col-span-7 lg:col-span-6">
            <Eyebrow>The Estate</Eyebrow>
            <Rule className="mt-5" index={0} />

            {/* The single most important paragraph on the page. It is set at
                heading scale because it is the heading. */}
            <p data-reveal style={{ "--i": 1 } as React.CSSProperties} className="mt-8 max-w-[20ch] font-serif text-h1 leading-[0.98] md:mt-10">
              {statement}.
            </p>

            {credit ? (
              <p data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-8 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-oc-ink-soft">
                {credit}
              </p>
            ) : null}
          </div>

          <div className="md:col-span-5 md:col-start-8 lg:col-span-5 lg:col-start-8">
            {assets.positioning.src ? (
              <figure data-reveal style={{ "--i": 2 } as React.CSSProperties} className="relative aspect-[4/5] overflow-hidden md:-mt-6">
                <Image
                  src={assets.positioning.src}
                  alt={assets.positioning.alt}
                  fill
                  sizes="(min-width: 810px) 40vw, 100vw"
                  placeholder="blur"
                  blurDataURL={blurFor(assets.positioning.src)}
                  className="object-cover"
                  style={{ objectPosition: assets.positioning.focal }}
                />
                <figcaption className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-oc-ink-deep/80 to-transparent p-5 font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper">
                  {developer.name}
                </figcaption>
              </figure>
            ) : null}
          </div>
        </div>
      </Shell>
    </InView>
  );
}
