import React, { useState } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = localStorage.getItem("authToken");
      const response = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        headers: {
          Authorization: `Token ${token}`,
        },
        body: formData,
    });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      setMessage("Upload successful");
      setFile(null);
    } catch (error) {
      setMessage("Error uploading file");
    }
  };

  return (
    <div>
      <h2>Upload CSV</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <br /><br />
        <button type="submit">Upload</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default UploadForm;