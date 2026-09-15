import Image from "next/image";
import { contact, developer, payment } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { blurFor } from "@/lib/media";
import { telHref, whatsappAbout } from "@/lib/site";
import { Action, Eyebrow, Heading, InView, Shell } from "@/components/primitives";

/* Typed null in content today; typed loosely here so that the day the client
   sends the real steps, dropping them into content is the only change needed. */
const steps = payment.steps as readonly string[] | null;

export function PurchaseProcess() {
  const enquire = whatsappAbout("the purchase process");
  const phone = contact.phones[0];

  return (
    <InView as="section" id="process" aria-label="How to buy" className="relative isolate overflow-hidden bg-oc-ink-deep py-sec-lg text-oc-paper" amount={0.12}>
      {assets.purchaseBg.src ? (
        <Image
          src={assets.purchaseBg.src}
          alt=""
          fill
          loading="lazy"
          sizes="100vw"
          placeholder="blur"
          blurDataURL={blurFor(assets.purchaseBg.src)}
          className="-z-20 object-cover"
        />
      ) : null}
      <div aria-hidden="true" className="absolute inset-0 -z-10 bg-oc-ink-deep/78" />
      <div aria-hidden="true" className="card-noise absolute inset-0 -z-10 opacity-40" />

      <Shell>
        <Eyebrow>How to buy</Eyebrow>
        <Heading lines={["Buying is a", "conversation."]} size="h1" offset={1} className="mt-6 max-w-[16ch] text-oc-paper" />

        {steps && steps.length > 0 ? (
          <ol className="mt-12 grid grid-cols-1 gap-px border border-oc-paper/15 bg-oc-paper/15 sm:grid-cols-2 lg:grid-cols-4">
            {steps.map((step, index) => (
              <li key={step} data-reveal style={{ "--i": index } as React.CSSProperties} className="bg-oc-ink-deep/80 p-6">
                <span className="font-mono text-[0.6875rem] tracking-[0.16em] text-oc-orange">{String(index + 1).padStart(2, "0")}</span>
                <p className="mt-4 text-body leading-relaxed text-oc-paper/85">{step}</p>
              </li>
            ))}
          </ol>
        ) : (
          /* No documented steps exist yet, so we do not invent a four-step
             graphic. The honest version is a direct line to the team. */
          <p data-reveal style={{ "--i": 3 } as React.CSSProperties} className="mt-8 max-w-[44ch] text-lead leading-relaxed text-oc-paper/80">
            Reservation, payment and allocation are confirmed directly with the {developer.name} team.
          </p>
        )}

        <div data-reveal style={{ "--i": 4 } as React.CSSProperties} className="mt-10 flex flex-col gap-2.5 sm:flex-row">
          {enquire ? (
            <Action href={enquire} variant="primary" className="w-full sm:w-auto">
              Start on WhatsApp
            </Action>
          ) : null}
          {phone ? (
            <Action href={telHref(phone)} variant="ghost-dark" className="w-full sm:w-auto">
              Call the team
            </Action>
          ) : null}
        </div>
      </Shell>
    </InView>
  );
}
