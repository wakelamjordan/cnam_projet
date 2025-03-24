"use client";
import GetCookie from "@/app/_fct/GetCookie";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

function page() {
  const [user, setUser] = useState(null);
  // const [shouldRedirect, setShouldRedirect] = useState(false);
  const [passwordIsReset, setPasswordIsReset] = useState(false);
  const [handleUser, setHandleUser] = useState({});

  useEffect(() => {
    if (!GetCookie({ name: "user" })) {
      window.location.href = "/";
    }
    setUser(JSON.parse(decodeURIComponent(GetCookie({ name: "user" }))));
  }, []);

  // if (shouldRedirect) {
  //   redirect("/");
  // }

  if (user === null) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }
  
  //   let firstName = "";
  //   let lastName = "";
  //   let birthAt = "";
  //   let email = "";
  function handleChange(e) {
    const { id, value } = e.target;
    setHandleUser((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const today = new Date(Date.now());
    today.setHours(today.getHours() + 1);
    let userNew = { ...user };

    Object.keys(user).forEach((key) => {
      if (handleUser[key] !== undefined && handleUser[key] !== user[key]) {
        userNew[key] = handleUser[key];
      }
    });

    if (handleUser.email !== undefined && handleUser.email !== user.email) {
      userNew.newEmail = userNew.email;
      userNew.email = user.email;
    }

    document.cookie =
      `user=${encodeURIComponent(JSON.stringify(userNew))}; expires=` +
      today.toUTCString() +
      "; path=/";
    window.location.href = "/profil";
  }

  function passwordReset() {
    if (confirm("Confirmer la demande de réinitialisation ?")) {
      setPasswordIsReset(true);
    }
  }

  return (
    <main className="">
      {passwordIsReset && (
        <div role="alert" className="alert alert-info">
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
            Un mail vous a été envoyé afin de réinitialiser votre mot de passe.
          </span>
        </div>
      )}
      <form
        className="grid gap-3 lg:grid-cols-6 lg:mx-40 lg:my-20"
        onSubmit={(e) => handleSubmit(e)}
      >
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Email :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-3">
            <input
              type="email"
              className="grow"
              defaultValue={user.email}
              onChange={(e) => handleChange(e)}
              id="email"
              required
            />
          </label>
        </div>
        <button
          className="btn btn-warning lg:col-span-3 mx-auto"
          onClick={passwordReset}
          disabled={passwordIsReset}
        >
          Réinitialiser le mot de passe
        </button>
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Nom :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-3">
            <input
              type="text"
              className="grow"
              defaultValue={user.firstName}
              onChange={(e) => handleChange(e)}
              id="firstName"
            />
          </label>
        </div>
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Prénom :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-3">
            <input
              type="text"
              className="grow"
              defaultValue={user.lastName}
              onChange={(e) => handleChange(e)}
              id="lastName"
              required
            />
          </label>
        </div>
        <div className="grid grid-cols-7 items-center lg:col-span-3">
          <span className="col-span-3">Date de naissance :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-4">
            <input
              type="date"
              className="grow"
              defaultValue={user.birthAt}
              onChange={(e) => handleChange(e)}
              id="birthAt"
              required
            />
          </label>
        </div>
        {/* <div className="grid grid-cols-7 items-center">
        <span className="col-span-4">Date de création :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
        <input type="date" className="grow" value={"2025-02-09"} disabled />
        </label>
        </div>
        <div className="grid grid-cols-7 items-center">
        <span className="col-span-4">Dernière connexion :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
        <input type="date" className="grow" value={"2025-02-09"} disabled />
        </label>
        </div> */}
        <button
          className="btn text-white bg-[var(--color-1)] lg:col-start-3 lg:col-span-2 my-11 w-60 mx-auto"
          type="submit"
        >
          Sauvegarder
        </button>
      </form>
    </main>
  );
}

export default page;
