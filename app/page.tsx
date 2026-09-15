import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { Positioning } from "@/components/Positioning";
import { Documentation } from "@/components/Documentation";
import { FeatureStory } from "@/components/FeatureStory";
import { Location } from "@/components/Location";
import { Landmarks } from "@/components/Landmarks";
import { Facilities } from "@/components/Facilities";
import { Gallery } from "@/components/Gallery";
import { InvestmentBenefits } from "@/components/InvestmentBenefits";
import { GrowthCorridor } from "@/components/GrowthCorridor";
import { CommunityVision } from "@/components/CommunityVision";
import { Masterplan } from "@/components/Masterplan";
import { PlotPricing } from "@/components/PlotPricing";
import { PurchaseProcess } from "@/components/PurchaseProcess";
import { PaymentDetails } from "@/components/PaymentDetails";
import { ContactCTA } from "@/components/ContactCTA";
import { Footer } from "@/components/Footer";

/**
 * Section order is the master prompt's order and is not to be changed.
 * Backgrounds alternate paper → paper-warm → ink so no two adjacent sections
 * share a field: that alternation is what stops the page reading as one
 * endless scroll.
 */
export default function Home() {
  return (
    <>
      <Header />
      <main id="main-content">
        <Hero />
        <Positioning />
        <Documentation />
        <FeatureStory />
        <Location />
        <Landmarks />
        <Facilities />
        <Gallery />
        <InvestmentBenefits />
        <GrowthCorridor />
        <CommunityVision />
        <Masterplan />
        <PlotPricing />
        <PurchaseProcess />
        <ContactCTA />
        <PaymentDetails />
      </main>
      <Footer />
    </>
  );
}
