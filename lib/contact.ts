import { contact } from "@/content/orange-county";

export function hasDirectContact(): boolean {
  return Boolean(contact.whatsappPrimary || contact.phones.length > 0);
}

export function primaryPhone(): string | null {
  return contact.phones[0] ?? null;
}
