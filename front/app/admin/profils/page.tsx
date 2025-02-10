"use client";
import { useEffect, useState, useRef } from "react";
import { redirect } from "next/navigation";
import GetCookie from "@/app/_fct/GetCookie";

import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function page() {
  const [user, setUser] = useState(null);
  const modalRef = useRef(null);
  const [selectedProfil, setSelectedProfil] = useState(null);

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
  const profils = [
    {
      firstName: "admin",
      lastName: "adminjr",
      email: "admin@gmail.com",
      birthAt: "1990-01-01",
      loginAt: "2025-02-10",
      createdAt: "2025-01-10",
      role: "admin",
    },
    {
      firstName: "John",
      lastName: "Doe",
      email: "john.doe@example.com",
      birthAt: "1985-05-15",
      loginAt: "2025-02-09",
      createdAt: "2025-01-05",
      role: "user",
    },
    {
      firstName: "Jane",
      lastName: "Smith",
      email: "jane.smith@example.com",
      birthAt: "1992-08-22",
      loginAt: "2025-02-08",
      createdAt: "2025-01-02",
      role: "user",
    },
    {
      firstName: "Alice",
      lastName: "Johnson",
      email: "alice.johnson@example.com",
      birthAt: "1988-11-30",
      loginAt: "2025-02-07",
      createdAt: "2025-01-01",
      role: "user",
    },
  ];

  function openModal(data) {
    setSelectedProfil(data);
    modalRef.current?.showModal();
  }
  return (
    <main className="flex justify-center items-center">
      <div></div>
      <div className="overflow-x-auto xl:w-2/3 max-h-screen">
        <table className="table table-zebra text-center">
          {/* head */}
          <thead className="sticky top-0">
            <tr className="bg-black text-white">
              <th>Email</th>
              <th className="hidden md:table-cell">Nom</th>
              <th className="hidden md:table-cell">Prenom</th>
              <th className="hidden lg:table-cell">Date de naissance</th>
              <th className="hidden lg:table-cell">Dernière connexion</th>
              <th className="hidden lg:table-cell">Date de création</th>
              <th className="hidden md:table-cell">Role</th>
            </tr>
          </thead>
          <tbody className="max-h-screen overflow-hidden">
            {profils.map((item, key) => (
              <tr key={key} onClick={() => openModal(item)}>
                <td>{item.email}</td>
                <td className="hidden md:table-cell">{item.firstName}</td>
                <td className="hidden md:table-cell">{item.lastName}</td>
                <td className="hidden lg:table-cell">{item.birthAt}</td>
                <td className="hidden lg:table-cell">{item.loginAt}</td>
                <td className="hidden lg:table-cell">{item.createdAt}</td>
                <td className="hidden md:table-cell">{item.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {/* <button className="btn" onClick={}>
          open modal
        </button> */}
        <dialog id="my_modal_4" className="modal relative" ref={modalRef}>
          <div className="modal-box">
            <div className="modal-action">
              {/* <form method="dialog"> */}
              {selectedProfil !== null ? (
                // <div className="grid gap-3 lg:grid-cols-6 lg:mx-40 lg:my-20s">
                <div className="grid">
                  {selectedProfil.newEmail && (
                    <div
                      role="alert"
                      className="alert alert-info"
                    >
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
                        Un mail vous a été envoyé à l'adresse{" "}
                        {selectedProfil.newEmail} pour la valider.
                      </span>
                    </div>
                  )}
                  <div className="">
                    <span className="">Email :</span>
                    <label className="">
                      <input
                        type="text"
                        className="grow"
                        value={selectedProfil.email}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span className="">Nom :</span>
                    <label className="">
                      <input
                        type="text"
                        className="grow"
                        value={selectedProfil.firstName}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span className="">Prénom :</span>
                    <label className="">
                      <input
                        type="text"
                        className="grow"
                        value={selectedProfil.lastName}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span className="">Date de naissance :</span>
                    <label className="">
                      <input
                        type="date"
                        className="grow"
                        value={selectedProfil.birthAt}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span className="">Date de création :</span>
                    <label className="">
                      <input
                        type="date"
                        className="grow"
                        value={selectedProfil.createdAt}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span className="">Dernière connexion :</span>
                    <label className="">
                      <input
                        type="date"
                        className="grow"
                        value={selectedProfil.loginAt}
                        disabled
                      />
                    </label>
                  </div>
                  <a
                    className="btn text-white bg-[var(--color-1)]"
                    href="/profil/edit"
                  >
                    Modifier
                  </a>
                </div>
              ) : (
                <>pas de data</>
              )}
              <button className="absolute right-4 top-2" onClick={()=>{modalRef.current?.close()}}><FontAwesomeIcon icon={faX} className="fa-xs"/></button>
              {/* </form> */}
            </div>
          </div>
        </dialog>
      </div>
    </main>
  );
}
export default page;
