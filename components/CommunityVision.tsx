import { communityVision } from "@/content/orange-county";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

const leadLines = communityVision.lead.split("\n").map((line) => line.trim()).filter(Boolean);

export function CommunityVision() {
  return (
    <InView as="section" id="vision" aria-label="Community vision" className="bg-oc-paper-warm py-sec-lg text-oc-ink" amount={0.12}>
      <Shell>
        <div className="grid grid-cols-1 gap-10 md:grid-cols-12 md:gap-12">
          <div className="md:col-span-6">
            <Eyebrow>The Vision</Eyebrow>
            <Heading lines={leadLines} size="h1" offset={1} className="mt-6 max-w-[18ch] leading-[1.0]" />
          </div>

          <ol className="md:col-span-6 md:col-start-7 md:self-end">
            {communityVision.points.map((point, index) => (
              <li key={point} className="border-t border-oc-line py-5 last:border-b md:py-6">
                <div className="flex items-baseline gap-5">
                  <span data-reveal style={{ "--i": index } as React.CSSProperties} className="font-mono text-[0.6875rem] tracking-[0.16em] text-oc-orange">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span className="mask flex-1" style={{ "--i": index + 1 } as React.CSSProperties}>
                    <span className="block font-serif text-h2 leading-[1.1]">{point}</span>
                  </span>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </Shell>
    </InView>
  );
}
