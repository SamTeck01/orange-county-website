import type { Metadata } from "next";
import "./globals.css";
import { oyo } from "@/content/estates";
import { ScrollEffects } from "@/components/ScrollEffects";
import { Analytics } from "@vercel/analytics/next";

const description = `Orange County residential estates by ${oyo.developer.name} — in Balogun, Oyo and Epe, Lagos.`;

export const metadata: Metadata = {
  metadataBase: process.env.NEXT_PUBLIC_SITE_URL ? new URL(process.env.NEXT_PUBLIC_SITE_URL) : undefined,
  title: { default: "Orange County — Oyo & Epe", template: "%s — Orange County" },
  description,
  applicationName: "Orange County",
  authors: [{ name: oyo.developer.name }],
  keywords: ["Orange County estate", "land for sale Oyo", "Balogun Oyo", "land for sale Epe", "Epe Lagos", oyo.developer.name, "residential plots Nigeria"],
  openGraph: {
    type: "website",
    title: "Orange County — Oyo & Epe",
    description,
    siteName: "Orange County",
    locale: "en_NG",
    images: oyo.media.heroVideo.poster ? [{ url: oyo.media.heroVideo.poster, width: 1600, height: 900, alt: oyo.media.hero.alt }] : undefined,
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
        <meta name="theme-color" content="#080d09" />
      </head>
      <body className="min-h-svh bg-oc-paper font-sans text-oc-ink antialiased">
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>
        <ScrollEffects />
        {children}
        <Analytics />
      </body>
    </html>
  );
}
