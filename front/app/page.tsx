function page() {
  return (
    <main className="min-h-screen mt-[1rem] grid lg:grid-cols-3 lg:grid-rows-[auto_1fr] gap-2">
      {/* <div className="lg:col-span-3"> */}
        <div className="carousel w-full lg:col-span-3">
          <div id="item1" className="carousel-item w-full ">
            <img
              src="https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp"
              className="w-full object-cover"
            />
          </div>
          <div id="item2" className="carousel-item w-full">
            <img
              src="https://img.daisyui.com/images/stock/photo-1609621838510-5ad474b7d25d.webp"
              className="w-full object-cover"
            />
          </div>
          <div id="item3" className="carousel-item w-full">
            <img
              src="https://img.daisyui.com/images/stock/photo-1414694762283-acccc27bca85.webp"
              className="w-full object-cover"
            />
          </div>
          <div id="item4" className="carousel-item w-full">
            <img
              src="https://img.daisyui.com/images/stock/photo-1665553365602-b2fb8e5d1707.webp"
              className="w-full"
            />
          </div>
        </div>
        {/* <div className="flex w-full justify-center gap-2 py-2">
          <a href="#item1" className="btn btn-xs">
            1
          </a>
          <a href="#item2" className="btn btn-xs">
            2
          </a>
          <a href="#item3" className="btn btn-xs">
            3
          </a>
          <a href="#item4" className="btn btn-xs">
            4
          </a>
        </div> */}
      {/* </div> */}
      <div className="bg-black lg:col-span-2"></div>
      <div className="bg-lime-500 row-start-2 lg:col-start-3"></div>
    </main>
  );
}

export default page;
