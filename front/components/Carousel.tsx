"use client";
import * as React from "react";
import Image from "next/image";
import Autoplay from "embla-carousel-autoplay";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

const images = [
  "https://img.daisyui.com/images/stock/photo-1625726411847-8cbb60cc71e6.webp",
  "https://img.daisyui.com/images/stock/photo-1609621838510-5ad474b7d25d.webp",
  "https://img.daisyui.com/images/stock/photo-1414694762283-acccc27bca85.webp",
  "https://img.daisyui.com/images/stock/photo-1665553365602-b2fb8e5d1707.webp",
];

export function CarouselDemo({ className = "" }) {
  const plugin = React.useRef(
    Autoplay({ delay: 2000, stopOnInteraction: true })
  );

  return (
    <Carousel
      plugins={[plugin.current]}
      className={`w-full relative ${className}`}
      onMouseEnter={() => plugin.current?.stop()}
      onMouseLeave={() => plugin.current?.play()}
    >
      <CarouselContent>
        {images.map((item, index) => (
          <CarouselItem key={index}>
            <img
              src={item}
              //   width="w-full" // Adjust width as needed
              //   height="300px" // Adjust height as needed
              //   width={300} // Adjust width as needed
              //   height={300} // Adjust height as needed
              className="w-full h-full object-cover"
              //   alt={`Slide ${index + 1}`}
            />
          </CarouselItem>
        ))}
      </CarouselContent>

      <CarouselPrevious className="absolute left-7 hidden md:flex" />

      <CarouselNext className="absolute right-7 hidden md:flex"/>
    </Carousel>
  );
}
