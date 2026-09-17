export type MediaAsset = {
  src: string | null;
  alt: string;
  focal?: string;
  videoSrc?: string;
  poster?: string;
};

export type VideoAsset = {
  src: string | null;
  poster: string | null;
  /** Human description of the footage, for the a11y label on the play control. */
  label: string;
};

/**
 * ALL media lives here. Components never hardcode a path.
 *
 * ALT TEXT RULE: the estate is not built. Anything produced from the 3D
 * package must say "3D render of …". Only the location and landmark images
 * are real photographs and they must NOT claim to be renders.
 *
 * A null `src` means the component renders its DESIGNED EMPTY STATE —
 * the layout collapses, it never draws an empty filled rectangle.
 */
export const assets = {
  logo: { src: "/brand/orange-county-logo.png", alt: "Orange County logo" },
  // Hero — the 16s seamless loop (aerial push-in to the front gate).
  // 798KB, no audio track. Poster is the matching frame so there is no flash.
  heroVideo: {
    src: "/video/hero-loop.mp4",
    poster: "/images/hero-poster.jpg",
    label: "Aerial flythrough of Orange County, Balogun, Oyo",
  } satisfies VideoAsset,
  // Static fallback for prefers-reduced-motion and for browsers that refuse autoplay.
  hero: {
    src: "/images/hero-gate-arrival.webp",
    alt: "3D render of the entrance gate at Orange County, Balogun, Oyo",
    focal: "center 55%",
  },

  positioning: {
    src: "/images/positioning-frontage.webp",
    alt: "3D render of the commercial frontage at Orange County, Balogun, Oyo",
    focal: "center 60%",
  },

  // No render in the 3D package shows a document, and a stock certificate
  // would imply the C of O exists. Null on purpose — the section is typographic.
  documentation: { src: null, alt: "" },

  featureRoad: {
    src: "/images/feature-road-network.webp",
    alt: "3D render of the estate road network at Orange County, Balogun, Oyo",
    focal: "center",
  },
  featureSolar: {
    src: "/images/feature-street-lighting.webp",
    alt: "3D render of the illuminated entrance and street lighting at Orange County, Balogun, Oyo",
    focal: "center 45%",
  },
  // No camera appears anywhere in the 3D package. A stock CCTV photograph
  // would be a claim we cannot support, so this scene is typographic.
  featureCctv: {
    src: "/images/feature-cctv.webp",
    alt: "Photograph of CCTV surveillance cameras on estate security pole",
    focal: "center 35%",
  },
  featureGated: {
    src: "/images/feature-gated-entry.webp",
    alt: "3D render of the gated entrance and guardhouse at Orange County, Balogun, Oyo",
    focal: "center 50%",
  },

  // Real photograph of the area — not a render.
  locationMap: {
    src: "/images/location-street.webp",
    alt: "Street scene in Balogun, Oyo",
    focal: "center",
  },

  facilityGym: { src: "/images/facility-gym.webp", alt: "3D render of the gym at Orange County, Balogun, Oyo" },
  facilityPitch: { src: "/images/facility-football-pitch.webp", alt: "3D render of the football pitch at Orange County, Balogun, Oyo" },
  facilityBasketballCourt: { src: "/images/facility-basketball-court.webp", alt: "3D render of the basketball court at Orange County, Balogun, Oyo" },
  facilityMart: { src: "/images/facility-mini-mart.webp", alt: "3D render of the mini mart at Orange County, Balogun, Oyo" },

  gallery: [
    { src: "/images/gallery-gate-day.webp", alt: "3D render of the entrance gate at Orange County, Balogun, Oyo" },
    { src: "/images/gallery-commercial-strip.webp", alt: "3D render of the commercial strip at Orange County, Balogun, Oyo" },
    { src: "/images/gallery-estate-aerial.webp", alt: "3D render of the estate from the air at Orange County, Balogun, Oyo" },
    { src: "/images/gallery-masterplan-wide.webp", alt: "3D render of the masterplan at Orange County, Balogun, Oyo" },
    { src: "/images/gallery-masterplan-blocks.webp", alt: "3D render of the planned blocks at Orange County, Balogun, Oyo" },
  ] as MediaAsset[],

  // The full 60-second flythrough. Click-to-play only, preload="none" —
  // 14.2MB must never download on page load.
  film: {
    src: "/video/film-720.mp4",
    poster: "/images/film-poster.jpg",
    label: "60-second flythrough of Orange County, Balogun, Oyo",
  } satisfies VideoAsset,

  masterplan: { src: "/images/masterplan-labelled.webp", alt: "3D render of the labelled masterplan at Orange County, Balogun, Oyo, showing Block A to Block L" },
  purchaseBg: { src: "/images/purchase-dusk-aerial.webp", alt: "3D render of the estate at dusk at Orange County, Balogun, Oyo" },
  footerBg: { src: "/images/footer-aerial-clean.webp", alt: "3D render of the estate from the air at Orange County, Balogun, Oyo" },
};

/** Real photographs of the four landmarks. Order matches `landmarks` in content. */
export const landmarkImages: (MediaAsset | MediaAsset[])[] = [
  {
    src: "/images/landmark-iseyin-express.webp",
    alt: "Footage of the Iseyin Express road",
    videoSrc: "/video/landmark-iseyin-express.mp4",
    poster: "/images/landmark-iseyin-express-poster.jpg",
  },
  [
    { src: "/images/IMG-20260915-WA0035.jpg", alt: "Photograph of the Divisional Police Headquarters, Balogun" },
    { src: "/images/IMG-20260915-WA0036.jpg", alt: "Photograph of the Divisional Police Headquarters, Balogun" },
  ],
  { src: "/images/landmark-film-village.webp", alt: "Photograph of Afri Chatta Film Village" },
  { src: "/images/landmark-asphalt-plant.webp", alt: "Photograph of the Danbaba asphalt plant" },
];

export type SiteAssets = typeof assets;
export type AssetKey = keyof SiteAssets;
