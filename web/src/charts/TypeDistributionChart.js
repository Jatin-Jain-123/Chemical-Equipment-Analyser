import React from "react";
import { Bar } from "react-chartjs-2";

function TypeDistributionChart({ distribution }) {
  const data = {
    labels: Object.keys(distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(distribution),
      },
    ],
  };

  return <Bar data={data} />;
}

export default TypeDistributionChart;