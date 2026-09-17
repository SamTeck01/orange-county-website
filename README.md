# Orange County

Marketing site for Orange County, a residential estate in Balogun, Oyo, developed by Pace Consult.

## Where Things Live

- content/orange-county.ts and content/assets.ts: every fact and media path. PROTECTED.
- lib/site.ts: values derived from content (entry price, plot sizes, tel and WhatsApp links).
- lib/blur.ts: generated mean-colour map behind the next/image blur placeholders.
- components/: one file per section, composed in order by app/page.tsx.
- app/globals.css: design tokens, type scale and the single reveal mechanic.

app/debug/content dumps the content tree as JSON. Development aid only; remove before launch.

Rules that are not negotiable, and the reason for each, are in AGENTS.md.
