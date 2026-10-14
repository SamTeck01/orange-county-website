import { oyo } from "@/content/estates";
import { EstatePage, estateMetadata } from "@/components/EstatePage";

export const metadata = estateMetadata(oyo);

export default function Page() {
  return <EstatePage estate={oyo} />;
}
