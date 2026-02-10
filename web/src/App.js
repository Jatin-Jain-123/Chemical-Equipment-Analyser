import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import DatasetList from "./components/DatasetList";
import Login from "./components/Login";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("authToken")
  );
  const [refreshKey, setRefreshKey] = useState(0);

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Chemical Equipment Visualizer</h1>
      <button onClick={handleLogout}>Logout</button>

      <UploadForm onUploadSuccess={() => setRefreshKey(prev => prev + 1)} />
      <hr />
      <DatasetList refreshKey={refreshKey} />
    </div>
  );
}

export default App;