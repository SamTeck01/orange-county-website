import type { Metadata } from "next";
import type { Estate } from "@/content/estates";
import { entryPrice, locationLine, plotSizes } from "@/lib/site";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { Positioning } from "@/components/Positioning";
import { Documentation } from "@/components/Documentation";
import { FeatureStory } from "@/components/FeatureStory";
import { Location } from "@/components/Location";
import { Landmarks } from "@/components/Landmarks";
import { Facilities } from "@/components/Facilities";
import { Gallery } from "@/components/Gallery";
import { Explore3D } from "@/components/Explore3D";
import { InvestmentBenefits } from "@/components/InvestmentBenefits";
import { GrowthCorridor } from "@/components/GrowthCorridor";
import { CommunityVision } from "@/components/CommunityVision";
import { Masterplan } from "@/components/Masterplan";
import { PlotPricing } from "@/components/PlotPricing";
import { PurchaseProcess } from "@/components/PurchaseProcess";
import { PaymentDetails } from "@/components/PaymentDetails";
import { ContactCTA } from "@/components/ContactCTA";
import { Footer } from "@/components/Footer";
import { StickyMobileCTA } from "@/components/StickyMobileCTA";

export function estateMetadata(estate: Estate): Metadata {
  const title = `${estate.name} ${estate.label} — ${locationLine(estate)}`;
  const price = entryPrice(estate);
  const sizes = plotSizes(estate);
  const description = [
    `${estate.name} is a residential estate in ${locationLine(estate)} by ${estate.developer.name}.`,
    price ? `Plots${sizes ? ` of ${sizes} sqm` : ""} from ${price.display}.` : estate.positioning.body,
  ].join(" ");
  const poster = estate.media.heroVideo.poster;
  return {
    title: { absolute: title },
    description,
    openGraph: {
      type: "website",
      title,
      description,
      siteName: estate.name,
      locale: "en_NG",
      images: poster ? [{ url: poster, width: 1600, height: 900, alt: estate.media.hero.alt }] : undefined,
    },
    twitter: { card: "summary_large_image", title, description },
  };
}

/**
 * One page template for every branch. Each section returns null when the
 * estate has nothing for it, so the order below never changes.
 */
export function EstatePage({ estate }: { estate: Estate }) {
  return (
    <>
      <Header estate={estate} />
      <main id="main-content">
        <Hero estate={estate} />
        <Positioning estate={estate} />
        <Documentation estate={estate} />
        <FeatureStory estate={estate} />
        <Location estate={estate} />
        <Landmarks estate={estate} />
        <Facilities estate={estate} />
        <Gallery estate={estate} />
        <Explore3D estate={estate} />
        <InvestmentBenefits estate={estate} />
        <GrowthCorridor estate={estate} />
        <CommunityVision estate={estate} />
        <Masterplan estate={estate} />
        <PlotPricing estate={estate} />
        <PurchaseProcess estate={estate} />
        <ContactCTA estate={estate} />
        <PaymentDetails estate={estate} />
      </main>
      <Footer estate={estate} />
      <StickyMobileCTA estate={estate} />
    </>
  );
}
