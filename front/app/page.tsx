"use client";
import { useState } from "react";

function Page() {
  const slides = [
    "https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp",
    "https://img.daisyui.com/images/stock/photo-1609621838510-5ad474b7d25d.webp",
    "https://img.daisyui.com/images/stock/photo-1414694762283-acccc27bca85.webp",
    "https://img.daisyui.com/images/stock/photo-1665553365602-b2fb8e5d1707.webp",
  ];
  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <main className="mt-[1rem] grid lg:grid-cols-3 lg:grid-rows-[auto_auto_auto_1fr] gap-y-2">
      <div className="relative w-full col-span-3 overflow-hidden">
        <div
          className="flex transition-transform duration-500 ease-in-out"
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {slides.map((src, index) => (
            <img key={index} src={src} className="w-full flex-shrink-0" />
          ))}
        </div>
        <div className="absolute left-5 right-5 top-1/2 flex -translate-y-1/2 transform justify-between">
          <button
            onClick={prevSlide}
            className="btn btn-circle w-8 h-8 text-xs lg:w-12 lg:h-12 lg:text-lg"
          >
            ❮
          </button>
          <button
            onClick={nextSlide}
            className="btn btn-circle w-8 h-8 text-xs lg:w-12 lg:h-12 lg:text-lg"
          >
            ❯
          </button>
        </div>
      </div>

      <div className="col-span-3 p-5">
        <h1 className="text-2xl my-3">
          Lorem ipsum dolor sit amet consectetur adipisicing elit
        </h1>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Quod voluptas
          quas, consequatur consequuntur exercitationem ipsa eveniet minima
          itaque. Necessitatibus, ex tenetur. Facilis et aperiam magnam debitis
          ratione quisquam ex exercitationem? Enim consequatur veniam porro
          asperiores doloremque ipsum odit alias, voluptatibus nesciunt
          repudiandae omnis et esse illo dolor hic recusandae sed iste quis
          voluptatum inventore quaerat. Quas consequuntur tempore in temporibus.
          Vitae enim quidem nemo adipisci quo cumque explicabo officia impedit
          sunt. Nobis magni nulla illum, perferendis magnam, ea blanditiis
          exercitationem quia natus molestiae pariatur esse vitae architecto
          unde at vero!
        </p>
      </div>
      <div className="row-start-4 col-span-3 lg:row-start-3 lg:col-span-2">
        <h2 className="text-xl text-center">Actualités</h2>
        <div className=" h-screen overflow-y-scroll grid gap-2 p-8">
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
          <div className="bg-secondary h-max lg:h-48 rounded w-full grid lg:grid-cols-6 overflow-hidden transform hover:scale-105 transition duration-300 ease-in-out shadow-lg">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              alt=""
              className="object-cover h-40 lg:h-full row-start-1 row-end-3 lg:row-start-1 lg:row-end-2 lg:col-span-2"
            />
            <div className="row-start-3 row-end-6 lg:row-start-1 lg:row-end-2 lg:col-span-4 p-5">
              <h3 className="text-xl my-3">Titre publication</h3>
              <p>
                Description de la publication, Lorem ipsum dolor sit amet,
                consectetur adipisicing elit. Non nihil voluptates numquam
                voluptatum, quidem id eveniet ullam sed debitis beatae maxime
                magnam facilis officiis natus iusto asperiores impedit quos
                placeat!
              </p>
            </div>
          </div>
        </div>
      </div>
      {/* <div className="divider divider-horizontal">OR</div> */}
      <div className="row-start-3 col-span-3 lg:col-start-3 p-2 flex flex-col justify-around">
        <div>
          <h3 className="text-xl text-center">Événements</h3>
          <iframe
            src="https://calendar.google.com/calendar/embed?src=jwakelams%40gmail.com&ctz=Europe%2FParis"
            // style={"border: 0"}
            className="border-none w-full h-60"
            // width="800"
            // height="600"
            frameBorder="0"
            scrolling="no"
          ></iframe>
        </div>

        <div className="">
          <h3 className="text-xl text-center">Horaires-Service passeport</h3>
          <table className="table text-center border border-black w-full">
            {/* head */}
            <thead className="bg-slate-500 text-white border border-black">
              <tr className="border border-black">
                <th className="p-1 lg:p-3"></th>
                <th colSpan={2}>Matin</th>
                <th colSpan={2}>Aprés midi</th>
              </tr>
              <tr className="border border-black">
                <th className="p-1 lg:p-3">Jour</th>
                <th className="p-1 lg:p-3">début</th>
                <th className="p-1 lg:p-3">fin</th>
                <th className="p-1 lg:p-3">début</th>
                <th className="p-1 lg:p-3">fin</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border border-black">
                <th className="p-1 lg:p-3">Lundi</th>
                <td className="p-1 lg:p-3">09h00</td>
                <td className="p-1 lg:p-3">13h00</td>
                <td className="bg-black p-1 lg:p-3"></td>
                <td className="bg-black p-1 lg:p-3"></td>
              </tr>
              <tr className="border border-black">
                <th className="p-1 lg:p-3">Mardi</th>
                <td className="p-1 lg:p-3">09h00</td>
                <td className="bg-black p-1 lg:p-3"></td>
                <td className="bg-black p-1 lg:p-3"></td>
                <td>17h00</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}

export default Page;
