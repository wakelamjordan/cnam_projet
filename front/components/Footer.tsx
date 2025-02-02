import Link from "next/link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSquareFacebook,
  faInstagram,
  faSquareXTwitter,
  faSquareGithub,
  faSquareDribbble,
} from "@fortawesome/free-brands-svg-icons";

const Footer = () => {
  return (
    <footer className="bg-white py-12">
      <div className="max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex flex-wrap justify-center space-x-6">
          {["About", "Blog", "Team", "Pricing", "Contact", "Terms"].map(
            (item, index) => (
              <Link
                key={index}
                href="#"
                className="text-gray-500 hover:text-gray-900"
              >
                {item}
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
        <p className="mt-8 text-center text-gray-400">
          © {new Date().getFullYear()} SomeCompany, Inc. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
