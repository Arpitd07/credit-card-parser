import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });
    const result = await res.json();
    setData(result);
  };

  const containerStyle = {
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    maxWidth: "600px",
    margin: "50px auto",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.05)",
    backgroundColor: "#fafafa",
    textAlign: "center",
  };

  const inputStyle = {
    marginTop: "15px",
    marginBottom: "15px",
    padding: "8px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  };

  const buttonStyle = {
    padding: "8px 16px",
    borderRadius: "5px",
    border: "none",
    backgroundColor: "#4CAF50",
    color: "#fff",
    cursor: "pointer",
    fontWeight: "bold",
  };

  const buttonDisabledStyle = {
    ...buttonStyle,
    backgroundColor: "#9E9E9E",
    cursor: "not-allowed",
  };

  const resultStyle = {
    marginTop: "30px",
    textAlign: "left",
    display: "inline-block",
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "10px",
    border: "1px solid #ddd",
    boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ color: "#333" }}>Credit Card Statement Parser</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          style={inputStyle}
        />
        <br />
        <button type="submit" style={file ? buttonStyle : buttonDisabledStyle} disabled={!file}>
          Upload
        </button>
      </form>

      {data && (
        <div style={resultStyle}>
          <h3 style={{ marginTop: 0 }}>Extracted Details</h3>
          <ul style={{ paddingLeft: "20px" }}>
            {Object.entries(data).map(([k, v]) => (
              <li key={k} style={{ marginBottom: "8px" }}>
                <b>{k}:</b> {v}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
