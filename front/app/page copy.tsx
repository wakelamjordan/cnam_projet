import { faHouse } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function page() {
  return (
    <main className="min-h-screen mt-[1rem]">
        <FontAwesomeIcon icon={faHouse} className="w-7" />
    </main>
  );
}

export default page;
