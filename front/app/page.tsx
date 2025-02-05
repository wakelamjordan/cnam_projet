import { CarouselDemo } from "@/components/Carousel";
import { Calendar } from "@/components/Calendar";
import Table from "@/components/Table";
import Card from "@/components/Card";


export default function Home() {
  return (
    <main className=" min-h-screen w-full row-start-2 grid grid-rows-[auto_1fr]">
      <CarouselDemo className="row-start-1" />
      <div className="p-5">
        <h1 className="text-2xl my-3">Site de la mairie</h1>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatum
          itaque id reprehenderit facere tempora qui harum deleniti laudantium!
          Magnam voluptatibus omnis, earum modi voluptates ducimus dignissimos
          debitis eum expedita nulla. Eum dolorem minus aperiam nam consectetur
          eveniet laudantium saepe, officiis soluta voluptatibus modi distinctio
          suscipit ab libero doloribus hic dolor quia vero! Est, debitis
          perferendis placeat animi ducimus modi eum?
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
  );
}
