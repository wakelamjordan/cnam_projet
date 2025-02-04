"use client";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { InputGroup } from "@/components/InputGroup";



// function navLink(n = 0, elements = []) {
//   if (n >= navigation.length) {
//     return elements; // Base case: return accumulated elements
//   }

//   const item = navigation[n];

//   if (item.children) {
//     return navLink(n + 1, [
//       ...elements,
//       <div key={item.name} className="relative group">
//         <span
//           className={classNames(
//             item.current
//               ? "bg-gray-900 text-white"
//               : "text-white hover:bg-gray-700 hover:text-white",
//             "rounded-md px-3 py-2 text-sm font-medium cursor-pointer"
//           )}
//         >
//           {item.name}
//         </span>
//         <div className="absolute left-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg hidden group-hover:flex flex-col">
//           {item.children.map((child) => (
//             <a
//               key={child.name}
//               href={child.href}
//               className="px-3 py-2 text-sm text-black hover:bg-gray-700 hover:text-white rounded-md"
//             >
//               {child.name}
//             </a>
//           ))}
//         </div>
//       </div>,
//     ]);
//   } else {
//     return navLink(n + 1, [
//       ...elements,
//       <a
//         key={item.name}
//         href={item.href}
//         aria-current={item.current ? "page" : undefined}
//         className={classNames(
//           item.current
//             ? "bg-gray-900 text-white"
//             : "text-white hover:bg-gray-700 hover:text-white",
//           "rounded-md px-3 py-2 text-sm font-medium"
//         )}
//       >
//         {item.name}
//       </a>,
//     ]);
//   }
// }

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function Navbar({navigation}) {
  return (
    <div className="w-full">
      <Disclosure as="nav" className="bg-[#ED1D26] rounded">
        <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
          <div className="relative flex h-16 items-center justify-between">
            <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
              {/* Mobile menu button*/}
              <DisclosureButton className="group relative inline-flex items-center justify-center rounded-md p-2 text-white hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:outline-hidden focus:ring-inset">
                <span className="absolute -inset-0.5" />
                <span className="sr-only">Open main menu</span>
                <Bars3Icon
                  aria-hidden="true"
                  className="block size-6 group-data-open:hidden"
                />
                <XMarkIcon
                  aria-hidden="true"
                  className="hidden size-6 group-data-open:block"
                />
              </DisclosureButton>
            </div>
            <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
              {/* <div className="flex shrink-0 items-center">
              <img
              alt="Your Company"
              src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=500"
              className="h-8 w-auto"
              />
              </div> */}
              <div className="hidden sm:ml-6 sm:block">
                <div className="flex space-x-4">
                  {navigation.map((item) =>
                    item.children ? (
                      <div key={item.name} className="relative group">
                        <span
                          className={classNames(
                            item.current
                              ? "bg-gray-900 text-white"
                              : "text-white hover:bg-gray-700 hover:text-white",
                            "rounded-md px-3 py-2 text-sm font-medium cursor-pointer"
                          )}
                        >
                          {item.name}
                        </span>
                        <div className="absolute left-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg hidden group-hover:flex flex-col">
                          {item.children.map((child) => (
                            <a
                              key={child.name}
                              href={child.href}
                              className="px-3 py-2 text-sm text-black hover:bg-gray-700 hover:text-white rounded-md"
                            >
                              {child.name}
                            </a>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <a
                        key={item.name}
                        href={item.href}
                        aria-current={item.current ? "page" : undefined}
                        className={classNames(
                          item.current
                            ? "bg-gray-900 text-white"
                            : "text-white hover:bg-gray-700 hover:text-white",
                          "rounded-md px-3 py-2 text-sm font-medium"
                        )}
                      >
                        {item.name}
                      </a>
                    )
                  )}
                </div>
              </div>
            </div>
            <div className="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
              <div className="hidden md:block">
                <InputGroup />
              </div>
            </div>
          </div>
        </div>

        <DisclosurePanel className="sm:hidden">
          <div className="space-y-1 px-2 pt-2 pb-3">
            <div className="relative">
              {/* First-Level Dropdown */}
              <Disclosure>
                {navigation.map((item, key) =>
                  item.children ? (
                    <Disclosure key={item.name}>
                      {({ open }) => (
                        <div key={key} className="py-1">
                          <DisclosureButton className="rounded-md px-3 py-2 text-sm font-medium cursor-pointer text-white bg-gray-800 hover:bg-gray-700 w-full text-left flex justify-between">
                            {item.name}
                            <span
                              className={`transition-transform ${
                                open ? "rotate-180" : "rotate-0"
                              }`}
                            >
                              ▼
                            </span>
                          </DisclosureButton>
                          <DisclosurePanel className="ml-4 border-l border-gray-500 pl-2 space-y-1">
                            {item.children.map((child) => (
                              <a
                                key={child.name}
                                href={child.href}
                                className="block px-3 py-2 text-sm text-black hover:bg-gray-700 hover:text-white rounded-md"
                              >
                                {child.name}
                              </a>
                            ))}
                          </DisclosurePanel>
                        </div>
                      )}
                    </Disclosure>
                  ) : (
                    <a
                      key={item.name}
                      href={item.href}
                      className="block px-3 py-2 text-sm text-white hover:bg-gray-700 hover:text-white rounded-md"
                    >
                      {item.name}
                    </a>
                  )
                )}
                <InputGroup />
              </Disclosure>
            </div>
          </div>
        </DisclosurePanel>
      </Disclosure>
    </div>
  );
}
