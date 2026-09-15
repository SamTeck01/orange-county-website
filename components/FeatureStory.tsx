"use client";

import Image from "next/image";
import { features } from "@/content/orange-county";
import { assets, type MediaAsset } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

const featureMedia: MediaAsset[] = [assets.featureRoad, assets.featureSolar, assets.featureCctv, assets.featureGated];

/**
 * Drawn coverage motif — used where there is no photograph.
 * No render in the 3D package contains a camera, and a stock CCTV photo
 * would be a claim we cannot support. The absence becomes the design:
 * this is the one dark card in the sequence.
 */
function CoverageMotif() {
  return (
    <div aria-hidden="true" className="relative h-full w-full overflow-hidden rounded-[20px] border border-oc-paper/10 bg-oc-ink-deep">
      <div className="absolute bottom-0 left-0 h-full w-full">
        {[0.28, 0.5, 0.72, 0.94, 1.16].map((scale, index) => (
          <span
            key={scale}
            className="absolute rounded-full border border-oc-paper/15"
            style={{
              left: "12%",
              bottom: "14%",
              width: `${scale * 140}%`,
              aspectRatio: "1",
              transform: "translate(-50%, 50%)",
              opacity: 1 - index * 0.16,
            }}
          />
        ))}
        <span className="absolute left-[12%] bottom-[14%] block h-2.5 w-2.5 -translate-x-1/2 translate-y-1/2 rounded-full bg-oc-orange" />
        <span className="absolute left-[12%] bottom-[14%] block h-2.5 w-2.5 -translate-x-1/2 translate-y-1/2 animate-ping rounded-full bg-oc-orange/60 motion-reduce:animate-none" />
      </div>
      <p className="absolute bottom-5 right-5 text-right font-mono text-[0.625rem] uppercase leading-relaxed tracking-[0.14em] text-oc-paper/45">
        Monitored
        <br />
        day and night
      </p>
    </div>
  );
}

function FeatureCard({ index, total }: { index: number; total: number }) {
  const feature = features[index];
  const asset = featureMedia[index];
  const isLast = index === total - 1;
  const hasMedia = Boolean(asset?.src);

  return (
    <article
      data-stack-card
      data-last={isLast ? "true" : "false"}
      style={
        {
          // Each card parks a little lower than the one before, so the stack
          // shows a stepped edge instead of a single flat slab.
          "--stack-top": `${5.25 + index * 0.9}rem`,
          zIndex: index + 1,
        } as React.CSSProperties
      }
      className="stack-card relative isolate overflow-hidden rounded-[24px] bg-oc-ink-deep text-oc-paper md:rounded-[28px]"
    >
      {/* Blurred bed of the same image — gives the card depth behind the
          sharp inset, and means the card is never a flat rectangle. */}
      {hasMedia && asset.src ? (
        <div aria-hidden="true" className="absolute inset-0 -z-10 scale-110">
          <Image src={asset.src} alt="" fill sizes="100vw" className="object-cover blur-[26px]" placeholder="blur" blurDataURL={blurFor(asset.src)} />
        </div>
      ) : null}
      <div aria-hidden="true" className="card-noise absolute inset-0 -z-10 opacity-60" />
      <div aria-hidden="true" className="absolute inset-0 -z-10 bg-oc-ink-deep/55" />
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-[inherit] border border-oc-paper/10" />

        <div className="grid grid-cols-1 gap-7 p-6 md:min-h-[32rem] md:grid-cols-12 md:items-stretch md:gap-8 md:p-9 lg:min-h-[36rem] lg:p-11">
          {/* Text column */}
          <div className="flex flex-col md:col-span-6 lg:col-span-5">
            <div className="flex items-center gap-3 font-mono text-[0.6875rem] tracking-[0.14em]">
              <span className="text-oc-orange">{feature.n}</span>
              <span className="h-px w-8 bg-oc-paper/30" />
              <span className="text-oc-paper/50">{String(total).padStart(2, "0")}</span>
            </div>

            <h3 className="mt-5 max-w-[11ch] font-serif text-h1 leading-[0.94] text-oc-paper md:mt-7">{feature.title}</h3>

            {feature.body ? (
              <p className="mt-5 max-w-[42ch] text-body text-oc-paper/75 md:mt-auto md:pt-10">{feature.body}</p>
            ) : null}
          </div>

          {/* Media column */}
          <div className="md:col-span-6 md:col-start-7 lg:col-span-6 lg:col-start-7">
            <div className="relative aspect-[4/3] overflow-hidden rounded-[20px] md:h-full md:aspect-auto md:min-h-[18rem]">
              {hasMedia && asset.src ? (
                <>
                  <Image
                    src={asset.src}
                    alt={asset.alt}
                    fill
                    loading={index === 0 ? "eager" : "lazy"}
                    sizes="(min-width: 810px) 50vw, 100vw"
                    placeholder="blur"
                    blurDataURL={blurFor(asset.src)}
                    className="object-cover"
                    style={{ objectPosition: asset.focal }}
                  />
                  <span aria-hidden="true" className="pointer-events-none absolute inset-0 rounded-[20px] border border-oc-paper/15" />
                </>
              ) : (
                <CoverageMotif />
              )}
            </div>
          </div>
        </div>
      </article>
  );
}

export function FeatureStory() {
  return (
    <InView as="section" id="features" aria-label="Estate features" className="bg-oc-paper py-sec text-oc-ink" amount={0.05}>
      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["Planned into", "the estate."]} size="h1" className="max-w-[14ch]" />
          <Eyebrow index={2} className="md:pb-3">
            Estate Features
          </Eyebrow>
        </div>

        <div className="mt-12 md:mt-20">
          {features.map((feature, index) => (
            <FeatureCard key={feature.n} index={index} total={features.length} />
          ))}
        </div>
      </Shell>
    </InView>
  );
}
