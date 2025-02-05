import Link from "next/link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSquareFacebook,
  faInstagram,
  faSquareXTwitter,
  faSquareGithub,
  faSquareDribbble,
} from "@fortawesome/free-brands-svg-icons";
// import { library } from "@fortawesome/fontawesome-svg-core";

const Footer = ({ navigation }) => {
  return (
    <footer className="bg-white py-12">
      <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="grid grid-cols-2 gap-2 justify-items-center lg:flex flex-wrap justify-center lg:space-x-6">
          {navigation.map((item, index) =>
            item.children ? (
              <ul key={index}>
                <li className="text-gray-500">{item.name}</li>
                {item.children.map((children, key) => (
                  <li key={key}>
                    <Link
                      href={children.href}
                      className="text-gray-500 hover:text-gray-900"
                    >
                      {children.name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <Link
                key={index}
                href={item.href}
                className="text-gray-500 hover:text-gray-900"
              >
                {item.name}
              </Link>
            )
          )}
        </nav>
        <div className="flex justify-center mt-8 space-x-6">
          {[
            faSquareFacebook,
            faInstagram,
            faSquareXTwitter,
            faSquareGithub,
            faSquareDribbble,
          ].map((Icon, index) => (
            <a
              key={index}
              href="#"
              className="text-gray-400 hover:text-gray-500"
            >
              <FontAwesomeIcon icon={Icon} className="w-6 h-6" />
            </a>
          ))}
        </div>
        <p className="text-center">
          <Link href={"/login"}>Login</Link>
        </p>
        <p className="mt-8 text-center text-gray-400">
          © {new Date().getFullYear()} SomeCompany, Inc. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
