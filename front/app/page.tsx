import { CarouselDemo } from "@/components/Carousel";
import Footer from "@/components/Footer";

import { Calendar } from "@/components/Calendar";
import Table from "@/components/Table";
import Image from "next/image";
import bandeau from "../public/img/bandeau.jpg";
import left from "../public/img/pussay_logo.png";
import right from "../public/img/territoire-engage-nature.png";
import Navbar from "@/components/Navbar";
import Card from "@/components/Card";

// import Example from "@/components/test";

const navigation = [
  {
    name: "catégorie1",
    href: "#",
    current: false,
    children: [
      { name: "article1", href: "#", current: false },
      { name: "article2", href: "#", current: false },
      { name: "article3", href: "#", current: false },
      { name: "article4", href: "#", current: false },
    ],
  },
  {
    name: "catégorie2",
    href: "#",
    current: false,
    children: [
      { name: "article1", href: "#", current: false },
      { name: "article2", href: "#", current: false },
      { name: "article3", href: "#", current: false },
      { name: "article4", href: "#", current: false },
    ],
  },
  {
    name: "catégorie3",
    href: "#",
    current: false,
    children: [
      { name: "article1", href: "#", current: false },
      { name: "article2", href: "#", current: false },
      { name: "article3", href: "#", current: false },
      { name: "article4", href: "#", current: false },
    ],
  },
  {
    name: "catégorie4",
    href: "#",
    current: false,
    children: [
      { name: "article1", href: "#", current: false },
      { name: "article2", href: "#", current: false },
      { name: "article3", href: "#", current: false },
      { name: "article4", href: "#", current: false },
    ],
  },
];

export default function Home() {
  return (
    <div className="grid grid-rows-[auto_1fr_auto] items-center justify-items-center min-h-screen md:p-8 pb-20 gap-5 font-[family-name:var(--font-geist-sans)]">
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
          <Navbar navigation={navigation}/>
        </div>
      </div>
      <main className=" min-h-screen w-full row-start-2 grid grid-rows-[auto_1fr]">
        <CarouselDemo className="row-start-1" />
        <div className="p-5">
          <h1 className="text-2xl my-3">Site de la mairie</h1>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatum
            itaque id reprehenderit facere tempora qui harum deleniti
            laudantium! Magnam voluptatibus omnis, earum modi voluptates ducimus
            dignissimos debitis eum expedita nulla. Eum dolorem minus aperiam
            nam consectetur eveniet laudantium saepe, officiis soluta
            voluptatibus modi distinctio suscipit ab libero doloribus hic dolor
            quia vero! Est, debitis perferendis placeat animi ducimus modi eum?
          </p>
        </div>
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

      <Footer navigation={navigation}/>
    </div>
  );
}
