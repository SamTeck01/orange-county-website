import { plots } from "@/content/orange-county";
import { whatsappAbout } from "@/lib/site";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/**
 * The second and last place cards are permitted (AGENTS.md rule 4).
 * Every plot has `availability: null`. Nothing here shows a count, a
 * "selling fast" badge, or a plot number — the site must never imply that a
 * specific plot is available.
 */
export function PlotPricing() {
  return (
    <InView as="section" id="pricing" aria-label="Plot pricing" className="bg-oc-paper py-sec text-oc-ink" amount={0.08}>
      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["Choose", "your plot."]} size="h1" className="max-w-[12ch]" />
          <Eyebrow index={2} className="md:pb-3">
            Plot Pricing
          </Eyebrow>
        </div>

        <ul className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 md:mt-16 lg:grid-cols-4 lg:gap-5">
          {plots.map((plot, index) => {
            const enquire = whatsappAbout(`the ${plot.size} plot`);
            return (
              <li key={plot.size} data-reveal style={{ "--i": index } as React.CSSProperties}>
                <article className="group flex h-full flex-col rounded-[18px] border border-oc-line bg-oc-paper-warm p-6 transition-colors duration-500 hover:border-oc-orange md:p-7">
                  <p className="font-mono text-[0.6875rem] uppercase tracking-[0.14em] text-oc-ink-soft">{plot.size}</p>

                  <p className="mt-6 font-serif text-h2 leading-none md:mt-8">{plot.display}</p>

                  <span aria-hidden="true" className="mt-6 block h-px w-full bg-oc-line md:mt-8" />

                  {enquire ? (
                    <a
                      href={enquire}
                      rel="noopener noreferrer"
                      className="mt-5 inline-flex min-h-12 items-center justify-between gap-3 font-mono text-[0.6875rem] uppercase tracking-[0.12em] text-oc-ink transition-colors duration-300 group-hover:text-oc-orange-deep"
                    >
                      Enquire
                      <span aria-hidden="true" className="transition-transform duration-500 ease-out group-hover:translate-x-1">→</span>
                    </a>
                  ) : null}
                </article>
              </li>
            );
          })}
        </ul>
      </Shell>
    </InView>
  );
}
