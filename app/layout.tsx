import type { Metadata } from "next";
import "./globals.css";
import { developer } from "@/content/orange-county";
import { assets } from "@/content/assets";
import { entryPrice, estateName, locationLine, plotSizes } from "@/lib/site";
import { StickyMobileCTA } from "@/components/StickyMobileCTA";
import { ScrollEffects } from "@/components/ScrollEffects";

const description = `${estateName} is a residential estate in ${locationLine} by ${developer.name}. Plots of ${plotSizes} sqm from ${entryPrice.display}.`;

export const metadata: Metadata = {
  metadataBase: process.env.NEXT_PUBLIC_SITE_URL ? new URL(process.env.NEXT_PUBLIC_SITE_URL) : undefined,
  title: {
    default: `${estateName} — ${locationLine}`,
    template: `%s — ${estateName}`,
  },
  description,
  applicationName: estateName,
  authors: [{ name: developer.name }],
  keywords: ["Orange County estate", "land for sale Oyo", "Balogun Oyo", developer.name, "residential plots Nigeria"],
  openGraph: {
    type: "website",
    title: `${estateName} — ${locationLine}`,
    description,
    siteName: estateName,
    locale: "en_NG",
    images: assets.heroVideo.poster ? [{ url: assets.heroVideo.poster, width: 1600, height: 900, alt: assets.hero.alt }] : undefined,
  },
  twitter: {
    card: "summary_large_image",
    title: `${estateName} — ${locationLine}`,
    description,
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
        <StickyMobileCTA />
      </body>
    </html>
  );
}
