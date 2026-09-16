import Image from "next/image";
import { landmarks } from "@/content/orange-county";
import { landmarkImages, type MediaAsset } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/**
 * Rows, not cards. AGENTS.md rule 4 permits cards in exactly two places —
 * Facilities and Plot Pricing — so this is an editorial list: hairline,
 * index, copy, photograph. The photographs are real, not renders.
 */
export function Landmarks() {
  return (
    <InView as="section" id="landmarks" aria-label="Nearby landmarks" className="bg-oc-paper py-sec text-oc-ink" amount={0.06}>
      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["What's around", "the estate."]} size="h1" className="max-w-[14ch]" />
          <Eyebrow index={2} className="md:pb-3">
            Nearby
          </Eyebrow>
        </div>

        <ol className="mt-12 md:mt-20">
          {landmarks.map((landmark, index) => {
            const photoSource = landmarkImages[index];
            const photos = Array.isArray(photoSource) ? photoSource : photoSource ? [photoSource] : [];
            const validPhotos = photos.filter((photo): photo is MediaAsset & { src: string } => typeof photo.src === "string");
            return (
              <li key={landmark.title} className="border-t border-oc-line py-8 last:border-b md:py-12">
                <div className="grid grid-cols-1 gap-6 md:grid-cols-12 md:gap-10">
                  <div className="flex items-start gap-4 md:col-span-6 lg:col-span-5">
                    <span data-reveal style={{ "--i": 0 } as React.CSSProperties} className="mt-1.5 font-mono text-[0.6875rem] tracking-[0.16em] text-oc-orange">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <div>
                      <h3 className="mask font-serif text-h2 leading-[1.05]" style={{ "--i": 1 } as React.CSSProperties}>
                        <span>{landmark.title}</span>
                      </h3>
                      {landmark.body ? (
                        <p data-reveal style={{ "--i": 2 } as React.CSSProperties} className="mt-4 max-w-[46ch] text-body leading-relaxed text-oc-ink-soft">
                          {landmark.body}
                        </p>
                      ) : null}
                    </div>
                  </div>

                  {photos[0]?.src ? (
                    <figure data-reveal style={{ "--i": 2 } as React.CSSProperties} className="relative aspect-[16/10] overflow-hidden md:col-span-5 md:col-start-8 md:aspect-[4/3]">
                      {validPhotos.map((photo, photoIndex) => (
                        <Image
                          key={photo.src}
                            src={photo.src}
                          alt={photo.alt}
                          fill
                          loading="lazy"
                          sizes="(min-width: 810px) 38vw, 100vw"
                          placeholder="blur"
                          blurDataURL={blurFor(photo.src)}
                          className={photos.length > 1 ? `landmark-slide landmark-slide-${photoIndex}` : "object-cover"}
                        />
                      ))}
                    </figure>
                  ) : null}
                </div>
              </li>
            );
          })}
        </ol>
      </Shell>
    </InView>
  );
}
