"use client"; // Ensures this is a client component

// import { useEffect } from "react";
// import { useRouter } from "next/navigation";
import GetCookie from "../_fct/GetCookie";
import { redirect } from "next/navigation";

function Page() {
  // const router = useRouter();

  // useEffect(() => {
  const value = GetCookie({ name: "user" });

  if (value) {
    document.cookie = "user= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/";
  } else {
    redirect("/");
  }

  // router.push("/"); // Redirect after logout
  // }, []);

  return (
    <main>
      <h1 className="text-xl text-center">Vous êtes déconnecté.</h1>
    </main>
  ); // No need to render anything
}

export default Page;
