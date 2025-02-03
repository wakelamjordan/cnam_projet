import React from "react";

function Card() {
  return (
    <a href="#" className="hover:scale-95 hover:shadow-2xl transition-transform duration-300 z-100">
      <div className="border border-gray-400 bg-amber-100 rounded shadow-lg p-3 w-full lg:h-56 grid grid-rows-2  lg:grid-rows-1 lg:grid-cols-6 gap-4">
        <div className="h-full overflow-hidden lg:col-span-2">
          <img
            src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
            alt="ddd"
            className="object-cover h-full rounded border border-gray-400"
          />
        </div>
        <div className="lg:col-span-4 grid grid-rows-[auto_1fr] items-center">
          <h2 className="text-2xl">Titre de la publication</h2>
          <div>
            <p className="text-lg">
              Lorem ipsum dolor sit amet, consectetur adipisicing elit.
              Voluptatum a, rerum facere commodi quis labore sint quos minus
              expedita dolores corrupti cupiditate eligendi temporibus sapiente
              aperiam sunt voluptatem, delectus inventore?
            </p>
          </div>
        </div>
      </div>
    </a>
  );
}

export default Card;
