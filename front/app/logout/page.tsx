"use client"; // Ensures this is a client component

import { useEffect } from "react";
// import { useRouter } from "next/navigation";
import GetCookie from "../_fct/GetCookie";

function Page() {
  // const router = useRouter();

  useEffect(() => {
    const value = GetCookie({ name: "username" });

    if (value) {
      document.cookie = "username= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
    }

    // router.push("/"); // Redirect after logout
  }, []);

  return <div>
    <h1 className="text-xl text-center">Vous êtes déconnecté.</h1>
  </div>; // No need to render anything
}

export default Page;
