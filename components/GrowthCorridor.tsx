import { benefits } from "@/content/orange-county";
import { Eyebrow, InView, Rule, Shell } from "@/components/primitives";

/* The growth-corridor benefit, rendered once, here, as a typographic
   interstitial. It is deliberately excluded from InvestmentBenefits. */
const corridor = benefits[3];

export function GrowthCorridor() {
  if (!corridor?.lead) return null;

  return (
    <InView as="section" id="growth" aria-label={corridor.title} className="bg-oc-green-deep py-sec-lg text-oc-paper" amount={0.15}>
      <Shell>
        <Eyebrow tone="paper">{corridor.title}</Eyebrow>
        <Rule tone="paper" index={1} className="mt-6 max-w-32" />

        <p data-reveal style={{ "--i": 2 } as React.CSSProperties} className="mt-9 max-w-[24ch] font-serif text-h1 leading-[1.0] md:mt-12">
          {corridor.lead}
        </p>
      </Shell>
    </InView>
  );
}
