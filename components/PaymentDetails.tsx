"use client";

import { useState } from "react";
import { payment } from "@/content/orange-county";
import { Eyebrow, Heading, InView, Shell } from "@/components/primitives";

function CopyButton({ value, label }: { value: string; label: string }) {
  const [copied, setCopied] = useState(false);

  return (
    <button
      type="button"
      aria-label={`Copy ${label}`}
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(value);
          setCopied(true);
          window.setTimeout(() => setCopied(false), 1800);
        } catch {
          /* Clipboard is unavailable over plain http and in some in-app
             browsers. The number is selectable text either way. */
        }
      }}
      className="inline-flex min-h-11 shrink-0 items-center gap-2 border border-oc-line px-4 font-mono text-[0.625rem] uppercase tracking-[0.12em] text-oc-ink transition-colors duration-300 hover:border-oc-ink/40"
    >
      {copied ? "Copied" : "Copy"}
    </button>
  );
}

export function PaymentDetails() {
  const rows: { label: string; value: string; copy?: boolean }[] = [
    { label: "Account name", value: payment.accountName },
    { label: "Bank", value: payment.bank },
    { label: "Account number", value: payment.accountNumber, copy: true },
  ];

  return (
    <InView as="section" id="payment" aria-label="Payment details" className="bg-oc-paper-warm py-sec text-oc-ink" amount={0.12}>
      <Shell>
        <div className="grid grid-cols-1 gap-9 md:grid-cols-12 md:gap-12">
          <div className="md:col-span-4">
            <Eyebrow>Payment</Eyebrow>
            <Heading lines={["Payment", "details."]} size="h2" offset={1} className="mt-5 leading-[1.05]" />
          </div>

          <dl className="md:col-span-8">
            {rows.map((row, index) => (
              <div key={row.label} data-reveal style={{ "--i": index } as React.CSSProperties} className="flex flex-wrap items-center gap-x-6 gap-y-3 border-t border-oc-line py-5 last:border-b">
                <dt className="w-full font-mono text-[0.625rem] uppercase tracking-[0.16em] text-oc-ink-soft sm:w-40">{row.label}</dt>
                <dd className="flex flex-1 flex-wrap items-center justify-between gap-4">
                  <span className={row.copy ? "select-all font-mono text-h3 tracking-[0.06em]" : "font-serif text-h3 leading-snug"}>{row.value}</span>
                  {row.copy ? <CopyButton value={row.value} label={row.label} /> : null}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </Shell>
    </InView>
  );
}
