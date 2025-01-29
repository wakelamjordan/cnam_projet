import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "cnam_projet",
  description: "site administrable afin de mettre en ligne des publications",
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        data-theme={"cupcake"}
      >
        <div className="grid grid-rows-[200px_100vh_250px] items-center justify-items-center min-h-screen p-8s gap-3 sm:p-5 md:px-20 font-[family-name:var(--font-geist-sans)]">
          <header className="bg-black row-start-1 w-full h-full">sss</header>
          {children}
          <footer className="bg-black row-start-3 w-full h-full">sss</footer>
        </div>
      </body>
    </html>
  );
}
