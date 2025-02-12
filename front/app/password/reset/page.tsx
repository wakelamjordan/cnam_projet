"use client";
import { useState, useEffect } from "react";

function Page() {
  const [message, setMessage] = useState(false);
  const [email, setEmail] = useState("");
  const [urlReset, setUrlReset] = useState("");
  const [emailParam, setEmailParam] = useState("");

  const [password, setPassword] = useState("");
  const [passwordRepeat, setPasswordRepeat] = useState("");

  // ✅ Use useEffect to update state based on the URL
  useEffect(() => {
    const param = new URLSearchParams(document.location.search).get("email");
    if (param) {
      setEmailParam(param);

      window.history.replaceState(null, "", window.location.pathname);
    }
  }, []); // Empty dependency array = runs only once on mount

  function handleSubmit(e) {
    e.preventDefault();
    let url = new URL(document.location.href);
    url.searchParams.append("email", email);
    setUrlReset(url.toString()); // ✅ Convert URL object to string
    setMessage(true);
  }
const [successMessage, setSuccessMessage] = useState("");

function handleSubmitPassword(e) {
  e.preventDefault();

  if (password !== passwordRepeat) {
    setMessage(true);
    setSuccessMessage(""); // Clear success message
  } else {
    setMessage(false);
    setSuccessMessage("Mot de passe réinitialisé, vous pouvez vous connecter.");
  }
}

if(successMessage){
      return (
        <main className="mt-[1rem] flex justify-center items-center flex-col">
          <h1 className="text-2xl my-5">
            Mot de passe réinitialisé vous pouvez dés à présent vous connecter.
          </h1>
        </main>
      );
}


  if (emailParam) {
    return (
      <main className="min-h-screen mt-[1rem] p-5 flex justify-center items-center flex-col">
        <h1 className="text-2xl my-5">
          Réinitialisation mot de passe {emailParam}
        </h1>
        <form className="grid gap-3" onSubmit={handleSubmitPassword}>
          {message && (
            <div role="alert" className="alert alert-error">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 shrink-0 stroke-current"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>Les deux mots de passes doivent être identiques.</span>
            </div>
          )}
          <label className="input input-bordered flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 opacity-70"
            >
              <path
                fillRule="evenodd"
                d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
                clipRule="evenodd"
              />
            </svg>
            <input
              type="password"
              className="grow"
              required
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>
          <label className="input input-bordered flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 opacity-70"
            >
              <path
                fillRule="evenodd"
                d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
                clipRule="evenodd"
              />
            </svg>
            <input
              type="password"
              className="grow"
              required
              onChange={(event) => setPasswordRepeat(event.target.value)}
            />
          </label>
          <button className="btn text-white bg-[var(--color-1)]" type="submit">
            Réinitialiser
          </button>
        </form>
      </main>
    );
  }

  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col">
      <h1 className="text-2xl my-5 text-center">
        Formulaire de Réinitialisation <br /> de mot de passe
      </h1>
      <form className="grid gap-3" onSubmit={handleSubmit}>
        {message && (
          <>
            <div role="alert" className="alert alert-success">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 shrink-0 stroke-current"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>
                Si le compte existe, un mail vous a été envoyé avec un lien.{" "}
                <br />
                Cliquez dessus et suivez les instructions.
              </span>
            </div>
            <a href={urlReset}>Simulation lien dans le mail</a>
          </>
        )}

        {!message && (
          <>
            <label className="input input-bordered flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                fill="currentColor"
                className="h-4 w-4 opacity-70"
              >
                <path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
                <path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
              </svg>
              <input
                type="email"
                className="grow"
                placeholder="Email"
                required
                onChange={(event) => setEmail(event.target.value)}
              />
            </label>
            <button
              className="btn text-white bg-[var(--color-1)]"
              type="submit"
            >
              Réinitialisation
            </button>
          </>
        )}
      </form>
    </main>
  );
}

export default Page;
