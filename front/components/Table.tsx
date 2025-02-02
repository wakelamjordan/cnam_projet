import React from "react";

function Table() {
  return (
    <div className="my-5">
      <h2>Service Passport</h2>
      <table className="table-auto border-collapse border border-gray-400">
        <thead>
          <tr>
            <th className="border border-gray-300">Jours</th>
            <th className="border border-gray-300">AM</th>
            <th className="border border-gray-300">PM</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border border-gray-300">Lundi</td>
            <td className="border border-gray-300">10H00-11H30</td>
            <td className="border border-gray-300">13H00-14H50</td>
          </tr>
          <tr>
            <td className="border border-gray-300">Mercredi</td>
            <td className="border border-gray-300">09H30-13H40</td>
            <td className="border border-gray-300">15H00-16H00</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Table;
