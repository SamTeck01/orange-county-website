import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  agentRules: false,
  images: {
    formats: ["image/avif", "image/webp"],
    // 75 (the default) left the renders soft; one higher step keeps them crisp at a small cost
    qualities: [88],
  },
};

export default nextConfig;
