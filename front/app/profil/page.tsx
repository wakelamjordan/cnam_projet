"use client";
import GetCookie from "../_fct/GetCookie";
import { useState, useEffect } from "react";
import { redirect } from "next/navigation";

function page() {
  const [user, setUser] = useState({});
  useEffect(() => {
    if (GetCookie({ name: "user" })) {
      setUser(JSON.parse(decodeURIComponent(GetCookie({ name: "user" }))));
    } else {
      return redirect("/");
    }
  }, []);

  if (!user) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }

  return (
    <main className="grid gap-3 lg:grid-cols-6 lg:mx-40 lg:my-20">
      {user.newEmail && (
        <div role="alert" className="alert alert-info lg:col-span-6">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="h-6 w-6 shrink-0 stroke-current"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <span>
            Un mail vous a été envoyé à l'adresse {user.newEmail} pour la
            valider.
          </span>
        </div>
      )}
      <div className="grid grid-cols-4 items-center lg:col-span-3">
        <span className="">Email :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="text" className="grow" value={user.email} disabled />
        </label>
      </div>
      <div className="grid grid-cols-4 items-center lg:col-span-3">
        <span className="">Nom :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="text" className="grow" value={user.firstName} disabled />
        </label>
      </div>
      <div className="grid grid-cols-4 items-center lg:col-span-3">
        <span className="">Prénom :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="text" className="grow" value={user.lastName} disabled />
        </label>
      </div>
      <div className="grid grid-cols-7 items-center lg:col-span-3">
        <span className="col-span-3">Date de naissance :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-4">
          <input type="date" className="grow" value={user.birthAt} disabled />
        </label>
      </div>
      <div className="grid grid-cols-7 items-center lg:col-span-3">
        <span className="col-span-4">Date de création :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="date" className="grow" value={"2025-02-09"} disabled />
        </label>
      </div>
      <div className="grid grid-cols-7 items-center lg:col-span-3">
        <span className="col-span-4">Dernière connexion :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="date" className="grow" value={"2025-02-09"} disabled />
        </label>
      </div>
      <a
        className="btn text-white bg-[var(--color-1)] lg:col-start-3 lg:col-span-2 my-11 w-60 mx-auto"
        href="/profil/edit"
      >
        Modifier
      </a>
    </main>
  );
}

export default page;
