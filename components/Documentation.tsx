import { documentation } from "@/content/orange-county";
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

        <ol className="mt-14 md:mt-20">
          {documentation.items.map((item, index) => (
            <li key={item} className="border-t border-oc-paper/15 py-7 last:border-b md:py-9">
              <div className="flex items-baseline gap-5 md:gap-10">
                <span data-reveal style={{ "--i": index } as React.CSSProperties} className="font-mono text-[0.6875rem] tracking-[0.16em] text-oc-orange">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span className="mask flex-1" style={{ "--i": index + 1 } as React.CSSProperties}>
                  {/* Verbatim. "C of O in View" is the client's own wording and
                      must never be softened into "C of O issued". */}
                  <span className="font-serif text-h1 leading-[1.02]">{item}</span>
                </span>
              </div>
            </li>
          ))}
        </ol>
      </Shell>
    </InView>
  );
}
