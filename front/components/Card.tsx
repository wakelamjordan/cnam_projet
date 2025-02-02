import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import React from "react";

function CardDemo() {
  return (
    <Card className="max-w-sm mx-auto shadow-lg">
      <CardHeader>
        <CardTitle>Beautiful Landscape</CardTitle>
        <CardDescription>A stunning view of nature</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col items-center">
        <img
          src="https://www.mmv.fr/images/cms/paysage-montagne-ete/paysage-montagne-mont-blanc.jpg?frz-v=462"
          alt="A beautiful landscape"
          width="300px"
          height="200px"
          className="rounded-lg"
        />
        <p className="mt-4 text-gray-600 text-sm text-center">
          This breathtaking scenery captures the essence of tranquility and
          beauty.
        </p>
      </CardContent>
      <CardFooter className="text-center">
        <p className="text-gray-500 text-sm">
          Discover more landscapes like this.
        </p>
      </CardFooter>
    </Card>
  );
}

export default CardDemo;
