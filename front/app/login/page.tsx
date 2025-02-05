import { Metadata } from "next";
import Form from "./Form";
export const metadata: Metadata = {
  title: "Login",
  description: "Login app",
};
export default function Login() {
  return (
    <main className=" min-h-screens w-full row-start-2 flex align-middle">
      <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <h1 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">
            Connection
          </h1>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <Form />
        </div>
      </div>
    </main>
  );
}
