"use client"; // Ensures this is a client component

import { useEffect, useState } from "react";
// import { useRouter } from "next/navigation";
import GetCookie from "../_fct/GetCookie";
import { redirect } from "next/navigation";

function Page() {
  // const router = useRouter();
  const [shouldRedirect, setShouldRedirect] = useState(false);

  useEffect(() => {
    const value = GetCookie({ name: "user" });

    if (value) {
      document.cookie =
        "user= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    } else {
      window.location.href = "/";
    }
  }, []);

  if (shouldRedirect) {
    redirect("/");
  }

  return (
    <main>
      <h1 className="text-xl text-center">Vous êtes déconnecté.</h1>
    </main>
  ); // No need to render anything
}

export default Page;
