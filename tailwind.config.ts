import type { Config } from "tailwindcss";

// Colour keys are declared in BOTH kebab and camel form on purpose.
// Tailwind generates class names from the literal key, so `paperWarm` alone
// silently produced no `bg-oc-paper-warm` class and three sections shipped
// with no background at all. Declaring both makes either spelling valid.
const palette = {
  orange: "var(--oc-orange)",
  "orange-deep": "var(--oc-orange-deep)",
  orangeDeep: "var(--oc-orange-deep)",
  "orange-tint": "var(--oc-orange-tint)",
  orangeTint: "var(--oc-orange-tint)",
  green: "var(--oc-green)",
  "green-deep": "var(--oc-green-deep)",
  greenDeep: "var(--oc-green-deep)",
  "green-tint": "var(--oc-green-tint)",
  greenTint: "var(--oc-green-tint)",
  paper: "var(--oc-paper)",
  "paper-warm": "var(--oc-paper-warm)",
  paperWarm: "var(--oc-paper-warm)",
  ink: "var(--oc-ink)",
  "ink-soft": "var(--oc-ink-soft)",
  inkSoft: "var(--oc-ink-soft)",
  "ink-deep": "var(--oc-ink-deep)",
  inkDeep: "var(--oc-ink-deep)",
  line: "var(--oc-line)",
};

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: { oc: palette },
      fontFamily: {
        serif: ["Instrument Serif", "Georgia", "serif"],
        sans: ["Plus Jakarta Sans", "Arial", "sans-serif"],
        mono: ["JetBrains Mono", "Consolas", "monospace"],
      },
      // One fluid type scale for the whole site. Sections must use these,
      // never a fresh clamp() invented at the call site.
      fontSize: {
        display: ["var(--t-display)", { lineHeight: "0.86", letterSpacing: "-0.03em" }],
        h1: ["var(--t-h1)", { lineHeight: "0.92", letterSpacing: "-0.025em" }],
        h2: ["var(--t-h2)", { lineHeight: "1.0", letterSpacing: "-0.02em" }],
        h3: ["var(--t-h3)", { lineHeight: "1.1", letterSpacing: "-0.01em" }],
        lead: ["var(--t-lead)", { lineHeight: "1.55" }],
        body: ["var(--t-body)", { lineHeight: "1.7" }],
        small: ["var(--t-small)", { lineHeight: "1.6" }],
      },
      spacing: {
        gut: "var(--pad-x)",
        sec: "var(--sec-y)",
        "sec-lg": "var(--sec-y-lg)",
      },
      maxWidth: { shell: "var(--shell)" },
      transitionTimingFunction: { out: "cubic-bezier(0.16, 1, 0.3, 1)" },
    },
  },
  plugins: [],
};

export default config;
