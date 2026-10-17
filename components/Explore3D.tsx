import type { Estate } from "@/content/estates";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";
import { EstateModelViewer } from "@/components/EstateModelViewer";

export function Explore3D({ estate }: { estate: Estate }) {
  const model = estate.media.model3d;
  if (!model) return null;

  return (
    <InView as="section" id="explore-3d" aria-label="Explore the estate in 3D" className="relative isolate overflow-hidden bg-oc-ink-deep py-sec text-oc-paper" amount={0.08}>
      <Shell>
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between md:gap-10">
          <Heading lines={["Walk the estate", "in 3D."]} size="h1" className="max-w-[14ch] text-oc-paper" />
          <div className="md:pb-3 md:text-right">
            <Eyebrow index={2}>Interactive model</Eyebrow>
          </div>
        </div>

        <div data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-10 md:mt-16">
          <EstateModelViewer src={model.src} poster={model.poster} />
        </div>
      </Shell>
    </InView>
  );
}
