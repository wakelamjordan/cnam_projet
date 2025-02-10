"use client"
import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import GetCookie from "../_fct/GetCookie";
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
  return (
<main className="flex justify-center items-center">
    <ul className="grid gap-3 lg:w-80">
        <li><a className="btn text-white bg-[var(--color-1)] w-full" href="/admin/profils">Profils</a></li>
        <li><a className="btn text-white bg-[var(--color-1)] w-full" href="/admin/category">Catégories</a></li>
        <li><a className="btn text-white bg-[var(--color-1)] w-full" href="/admin/photos">Photos</a></li>
        <li><a className="btn text-white bg-[var(--color-1)] w-full" href="/admin/calendar">Calendrier</a></li>
    </ul>
</main>
  );
}
export default page;
