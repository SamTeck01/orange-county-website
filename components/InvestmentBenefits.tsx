import { benefits } from "@/content/orange-county";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/* benefits[3] — "Strategic Growth Corridor Advantage" — is rendered by
   GrowthCorridor as its own interstitial. Showing it twice was one of the
   duplications in the previous build. */
const shown = benefits.filter((_, index) => index !== 3);

export function InvestmentBenefits() {
  return (
    <InView as="section" id="benefits" aria-label="Investment benefits" className="bg-oc-paper py-sec text-oc-ink" amount={0.05}>
      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["Why buy", "here."]} size="h1" className="max-w-[12ch]" />
          <Eyebrow index={2} className="md:pb-3">
            Investment Benefits
          </Eyebrow>
        </div>

        <ol className="mt-12 md:mt-20">
          {shown.map((benefit, index) => {
            const hasDetail = Boolean(benefit.lead) || benefit.points.length > 0;

            return (
              <li key={benefit.title} className="border-t border-oc-line py-8 last:border-b md:py-11">
                <div className="grid grid-cols-1 gap-5 md:grid-cols-12 md:gap-10">
                  <div className={`flex items-start gap-4 ${hasDetail ? "md:col-span-5" : "md:col-span-9"}`}>
                    <span data-reveal className="mt-1.5 font-mono text-[0.6875rem] tracking-[0.16em] text-oc-orange">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    {/* Where the client has given us no supporting copy, the
                        title carries the row alone at a larger size rather than
                        sitting next to an empty column. */}
                    <h3 className={`mask font-serif leading-[1.04] ${hasDetail ? "text-h2" : "text-h1"}`} style={{ "--i": 1 } as React.CSSProperties}>
                      <span>{benefit.title}</span>
                    </h3>
                  </div>

                  {hasDetail ? (
                    <div className="md:col-span-6 md:col-start-7">
                      {benefit.lead ? (
                        <p data-reveal style={{ "--i": 2 } as React.CSSProperties} className="max-w-[52ch] text-lead leading-relaxed text-oc-ink-soft">
                          {benefit.lead}
                        </p>
                      ) : null}

                      {benefit.points.length > 0 ? (
                        <ul className="mt-5 flex flex-wrap gap-x-6 gap-y-2.5">
                          {benefit.points.map((point, pointIndex) => (
                            <li
                              key={point}
                              data-reveal
                              style={{ "--i": pointIndex + 3 } as React.CSSProperties}
                              className="flex items-center gap-2.5 font-mono text-[0.75rem] uppercase tracking-[0.1em] text-oc-ink"
                            >
                              <span aria-hidden="true" className="block h-1.5 w-1.5 shrink-0 rounded-full bg-oc-orange" />
                              {point}
                            </li>
                          ))}
                        </ul>
                      ) : null}
                    </div>
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
