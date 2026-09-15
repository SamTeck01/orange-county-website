import Image from "next/image";
import { location } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { Eyebrow, Heading, InView, Rule, Shell } from "@/components/primitives";

export function Location() {
  /* content.location.coordinates is null — there is no GPS point in the
     brief, so this renders as a place, not as a map with a dropped pin. */
  const area = location.area.replace(/\.$/, "");

  return (
    <InView as="section" id="location" aria-label="Location" className="overflow-hidden bg-oc-paper-warm py-sec text-oc-ink" amount={0.1}>
      <Shell>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-12 md:items-end">
          <div className="md:col-span-8">
            <Eyebrow>Location</Eyebrow>
            <Heading lines={[area]} size="display" offset={1} className="mt-6 leading-[0.88]" />
          </div>
          <div className="md:col-span-4 md:pb-3">
            <Rule tone="orange" index={2} className="max-w-24" />
            <p data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-4 font-mono text-[0.75rem] uppercase tracking-[0.16em] text-oc-ink-soft">
              {location.road}
            </p>
          </div>
        </div>
      </Shell>

      {/* Full-bleed on purpose: the place should feel wider than the page. */}
      {assets.locationMap.src ? (
        <figure data-reveal style={{ "--i": 4 } as React.CSSProperties} className="relative mt-10 h-[48svh] w-full md:mt-16 md:h-[68svh]">
          <Image
            src={assets.locationMap.src}
            alt={assets.locationMap.alt}
            fill
            sizes="100vw"
            placeholder="blur"
            blurDataURL={blurFor(assets.locationMap.src)}
            className="object-cover"
            style={{ objectPosition: assets.locationMap.focal }}
          />
          <figcaption className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-oc-ink-deep/75 to-transparent px-gut pb-5 pt-16">
            <span className="mx-auto block max-w-shell font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper/85">{assets.locationMap.alt}</span>
          </figcaption>
        </figure>
      ) : null}
    </InView>
  );
}
