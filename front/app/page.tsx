import { CarouselDemo } from "@/components/Carousel";
import Footer from "@/components/Footer";
import { NavigationMenuDemo } from "@/components/Navbar";
import { InputWithButton } from "@/components/Input";
import { CalendarDemo } from "@/components/Calendar";
import Table from "@/components/Table";
import  CardDemo from "@/components/Card";

export default function Home() {
  return (
    <div className="grid grid-rows-[250px_1fr_200px] items-center justify-items-center min-h-screen md:p-8 pb-20 gap-5 font-[family-name:var(--font-geist-sans)]">
      <div className="h-full w-full py-5">
        <header className="bg-red-400 h-full w-full"></header>
        <div className="flex justify-between ">
          <NavigationMenuDemo />
          <InputWithButton />
        </div>
      </div>
      <main className="bg-gray-700 min-h-screen w-full row-start-2 grid grid-rows-[auto_1fr]">
        <CarouselDemo className="row-start-1" />
        <div className="md:grid grid-cols-3 flex flex-col-reverse">
          <section className="col-span-3 md:col-span-2 bg-amber-300 h-full grid md:grid-cols-2 lg:grid-cols-3 gap-2 p-2">
            <CardDemo />
            <CardDemo />
            <CardDemo />
            <CardDemo />
            <CardDemo />
            <CardDemo />
          </section>
          <section className="col-span-3 md:col-span-1 bg-green-900 flex justify-center flex-col items-center">
            <CalendarDemo />
            <Table />
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}
