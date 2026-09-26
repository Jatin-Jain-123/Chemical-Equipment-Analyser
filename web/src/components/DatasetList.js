import React, { useEffect, useState } from "react";
import TypeDistributionChart from "../charts/TypeDistributionChart";
import AveragesChart from "../charts/AveragesChart";

function DatasetList({ refreshKey, onAuthError }) {
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("authToken");

    fetch("http://127.0.0.1:8000/api/datasets/", {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
      .then((res) => {
        if (res.status === 401) {
          onAuthError();
          return [];
        }
        if (!res.ok) {
          throw new Error("Could not load datasets");
        }
        return res.json();
      })
      .then((data) => {
        setDatasets(data);
        setError("");
      })
      .catch(() => setError("Cannot reach the server. Is it running?"));
  }, [refreshKey, onAuthError]);
const downloadPDF = async (datasetId) => {
  const token = localStorage.getItem("authToken");

  const response = await fetch(
    `http://127.0.0.1:8000/api/datasets/${datasetId}/pdf/`,
    {
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  ).catch(() => null);

  if (!response || !response.ok) {
    setError("Could not download the PDF report");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `dataset_${datasetId}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
};

  return (
    <div>
      <h2>Last 5 Uploaded Datasets</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {datasets.map((dataset) => (
        <div
          key={dataset.id}
          style={{
            border: "1px solid #ccc",
            padding: "15px",
            marginBottom: "20px",
          }}
        >
          <h4>
            Uploaded:{" "}
            {new Date(dataset.uploaded_at).toLocaleString()}
          </h4>

          <p>Total Equipment: {dataset.summary.total_equipment}</p>

          <h5>Equipment Type Distribution</h5>
          <TypeDistributionChart
            distribution={dataset.summary.equipment_type_distribution}
          />

          <h5>Average Parameters</h5>
          <AveragesChart summary={dataset.summary} />
          <button onClick={() => downloadPDF(dataset.id)}>
            Download PDF Report
          </button>
        </div>
      ))}
    </div>
  );
}

export default DatasetList;