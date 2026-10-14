import { epe } from "@/content/estates";
import { EstatePage, estateMetadata } from "@/components/EstatePage";

export const metadata = estateMetadata(epe);

export default function Page() {
  return <EstatePage estate={epe} />;
}
