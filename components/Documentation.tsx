import { documentation, landTitle } from "@/content/orange-county";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/**
 * No photograph ships with this section on purpose. The only available image
 * was a fragment of a deck slide, and a stock certificate would imply a
 * document that does not yet exist. AGENTS.md rule 2: the items render
 * verbatim, and nothing here states that the C of O has been issued.
 */
export function Documentation() {
    return (
    <InView as="section" id="documentation" aria-label="Documentation" className="relative isolate overflow-hidden bg-oc-ink-deep py-sec-lg text-oc-paper" amount={0.12}>
      <div aria-hidden="true" className="card-noise absolute inset-0 -z-10 opacity-50" />

      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["What you get", "on paper."]} size="h1" className="max-w-[14ch] text-oc-paper" />
          <Eyebrow index={2} className="md:pb-3">
            Documentation
          </Eyebrow>
        </div>

        <div className="mt-14 grid gap-14 md:mt-20 md:grid-cols-[minmax(0,1.25fr)_minmax(18rem,0.75fr)] md:gap-20">
          <div>
            <p className="mb-5 font-mono text-[0.6875rem] uppercase tracking-[0.18em] text-oc-paper/55">What you get on paper</p>
            <ol>
              {documentation.items.map((item, index) => (
                <li key={item} className="border-t border-oc-paper/15 py-7 last:border-b md:py-9">
                  <div className="flex items-baseline gap-5 md:gap-10">
                    <span data-reveal style={{ "--i": index } as React.CSSProperties} className="font-mono text-[0.6875rem] tracking-[0.16em] text-oc-orange">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <span className="mask flex-1" style={{ "--i": index + 1 } as React.CSSProperties}>
                      <span className="font-serif text-h1 leading-[1.02]">{item}</span>
                    </span>
                  </div>
                </li>
              ))}
            </ol>
          </div>

          <div className="self-start border-t border-oc-orange pt-5 md:mt-12">
            <p className="font-mono text-[0.6875rem] uppercase tracking-[0.18em] text-oc-orange">Land title</p>
            <ol className="mt-7">
              {landTitle.items.map((item, index) => (
                <li key={item} className="flex items-start justify-between gap-6 border-b border-oc-paper/15 py-5 first:border-t">
                  <span className="font-serif text-[clamp(1.5rem,3vw,2.4rem)] leading-none">{item}</span>
                  <span className="pt-1 font-mono text-[0.6875rem] tracking-[0.16em] text-oc-paper/50">{String(index + 1).padStart(2, "0")}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </Shell>
    </InView>
  );
}
