import { contact } from "@/content/orange-county";
import { telDisplay, telHref, whatsappAbout } from "@/lib/site";
import { Action, Eyebrow, Heading, InView, Shell } from "@/components/primitives";

export function ContactCTA() {
  const inspection = whatsappAbout("booking an inspection");

  return (
    <InView as="section" id="contact" aria-label="Contact" className="relative isolate overflow-hidden bg-oc-orange py-sec-lg text-oc-ink" amount={0.12}>
      <Shell>
        <div className="grid grid-cols-1 gap-12 md:grid-cols-12 md:gap-12">
          <div className="md:col-span-7">
            <Eyebrow tone="ink">Get in touch</Eyebrow>
            <Heading lines={["Come and see", "it for yourself."]} size="h1" offset={1} className="mt-6 max-w-[16ch] leading-[0.98]" />

            <div data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-10 flex flex-col gap-2.5 sm:flex-row">
              {inspection ? (
                <Action href={inspection} variant="ghost" className="w-full border-oc-ink/30 hover:border-oc-ink hover:bg-oc-ink/10 sm:w-auto">
                  Book an inspection
                </Action>
              ) : null}
              {contact.phones[0] ? (
                <Action href={telHref(contact.phones[0])} variant="ghost" className="w-full border-oc-ink/30 hover:border-oc-ink hover:bg-oc-ink/10 sm:w-auto">
                  Call now
                </Action>
              ) : null}
            </div>
          </div>

          <div className="md:col-span-5 md:col-start-8">
            <dl>
              <div data-reveal className="border-t border-oc-ink/20 py-5">
                <dt className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-ink/60">Phone</dt>
                <dd className="mt-3 flex flex-col gap-1">
                  {contact.phones.map((phone) => (
                    <a key={phone} href={telHref(phone)} rel="noopener noreferrer" className="inline-flex min-h-11 items-center font-mono text-[0.9375rem] tracking-[0.04em] underline decoration-oc-ink/25 underline-offset-4 transition-colors duration-300 hover:decoration-oc-ink">
                      {telDisplay(phone)}
                    </a>
                  ))}
                </dd>
              </div>

              {contact.email ? (
                <div data-reveal style={{ "--i": 1 } as React.CSSProperties} className="border-t border-oc-ink/20 py-5">
                  <dt className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-ink/60">Email</dt>
                  <dd className="mt-3">
                    <a href={`mailto:${contact.email}`} rel="noopener noreferrer" className="inline-flex min-h-11 items-center break-all font-mono text-[0.875rem] underline decoration-oc-ink/25 underline-offset-4 transition-colors duration-300 hover:decoration-oc-ink">
                      {contact.email}
                    </a>
                  </dd>
                </div>
              ) : null}

              {contact.instagram ? (
                <div data-reveal style={{ "--i": 2 } as React.CSSProperties} className="border-y border-oc-ink/20 py-5">
                  <dt className="font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-ink/60">Instagram</dt>
                  <dd className="mt-3">
                    <a
                      href={contact.instagramUrl}
                      rel="noopener noreferrer"
                      target="_blank"
                      className="inline-flex min-h-11 items-center font-mono text-[0.875rem] underline decoration-oc-ink/25 underline-offset-4 transition-colors duration-300 hover:decoration-oc-ink"
                    >
                      {contact.instagram}
                    </a>
                  </dd>
                </div>
              ) : null}
            </dl>
          </div>
        </div>
      </Shell>
    </InView>
  );
}
