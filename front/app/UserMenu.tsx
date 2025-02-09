"use client";
import { useEffect, useState } from "react";
import GetCookie from "./_fct/GetCookie";

function UserMenu() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(
      JSON.parse(
        decodeURIComponent(
          GetCookie(
            { name: "user" }
          )
        )
      )
    );
    
  }, []);
  if (!user) return null;
  // console.log(user);


  return (
    <div className="dropdown dropdown-end">
      <div
        tabIndex={0}
        role="button"
        className="btn btn-ghost btn-circle avatar"
      >
        <div className="w-10 h-10 rounded-full bg-slate-500 capitalize relative">
          <span className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white text-lg font-bold">
            {user.lastName[0]}
          </span>
        </div>
      </div>
      <ul
        tabIndex={0}
        className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
      >
        <li>
          <a href="/profil" className="justify-between">
            Profil
            {/* <span className="badge">New</span> */}
          </a>
        </li>
        <li>
          <a>Admin</a>
        </li>
        <li>
          <a href="/logout" 
          onClick={handleLogout}
          >
            Déconnexion
          </a>
        </li>
      </ul>
    </div>
  );
}

// // Function to handle logout
const handleLogout = (setUsername) => {
  document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/"; // Delete cookie
  setUsername(null); // Update state to re-render component
};

export default UserMenu;
