import { TONE } from "@/lib/blur";

/** Neutral fallback for anything not in the generated tone map. */
export const BLUR_DATA_URL =
  "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='3'%3E%3Crect width='4' height='3' fill='%23c0d8c4'/%3E%3C/svg%3E";

/**
 * Build a 1px blur placeholder from an image's mean colour.
 * next/image blurs and scales this, so a flat tone reads as a soft
 * colour-matched fade-in — the same perceived effect as a JPEG LQIP
 * at a twentieth of the bytes.
 */
export function blurFor(src: string | null | undefined): string {
  if (!src) return BLUR_DATA_URL;
  const name = src.split("/").pop()?.replace(/\.(webp|jpg|jpeg|png|avif)$/i, "") ?? "";
  const tone = TONE[name];
  if (!tone) return BLUR_DATA_URL;
  return `data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='3'%3E%3Crect width='4' height='3' fill='%23${tone.slice(1)}'/%3E%3C/svg%3E`;
}
