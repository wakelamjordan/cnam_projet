/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*", // L'URL de ton API Flask
      },
    ];
  },
  output: "export",
};

export default nextConfig;
