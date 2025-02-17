"use client";
import GetCookie from "../_fct/GetCookie";
import { useState, useEffect } from "react";
import { redirect } from "next/navigation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";

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

  const publications = [
    {
      title: "publication une",
      autor: "john.doe@example.com",
      onLine: true,
      category: "/sous_categorie11",
    },
    {
      title: "publication deux",
      autor: "john.doe@example.com",
      onLine: true,
      category: "/sous_categorie11",
    },
    {
      title: "publication trois",
      autor: "jane.smith@example.com",
      onLine: false,
      category: "/sous_categorie11",
    },
    {
      title: "publication quatre",
      autor: "alice.johnson@example.com",
      onLine: true,
      category: "/sous_categorie21",
    },
    {
      title: "publication cinq",
      autor: "alice.johnson@example.com",
      onLine: true,
      category: "/sous_categorie22",
    },
    {
      title: "publication six",
      autor: "admin@gmail.com",
      onLine: true,
      category: "/sous_categorie12",
    },
  ];
  return (
    <main>
      <div className="my-2">
        <a href="" className="btn btn-success"><FontAwesomeIcon icon={faPlus} className="text-white"/></a>
      </div>
      <div className="overflow-x-auto max-h-[60vh]">
        <table className="table table-zebra">
          {/* head */}
          <thead>
            <tr className="bg-black text-white sticky top-0">
              <th>Titre</th>
              <th className="hidden lg:table-cell">Auteur</th>
              <th className="hidden lg:table-cell">Catégorie</th>
              <th>En ligne</th>
            </tr>
          </thead>
          <tbody>
            {/* row 1 */}
            {publications.map((item, key) => (
              <tr key={key}>
                <td>{item.title}</td>
                <td className="hidden lg:table-cell">{item.autor}</td>
                <td className="hidden lg:table-cell">{item.category}</td>
                <td>{item.onLine && <div className="badge badge-primary">En ligne</div>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
export default page;
