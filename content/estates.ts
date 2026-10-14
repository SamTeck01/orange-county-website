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
  benefits: oyoContent.benefits,
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
  positioning: {
    tagline: "Lagos called. We answered.",
    body: "A premium land ownership opportunity in Epe.",
  },
  documentation: [],
  landTitle: [],
  features: [],
  landmarks: [],
  facilities: [],
  benefits: [],
  communityVision: null,
  plots: [],
  payment: null,
  contact: oyoContent.contact,
  developer: oyoContent.developer,
  media: {
    hero: unplaced(assets.hero),
    heroVideo: unplaced(assets.heroVideo),
    positioning: unplaced(assets.positioning),
    features: [],
    locationMap: null,
    landmarkImages: [],
    facilities: [],
    gallery: assets.gallery.filter((shot) => !/masterplan/.test(shot.src ?? "")).map(unplaced),
    film: unplaced(assets.film),
    masterplan: null,
    purchaseBg: unplaced(assets.purchaseBg),
    footerBg: unplaced(assets.footerBg),
  },
};

export const estates = [oyo, epe] as const;
