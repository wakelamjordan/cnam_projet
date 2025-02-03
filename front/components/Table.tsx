import React from "react";

function Table() {
  return (
    <div className="p-5 w-full">
      <h2 className="text-center text-xl">Service Passport</h2>
      <table className="table-auto border-collapse border border-black w-full">
        <thead>
          <tr>
            <th className="border border-black">Jours</th>
            <th className="border border-black">AM</th>
            <th className="border border-black">PM</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border border-black">Lundi</td>
            <td className="border border-black">10H00-11H30</td>
            <td className="border border-black">13H00-14H50</td>
          </tr>
          <tr>
            <td className="border border-black">Mercredi</td>
            <td className="border border-black">09H30-13H40</td>
            <td className="border border-black">15H00-16H00</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Table;
