import type { Estate } from "@/content/estates";

/** "Balogun, Oyo — Off Iseyin Express" */
export const locationLine = (estate: Estate) => `${estate.area} — ${estate.road}`;

/** Cheapest plot, or null when the estate has no published prices. */
export function entryPrice(estate: Estate) {
  if (estate.plots.length === 0) return null;
  return estate.plots.reduce((low, plot) => (plot.price < low.price ? plot : low), estate.plots[0]);
}

/** "300 / 450 / 600" — sizes only, no invented ranges. */
export function plotSizes(estate: Estate) {
  return estate.plots
    .filter((plot) => /^\d/.test(plot.size))
    .map((plot) => plot.size.replace(/sqm$/i, ""))
    .join(" / ");
}

export const whatsappHref = (estate: Estate) =>
  estate.contact.whatsappPrimary ? `https://wa.me/${estate.contact.whatsappPrimary}` : null;

/** WhatsApp deep link with a prefilled first message naming the branch. */
export function whatsappAbout(estate: Estate, subject: string): string | null {
  if (!estate.contact.whatsappPrimary) return null;
  const message = `Hello ${estate.developer.name}, I'd like to know more about ${subject} at ${estate.name}, ${estate.area}.`;
  return `https://wa.me/${estate.contact.whatsappPrimary}?text=${encodeURIComponent(message)}`;
}

/**
 * Numbers are stored in local form (07034680780). tel: links need the
 * international form or they fail on desktop and on foreign SIMs.
 */
export function telHref(phone: string): string {
  const digits = phone.replace(/\D/g, "");
  return `tel:+234${digits.replace(/^0/, "")}`;
}

export function telDisplay(phone: string): string {
  const digits = phone.replace(/\D/g, "");
  return `${digits.slice(0, 4)} ${digits.slice(4, 7)} ${digits.slice(7)}`.trim();
}
