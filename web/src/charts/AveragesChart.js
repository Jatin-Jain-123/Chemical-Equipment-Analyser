import React from "react";
import { Bar } from "react-chartjs-2";

function AveragesChart({ summary }) {
  const data = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
      {
        label: "Average Values",
        data: [
          summary.average_flowrate,
          summary.average_pressure,
          summary.average_temperature,
        ],
      },
    ],
  };

  return <Bar data={data} />;
}

export default AveragesChart;