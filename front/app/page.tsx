import { CarouselDemo } from "@/components/Carousel";
import Footer from "@/components/Footer";

import { Calendar } from "@/components/Calendar";
import Table from "@/components/Table";
import CardDemo from "@/components/Card";
import Image from "next/image";
import bandeau from "../public/img/bandeau.jpg";
import left from "../public/img/pussay_logo.png";
import right from "../public/img/territoire-engage-nature.png";
import Navbar from "@/components/Navbar";
import Card from "@/components/Card";

// import Example from "@/components/test";

export default function Home() {
  return (
    <div className="grid grid-rows-[auto_1fr_200px] items-center justify-items-center min-h-screen md:p-8 pb-20 gap-5 font-[family-name:var(--font-geist-sans)]">
      <div className="h-full w-full">
        <header className="w-full overflow-hidden grid grid-cols-6 items-center">
          <Image src={left} alt="hhhh" className="w-auto" />
          <Image
            src={bandeau}
            alt="hhhh"
            className="w-auto col-span-4 col-start-2"
          />
          <Image src={right} alt="hhhh" className="w-auto" />
        </header>
        <div className="flex justify-between">
          <Navbar />
        </div>
      </div>
      <main className=" min-h-screen w-full row-start-2 grid grid-rows-[auto_1fr]">
        <CarouselDemo className="row-start-1" />
        <div className="md:grid grid-cols-3 flex flex-col-reverse h-full">
          <section className="col-span-3 md:col-span-2 grid md:grid-cols-1 gap-2 p-2 overflow-auto max-h-full">
            <Card />
            <Card />
            <Card />
          </section>
          <section className="col-span-3 md:col-span-1  flex justify-centers flex-col items-center h-auto">
            <Calendar />
            <Table />
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}
