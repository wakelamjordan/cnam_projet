"use client";
import GetCookie from "@/app/_fct/GetCookie";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

function Page() {
  const [actualUser, setActualUser] = useState(null);
  const [user, setUser] = useState({});
  const [handleUser, setHandleUser] = useState({});
  const [passwordIsReset, setPasswordIsReset] = useState(false);
  const router = useRouter();

  // Vérifier le cookie utilisateur et récupérer les paramètres d'URL
  useEffect(() => {
    const userCookie = GetCookie({ name: "user" });

    if (!userCookie) {
      router.push("/");
      return;
    }

    setActualUser(JSON.parse(decodeURIComponent(userCookie)));

    const url = new URL(window.location.href);
    setUser(Object.fromEntries(url.searchParams.entries()));
  }, [router]);

  if (!actualUser) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }

  function handleChange(e) {
    const { id, value } = e.target;
    setHandleUser((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    // const today = new Date(Date.now());
    // today.setHours(today.getHours() + 1);
    // let userNew = { ...user };

    // Object.keys(user).forEach((key) => {
    //   if (handleUser[key] !== undefined && handleUser[key] !== user[key]) {
    //     userNew[key] = handleUser[key];
    //   }
    // });

    // if (handleUser.email !== undefined && handleUser.email !== user.email) {
    //   userNew.newEmail = userNew.email;
    //   userNew.email = user.email;
    // }

    // document.cookie =
    //   `user=${encodeURIComponent(JSON.stringify(userNew))}; expires=` +
    //   today.toUTCString() +
    //   "; path=/";

    router.push("/admin/profils");
  }

  function passwordReset() {
    if (confirm("Confirmer la demande de réinitialisation ?")) {
      setPasswordIsReset(true);
    }
  }
  window.history.replaceState(null, "", window.location.pathname);
  return (
    <main>
      <h1 className="text-2xl my-2">Édition de profil</h1>
      {passwordIsReset && (
        <div role="alert" className="alert alert-info">
          <span>
            Un mail vous a été envoyé afin de réinitialiser votre mot de passe.
          </span>
        </div>
      )}
      <form
        className="grid gap-3 lg:mx-40 lg:my-20 text-center md:grid-cols-2 items-end relative"
        onSubmit={handleSubmit}
      >
        <div>
          <span>Email :</span>
          <label className="input input-bordered flex items-center gap-2">
            <input
              type="email"
              className="grow text-center"
              defaultValue={user.email}
              onChange={handleChange}
              id="email"
              required
            />
          </label>
        </div>
        <button
          className="btn btn-warning"
          onClick={passwordReset}
          disabled={passwordIsReset}
        >
          Réinitialiser le mot de passe
        </button>
        <div>
          <span>Nom :</span>
          <label className="input input-bordered flex items-center gap-2">
            <input
              type="text"
              className="grow text-center"
              defaultValue={user.firstName}
              onChange={handleChange}
              id="firstName"
            />
          </label>
        </div>
        <div>
          <span>Prénom :</span>
          <label className="input input-bordered flex items-center gap-2">
            <input
              type="text"
              className="grow text-center"
              defaultValue={user.lastName}
              onChange={handleChange}
              id="lastName"
              required
            />
          </label>
        </div>
        <div>
          <span>Date de naissance :</span>
          <label className="input input-bordered flex items-center gap-2">
            <input
              type="date"
              className="grow text-center"
              defaultValue={user.birthAt}
              onChange={handleChange}
              id="birthAt"
              required
            />
          </label>
        </div>
        <div>
          <span>Date de naissance :</span>
          <label className="input input-bordered flex items-center gap-2">
            <select name="role" id="role">
              <option value={user.role}>{user.role}</option>
              <option value={user.role == "admin" ? "user" : "admin"}>
                {user.role == "admin" ? "user" : "admin"}
              </option>
            </select>
            {/* <input
              type="date"
              className="grow text-center"
              defaultValue={user.birthAt}
              onChange={handleChange}
              id="birthAt"
              required
            /> */}
          </label>
        </div>
        <button
          className="btn text-white bg-[var(--color-1)] md:col-span-2 md:w-1/2 md:mx-auto max-w-96"
          type="submit"
        >
          Sauvegarder
        </button>
        <a
          href="/admin/profils"
          className="absolute top-[-20px] lg:top-[-40px] text-lg"
        >
          {"< "}retour
        </a>
      </form>
    </main>
  );
}

export default Page;
