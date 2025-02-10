"use client";
import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import GetCookie from "@/app/_fct/GetCookie";

function page() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    if (GetCookie({ name: "user" })) {
      setUser(JSON.parse(decodeURIComponent(GetCookie({ name: "user" }))));
    } else {
      return redirect("/");
    }
  }, []);

  if (user === null) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }

  if (!user) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }
  return <main>Catégorie</main>;
}

export default page;
