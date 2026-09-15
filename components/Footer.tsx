import Image from "next/image";
import { contact, developer } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { estateName, locationLine, telDisplay, telHref } from "@/lib/site";
import { Shell } from "@/components/primitives";

const columns = [
  {
    heading: "Estate",
    links: [
      { label: "The estate", href: "#positioning" },
      { label: "Documentation", href: "#documentation" },
      { label: "Features", href: "#features" },
      { label: "Facilities", href: "#facilities" },
    ],
  },
  {
    heading: "Buying",
    links: [
      { label: "Plot pricing", href: "#pricing" },
      { label: "How to buy", href: "#process" },
      { label: "Payment details", href: "#payment" },
      { label: "Masterplan", href: "#masterplan" },
    ],
  },
];

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="relative isolate overflow-hidden bg-oc-ink-deep pt-sec text-oc-paper">
      {assets.footerBg.src ? (
        <Image src={assets.footerBg.src} alt="" fill loading="lazy" sizes="100vw" placeholder="blur" blurDataURL={blurFor(assets.footerBg.src)} className="-z-20 object-cover" />
      ) : null}
      <div aria-hidden="true" className="absolute inset-0 -z-10 bg-gradient-to-b from-oc-ink-deep/92 via-oc-ink-deep/88 to-oc-ink-deep" />

      <Shell>
        <div className="grid grid-cols-1 gap-10 pb-14 md:grid-cols-12 md:gap-10 md:pb-20">
          <div className="md:col-span-5">
            <p className="font-serif text-h1 leading-[0.95]">{estateName}</p>
            <p className="mt-4 font-mono text-[0.625rem] uppercase leading-relaxed tracking-[0.16em] text-oc-paper/55">{locationLine}</p>
          </div>

          {columns.map((column) => (
            <nav key={column.heading} aria-label={column.heading} className="md:col-span-2">
              <p className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-orange">{column.heading}</p>
              <ul className="mt-4 flex flex-col">
                {column.links.map((link) => (
                  <li key={link.href}>
                    <a href={link.href} className="inline-flex min-h-11 items-center text-small text-oc-paper/70 transition-colors duration-300 hover:text-oc-paper">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          ))}

          <div className="md:col-span-3">
            <p className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-orange">Contact</p>
            <ul className="mt-4 flex flex-col">
              {contact.phones.map((phone) => (
                <li key={phone}>
                  <a href={telHref(phone)} rel="noopener noreferrer" className="inline-flex min-h-11 items-center font-mono text-small text-oc-paper/70 transition-colors duration-300 hover:text-oc-paper">
                    {telDisplay(phone)}
                  </a>
                </li>
              ))}
              {contact.email ? (
                <li>
                  <a href={`mailto:${contact.email}`} rel="noopener noreferrer" className="inline-flex min-h-11 items-center break-all font-mono text-small text-oc-paper/70 transition-colors duration-300 hover:text-oc-paper">
                    {contact.email}
                  </a>
                </li>
              ) : null}
              {contact.instagram ? (
                <li>
                  <a href={contact.instagramUrl} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center font-mono text-small text-oc-paper/70 transition-colors duration-300 hover:text-oc-paper">
                    {contact.instagram}
                  </a>
                </li>
              ) : null}
            </ul>
          </div>
        </div>

        <div className="flex flex-col gap-3 border-t border-oc-paper/15 py-7 font-mono text-[0.625rem] uppercase tracking-[0.14em] text-oc-paper/45 sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {year} {developer.name}
          </p>
          <p>All renders are for illustration</p>
        </div>
      </Shell>
    </footer>
  );
}
