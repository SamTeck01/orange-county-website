import { assets } from "@/content/assets";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";
import { MasterplanViewer } from "@/components/MasterplanViewer";

/**
 * `model` stays null. The estate's 3D survey model must not be published on
 * this site, and no plot on the masterplan is ever clickable — nothing here
 * may imply a specific plot is available.
 */
export function Masterplan() {
  const model: string | null = null;

  return (
    <InView as="section" id="masterplan" aria-label="Masterplan" className="relative isolate overflow-hidden bg-oc-ink-deep py-sec text-oc-paper" amount={0.08}>
      <div aria-hidden="true" className="card-noise absolute inset-0 -z-10 opacity-40" />

      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["Explore the", "masterplan."]} size="h1" className="max-w-[14ch] text-oc-paper" />
          <div className="md:pb-3 md:text-right">
            <Eyebrow index={2}>Masterplan</Eyebrow>
            <p data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-3 font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-paper/55">
              Tap to enlarge
            </p>
          </div>
        </div>

        <div data-reveal style={{ "--i": 4 } as React.CSSProperties} className="mt-10 md:mt-16">
          <MasterplanViewer model={model} poster={assets.masterplan} />
        </div>
      </Shell>
    </InView>
  );
}
