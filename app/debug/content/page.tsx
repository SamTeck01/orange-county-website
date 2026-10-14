import { assets } from "@/content/assets";
import { estates } from "@/content/estates";

export default function ContentDebugPage() {
  return (
    <main className="min-h-svh bg-oc-paper px-4 py-8 font-sans text-oc-ink sm:px-8">
      <section className="mx-auto max-w-5xl border-y border-[var(--oc-line)] py-6">
        <pre className="whitespace-pre-wrap break-words font-mono text-xs leading-6">
          {JSON.stringify(estates, null, 2)}
        </pre>
      </section>
      <section className="mx-auto max-w-5xl border-b border-[var(--oc-line)] py-6">
        <pre className="whitespace-pre-wrap break-words font-mono text-xs leading-6">
          {JSON.stringify(assets, null, 2)}
        </pre>
      </section>
    </main>
  );
}
