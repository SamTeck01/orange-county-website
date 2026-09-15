import { contact, developer, documentation, location, plots, positioning } from "@/content/orange-county";

/**
 * The estate name is derived from the one place it is stated in content,
 * rather than retyped in six components.
 * "Orange County is an avant-garde residential estate…" → "Orange County"
 */
export const estateName = positioning.body.slice(0, positioning.body.indexOf(" is "));

/** Cheapest plot, formatted. Never hardcode a price. */
export const entryPrice = plots.reduce((low, plot) => (plot.price < low.price ? plot : low), plots[0]);

/** "300 / 450 / 600" — sizes only, no invented ranges. */
export const plotSizes = plots
  .filter((plot) => /^\d/.test(plot.size))
  .map((plot) => plot.size.replace(/sqm$/i, ""))
  .join(" / ");

export const titleStatus = documentation.items[0];
export const surveyStatus = documentation.items[1];

export const whatsappHref = contact.whatsappPrimary
  ? `https://wa.me/${contact.whatsappPrimary}`
  : null;

/** WhatsApp deep link with a prefilled first message. */
export function whatsappAbout(subject: string): string | null {
  if (!contact.whatsappPrimary) return null;
  const message = `Hello ${developer.name}, I'd like to know more about ${subject} at ${estateName}.`;
  return `https://wa.me/${contact.whatsappPrimary}?text=${encodeURIComponent(message)}`;
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

export const locationLine = `${location.area.replace(/\.$/, "")} — ${location.road}`;
