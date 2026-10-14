import Image from "next/image";
import type { MediaAsset } from "@/content/assets";
import type { Estate } from "@/content/estates";
import { blurFor } from "@/lib/media";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";


/**
 * One of the TWO places cards are allowed (AGENTS.md rule 4). Every facility
 * has `body: null`, so the card is composed to work on image and label alone —
 * a tall frame with the label set into the image, not a text card with a hole.
 */
export function Facilities({ estate }: { estate: Estate }) {
  const facilities = estate.facilities;
  const facilityMedia: MediaAsset[] = estate.media.facilities;
  if (facilities.length === 0) return null;
  const hasImages = facilityMedia.some((media) => media?.src);
  return (
    <InView as="section" id="facilities" aria-label="Facilities" className="bg-oc-paper-warm py-sec text-oc-ink" amount={0.08}>
      <Shell>
        <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between md:gap-10">
          <div>
            <Heading lines={["The shared", "amenities."]} size="h1" className="max-w-[14ch]" />
            {hasImages ? (
              <p data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-5 font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-ink-soft">
                Shown as 3D renders
              </p>
            ) : null}
          </div>
          <Eyebrow index={2} className="md:pb-3">
            Facilities
          </Eyebrow>
        </div>

        <ul className={`mt-12 grid gap-3 sm:grid-cols-2 sm:gap-4 md:mt-16 lg:gap-5 ${hasImages ? "grid-cols-1 lg:grid-cols-4" : "grid-cols-2 lg:grid-cols-3"}`}>
          {facilities.map((facility, index) => {
            const media = facilityMedia[index];
            return (
              <li key={facility.title} data-reveal style={{ "--i": index } as React.CSSProperties}>
                <article className={`group relative isolate overflow-hidden rounded-[18px] bg-oc-ink-deep text-oc-paper ${hasImages ? "aspect-[4/5] lg:aspect-[3/4]" : "aspect-[4/3] card-noise"}`}>
                  {media?.src ? (
                    <Image
                      src={media.src}
                      alt={media.alt}
                      fill
                      loading="lazy"
                      sizes="(min-width: 1024px) 24vw, (min-width: 640px) 46vw, 92vw"
                      placeholder="blur"
                      blurDataURL={blurFor(media.src)}
                      className="object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                    />
                  ) : null}

                  <div aria-hidden="true" className="absolute inset-0 bg-gradient-to-t from-oc-ink-deep/85 via-oc-ink-deep/10 to-transparent" />
                  <span aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-[18px] border border-oc-paper/12" />

                  <span className="absolute left-4 top-4 font-mono text-[0.625rem] tracking-[0.16em] text-oc-paper/70">{String(index + 1).padStart(2, "0")}</span>

                  <h3 className="absolute inset-x-4 bottom-4 font-serif text-h3 leading-tight">{facility.title}</h3>
                </article>
              </li>
            );
          })}
        </ul>
      </Shell>
    </InView>
  );
}
