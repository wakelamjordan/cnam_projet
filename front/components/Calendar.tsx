"use client";

import * as React from "react";

import { Calendar as C} from "@/components/ui/calendar";

export function Calendar() {
  const [date, setDate] = React.useState<Date | undefined>(new Date());

  return (
    <C
      mode="single"
      selected={date}
      onSelect={setDate}
      className="rounded-md"
    />
  );
}
