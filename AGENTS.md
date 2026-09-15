# Orange County — Standing Law

Re-read this file at the start of every session. It overrides your defaults.

## 1. NEVER INVENT FACTS
Every fact on this site comes from content/orange-county.ts. If a field is null,
render the DESIGNED EMPTY STATE for that component. Do not write placeholder copy,
lorem ipsum, invented distances, invented amenities, invented testimonials, invented
statistics, or invented dates. A missing fact is a design problem, not a writing problem.

## 2. LEGAL PRECISION
The documentation status is "C of O in View" — this means the certificate has NOT been
issued. Render this phrase verbatim. Never render "C of O", "Certificate of Occupancy
issued", "titled", or any phrasing that implies the certificate exists.
"Registered Survey Plan" renders verbatim.

## 3. PROTECTED FILES — STOP, DO NOT EDIT
- content/orange-county.ts
- content/assets.ts
- AGENTS.md
If a task seems to require changing these, STOP and report what you need and why.
Components read from these files; they never hardcode copy or media paths.

## 4. STRUCTURAL RULE
Cards are permitted in EXACTLY TWO places: the Facilities section and the Plot Pricing
section. Everywhere else uses full-bleed, split, overlap, or editorial composition.
Do not turn a section into a card grid because it is convenient.

## 5. MOBILE IS PRIMARY
Design and verify mobile first. Use 100svh, never 100vh. Every interactive target is
>= 44px. Test at 360px width before anything else.

## 6. MOTION
No scroll-jacking. No scroll libraries (no Locomotive, no GSAP ScrollTrigger, no Lenis).
Scroll-driven effects use IntersectionObserver + requestAnimationFrame writing CSS custom
properties. Never drive scroll animation through React state.
Every motion has a prefers-reduced-motion fallback that is a static, complete composition.

## 7. FORBIDDEN
Generic hero-with-centered-text. Bootstrap-looking cards. Stock-photo gradients over text
for legibility rescue. Emoji as icons. Fake urgency ("only 3 plots left"). Autoplaying
audio. Carousels driven by drag libraries. Any dependency not already in package.json
without asking first.

## 8. BRAND
Orange County is the estate. Pace Consult is the developer. The estate's colours are
--oc-orange and --oc-green. Pace's corporate colours are NOT site colours.
