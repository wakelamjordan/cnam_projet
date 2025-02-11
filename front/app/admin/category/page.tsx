"use client";
import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import GetCookie from "@/app/_fct/GetCookie";
import { Ultra } from "next/font/google";

function page() {
  const [user, setUser] = useState(null);
  const [categories, setCategories] = useState(null);

  useEffect(() => {
    if (
      GetCookie({ name: "categories" }) !== null &&
      GetCookie({ name: "user" }) !== null
    ) {
      setUser(JSON.parse(decodeURIComponent(GetCookie({ name: "user" }))));
      setCategories(
        JSON.parse(decodeURIComponent(GetCookie({ name: "categories" })))
      );
    } else {
      window.location.href = "/";
    }
  }, []);

  // if (shouldRedirect) {
  //   redirect("/");
  // }

  if (categories === null) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }
  // console.log(categories);

  return (
    <main className="flex justify-center items-center flex-col">
      <h1 className="text-2xl my-2">Catégories</h1>
      <div className="overflow-x-auto max-h-[60vh] w-full">
        <table className="table table-zebra text-center">
          {/* head */}
          <thead className="sticky top-0">
            <tr className="bg-black text-white">
              <th>Libelle</th>
              <th className="hidden md:table-cell">Url</th>
              <th className="hidden md:table-cell">Parent</th>
              <th className="hidden md:table-cell">Ordre</th>
            </tr>
          </thead>
          <tbody className="">
            {categories.map((item, key) => (
              <>
                <tr key={key}>
                  <th>{item.libelle}</th>
                  <td className="hidden md:table-cell">{item.url}</td>
                  <td className="hidden md:table-cell">
                  </td>
                  <td className="hidden md:table-cell">{item.order}</td>
                </tr>
                {item.children?.map((child, keyChild) => (
                  <tr key={key + "-" + keyChild}>
                    <th>{child.libelle}</th>
                    <td className="hidden md:table-cell">{child.url}</td>
                    <td className="hidden md:table-cell">
                      {item.libelle}
                    </td>
                    <td className="hidden md:table-cell">{child.order}</td>
                  </tr>
                ))}
              </>
            ))}
          </tbody>
        </table>
      </div>

    </main>
  );
}

export default page;
