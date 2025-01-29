import Image from "next/image";
import Carousel from "./_components/home/Carousel";

export default function Home() {
  return (
    <main className="bg-black row-start-2 w-full h-full md:grid grid-cols-3">
      <Carousel className="col-span-3"/>
      <div className="col-start-1 col-span-2 bg-white">zz</div>
      <div className="bg-red-400">zz</div>
    </main>
  );
}
