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
  /** Shown beside the prices, e.g. "Pre-launch price". */
  pricingNote: string | null;
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
    /** Interactive 3D model of the estate (glTF binary) and the still shown before it loads. */
    model3d: { src: string; poster: MediaAsset } | null;
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
  pricingNote: null,
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
    model3d: null,
    purchaseBg: assets.purchaseBg,
    footerBg: assets.footerBg,
  },
};

export const epe: Estate = {
  slug: "epe",
  label: "Epe",
  name: "Orange County",
  area: "Epe, Lagos",
  road: "Off Epe / Ijebu Ode Expressway",
  // From the Epe launch flyers and the Epe product paper.
  positioning: {
    tagline: "Lagos called. We answered.",
    body: "A well planned estate designed for comfortable living and smart investment.",
  },
  // Papers as Oyo's. The Epe product paper lists the title as the Registered
  // Survey Plan only — it does not carry "C of O in View".
  documentation: oyoContent.documentation.items,
  landTitle: ["Registered Survey Plan"],
  features: oyoContent.features,
  landmarks: [
    { title: "Lekki-Epe International Airport", body: "25 mins" },
    { title: "Yabatech Epe Campus", body: "15 mins" },
    { title: "St. Augustine", body: "20 mins" },
    { title: "LASUED Michael Otedola", body: "15 mins" },
  ],
  facilities: [
    { title: "Gym Center", body: null },
    { title: "Football Pitch", body: null },
    { title: "Mini Mart", body: null },
    { title: "Green Environment", body: null },
    { title: "Drainage System", body: null },
    { title: "Reliable Water Supply", body: null },
  ],
  benefits: oyo.benefits,
  corridor: {
    title: oyoContent.benefits[3].title,
    lead: "Strategically located in Epe, Lagos — an emerging location with strong growth potential and promising investment advantages.",
  },
  communityVision: oyoContent.communityVision,
  plots: [
    { size: "300sqm", price: 3000000, display: "₦3,000,000", availability: null },
    { size: "450sqm", price: 4000000, display: "₦4,000,000", availability: null },
    { size: "600sqm", price: 5500000, display: "₦5,500,000", availability: null },
  ],
  pricingNote: "Pre-launch price",
  // Same Zenith account as Oyo, per the Epe product paper.
  payment: oyoContent.payment,
  contact: oyoContent.contact,
  developer: oyoContent.developer,
  media: {
    // Epe's own 3D renders (public/images/epe-*.webp, 2560px WebP from the 4K masters).
    hero: { src: "/images/epe-gate-front.webp", alt: "3D render of the entrance gate at Orange County, Epe" },
    // The Oyo flythrough shows Oyo's gate, so Epe shows its own still until the Epe film is ready.
    heroVideo: { src: "/video/epe-hero-loop.mp4", poster: "/images/epe-hero-poster.jpg", label: "Flythrough of Orange County, Epe" },
    positioning: { src: "/images/epe-gate-angle.webp", alt: "3D render of the gate and gatehouse at Orange County, Epe" },
    features: [
      { src: "/images/epe-feature-road.webp", alt: "3D render of a paved road inside Orange County, Epe" },
      { src: "/images/epe-street-lights.webp", alt: "3D render of solar street lights along the entrance road at Orange County, Epe" },
      { src: "/images/epe-feature-cctv.webp", alt: "3D render of a CCTV camera on the gatehouse at Orange County, Epe" },
      { src: "/images/epe-gate-angle.webp", alt: "3D render of the gated entrance at Orange County, Epe" },
    ],
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
    // Epe renders matched to each amenity in order.
    facilities: [
      { src: "/images/epe-facility-gym.webp", alt: "3D render of the gym at Orange County, Epe" },
      { src: "/images/epe-facility-pitch.webp", alt: "3D render of the football pitch at Orange County, Epe" },
      { src: "/images/epe-gym-supermart.webp", alt: "3D render of the supermart at Orange County, Epe" },
      { src: "/images/epe-aerial-clean.webp", alt: "3D render of the estate and its green surroundings at Orange County, Epe" },
      { src: "/images/epe-facility-drainage.webp", alt: "3D render of a kerbed, drained road at Orange County, Epe" },
      { src: "/images/epe-west-aerial.webp", alt: "3D render of the plots at Orange County, Epe" },
    ],
    gallery: [
      { src: "/images/epe-estate-aerial.webp", alt: "3D render of Orange County, Epe, from the air" },
      { src: "/images/epe-gate-front.webp", alt: "3D render of the entrance gate at Orange County, Epe" },
      { src: "/images/epe-gate-angle.webp", alt: "3D render of the gate and gatehouse at Orange County, Epe" },
      { src: "/images/epe-entrance-drone.webp", alt: "3D render of the entrance at Orange County, Epe, from the air" },
      { src: "/images/epe-gym-supermart.webp", alt: "3D render of the gym and supermart at Orange County, Epe" },
      { src: "/images/epe-swimming-pool.webp", alt: "3D render of the swimming pool at Orange County, Epe" },
      { src: "/images/epe-pitch-pool.webp", alt: "3D render of the football pitch and pool at Orange County, Epe" },
      { src: "/images/epe-main-avenue.webp", alt: "3D render of the main avenue at Orange County, Epe" },
      { src: "/images/epe-avenue-drone.webp", alt: "3D render of the main avenue and plots at Orange County, Epe, from the air" },
      { src: "/images/epe-special-700.webp", alt: "3D render of the special 700 sqm plot at Orange County, Epe" },
      { src: "/images/epe-west-aerial.webp", alt: "3D render of Blocks G, H and I at Orange County, Epe" },
      { src: "/images/epe-front-aerial.webp", alt: "3D render of Orange County, Epe, from the expressway" },
      { src: "/images/epe-commercial-plots.webp", alt: "3D render of the commercial plots facing the expressway at Orange County, Epe" },
      { src: "/images/epe-feature-cctv.webp", alt: "3D render of CCTV on the gatehouse at Orange County, Epe" },
      { src: "/images/epe-street-lights.webp", alt: "3D render of solar street lights along the entrance road at Orange County, Epe" },
      { src: "/images/epe-gatehouse-lights.webp", alt: "3D render of the gatehouse, its CCTV and the street lights at Orange County, Epe" },
      { src: "/images/epe-dusk-aerial.webp", alt: "3D render of Orange County, Epe, from the air at dusk" },
    ],
    // Full-quality Epe film: 1080p, anti-flicker pass, original score.
    film: { src: "/video/epe-film-1080.mp4", poster: "/images/epe-film-poster.jpg", label: "Film of Orange County, Epe" },
    masterplan: { src: "/images/epe-estate-aerial.webp", alt: "3D render of the labelled masterplan at Orange County, Epe, showing Block A to Block I" },
    // Simplified web export of the render scene (no people, far trees or cars).
    model3d: {
      src: "/models/epe-estate.glb",
      poster: { src: "/images/epe-3d-poster.webp", alt: "3D render of Orange County, Epe, seen from the air" },
    },
    purchaseBg: { src: "/images/epe-dusk-aerial.webp", alt: "3D render of Orange County, Epe, from the air at dusk" },
    footerBg: { src: "/images/epe-aerial-clean.webp", alt: "3D render of Orange County, Epe, from the air" },
  },
};

export const estates = [oyo, epe] as const;
