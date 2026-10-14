import * as oyoContent from "@/content/orange-county";
import { assets, landmarkImages, type MediaAsset, type VideoAsset } from "@/content/assets";

/**
 * One shape for every estate. Each section reads from an Estate and renders
 * nothing when its fact is null or empty, so a branch with a short brief gets
 * a shorter page instead of invented copy.
 */
export type Plot = { size: string; price: number; display: string; availability: null };

export type Estate = {
  slug: "oyo" | "epe";
  /** Short label for the chooser and the switcher: "Oyo", "Epe". */
  label: string;
  name: string;
  /** "Balogun, Oyo" — no trailing full stop. */
  area: string;
  road: string;
  positioning: { tagline: string; body: string };
  documentation: string[];
  landTitle: string[];
  features: { n: string; title: string; body: string | null }[];
  landmarks: { title: string; body: string | null }[];
  facilities: { title: string; body: string | null }[];
  benefits: { title: string; lead: string | null; points: string[] }[];
  /** One benefit pulled out as a full-width statement (GrowthCorridor). */
  corridor: { title: string; lead: string } | null;
  communityVision: { lead: string; points: string[] } | null;
  plots: Plot[];
  payment: { accountName: string; bank: string; accountNumber: string; steps: readonly string[] | null } | null;
  contact: typeof oyoContent.contact;
  developer: { name: string };
  media: {
    hero: MediaAsset;
    heroVideo: VideoAsset;
    positioning: MediaAsset;
    features: MediaAsset[];
    locationMap: MediaAsset | null;
    landmarkImages: (MediaAsset | MediaAsset[])[];
    facilities: MediaAsset[];
    gallery: MediaAsset[];
    film: VideoAsset;
    masterplan: MediaAsset | null;
    purchaseBg: MediaAsset;
    footerBg: MediaAsset;
  };
};

export const oyo: Estate = {
  slug: "oyo",
  label: "Oyo",
  name: "Orange County",
  area: oyoContent.location.area.replace(/\.$/, ""),
  road: oyoContent.location.road,
  positioning: oyoContent.positioning,
  documentation: oyoContent.documentation.items,
  landTitle: oyoContent.landTitle.items,
  features: oyoContent.features,
  landmarks: oyoContent.landmarks,
  facilities: oyoContent.facilities,
  // benefits[3] (growth corridor) is shown once, as its own interstitial.
  benefits: oyoContent.benefits.filter((_, index) => index !== 3),
  corridor: oyoContent.benefits[3].lead ? { title: oyoContent.benefits[3].title, lead: oyoContent.benefits[3].lead } : null,
  communityVision: oyoContent.communityVision,
  plots: oyoContent.plots,
  payment: oyoContent.payment,
  contact: oyoContent.contact,
  developer: oyoContent.developer,
  media: {
    hero: assets.hero,
    heroVideo: assets.heroVideo,
    positioning: assets.positioning,
    features: [assets.featureRoad, assets.featureSolar, assets.featureCctv, assets.featureGated],
    locationMap: assets.locationMap,
    landmarkImages,
    facilities: [assets.facilityGym, assets.facilityPitch, assets.facilityBasketballCourt, assets.facilityMart],
    gallery: assets.gallery,
    film: assets.film,
    masterplan: assets.masterplan,
    purchaseBg: assets.purchaseBg,
    footerBg: assets.footerBg,
  },
};

/* Epe reuses the Oyo 3D renders and films (client instruction). Their alt text
   names Balogun, so it is restated without a place. Real photographs of Oyo
   (location street, landmarks) and the Oyo masterplan are NOT reused: they
   show a different site. */
const unplaced = <T extends { alt?: string; label?: string }>(asset: T): T => ({
  ...asset,
  ...(asset.alt !== undefined ? { alt: asset.alt.replace(/ at Orange County, Balogun, Oyo/, "") } : {}),
  ...(asset.label !== undefined ? { label: asset.label.replace(/ of Orange County, Balogun, Oyo/, "") } : {}),
});

export const epe: Estate = {
  slug: "epe",
  label: "Epe",
  name: "Orange County",
  area: "Epe, Lagos",
  road: "Off Epe / Ijebu Ode Expressway",
  // Everything below is from the Epe launch flyers.
  positioning: {
    tagline: "Lagos called. We answered.",
    body: "A well planned estate designed for comfortable living and smart investment.",
  },
  documentation: [],
  landTitle: [],
  // The four features that have a matching render lead the stack.
  features: [
    { n: "01", title: "Gated Estate", body: null },
    { n: "02", title: "CCTV Cameras", body: null },
    { n: "03", title: "Solar Street Lights", body: null },
    { n: "04", title: "Good Road Network", body: null },
  ],
  landmarks: [
    { title: "Lekki-Epe International Airport", body: "25 mins" },
    { title: "Yabatech Epe Campus", body: "15 mins" },
    { title: "St. Augustine", body: "20 mins" },
    { title: "LASUED Michael Otedola", body: "15 mins" },
  ],
  facilities: [
    { title: "Facility Centres", body: null },
    { title: "Recreational Spaces", body: null },
    { title: "Green Environment", body: null },
    { title: "Drainage System", body: null },
    { title: "Reliable Water Supply", body: null },
    { title: "Beautiful Layout", body: null },
  ],
  benefits: [
    { title: "Great Investment Potential", lead: null, points: [] },
    { title: "Ideal for Residential & Commercial Use", lead: null, points: ["Residential Plots", "Commercial Plots"] },
    { title: "Peaceful Environment", lead: null, points: [] },
    { title: "Secure & Accessible", lead: null, points: [] },
    { title: "Prime Location", lead: null, points: [] },
    { title: "High Growth Area", lead: null, points: [] },
  ],
  corridor: { title: "Easy Access. Greater Opportunities.", lead: "A new address in Epe. Strategically located off Epe/Ijebu Ode Expressway." },
  communityVision: { lead: "More than land.\nA community built for tomorrow.", points: [] },
  plots: [],
  payment: null,
  // The Epe flyers list only the first two numbers.
  contact: { ...oyoContent.contact, phones: oyoContent.contact.phones.slice(0, 2) },
  developer: oyoContent.developer,
  media: {
    hero: unplaced(assets.hero),
    heroVideo: unplaced(assets.heroVideo),
    positioning: unplaced(assets.positioning),
    features: [assets.featureGated, assets.featureCctv, assets.featureSolar, assets.featureRoad].map(unplaced),
    locationMap: null,
    // Real photographs from Wikimedia Commons, all CC0 (public domain).
    landmarkImages: [
      // Client-supplied stand-in: the airport is under construction, so this is
      // labelled illustrative on the page rather than presented as the site.
      { src: "/images/epe-landmark-airport.webp", alt: "Illustrative image of an airport terminal", caption: "Illustrative image" },
      { src: "/images/epe-landmark-yabatech.jpg", alt: "Photograph of Yaba College of Technology, Epe Campus" },
      { src: "/images/epe-landmark-augustine.jpg", alt: "Photograph of the entrance of Augustine University, Ilara-Epe" },
      { src: "/images/epe-landmark-lasued.jpg", alt: "Photograph of Lagos State University of Education, Epe Campus" },
    ],
    facilities: [],
    gallery: assets.gallery.filter((shot) => !/masterplan/.test(shot.src ?? "")).map(unplaced),
    film: unplaced(assets.film),
    masterplan: null,
    purchaseBg: unplaced(assets.purchaseBg),
    footerBg: unplaced(assets.footerBg),
  },
};

export const estates = [oyo, epe] as const;
