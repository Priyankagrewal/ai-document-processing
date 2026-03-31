import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const API = "http://127.0.0.1:8000";

  const [docs, setDocs] = useState([]);
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState("");
  const [selectedDoc, setSelectedDoc] = useState(null);

  // Fetch documents
  const fetchDocs = async () => {
    const res = await axios.get(`${API}/documents`);
    setDocs(res.data);
  };

  // Fetch progress
  const fetchProgress = async () => {
    const res = await axios.get(`${API}/progress`);
    setProgress(res.data.progress);
  };

  useEffect(() => {
    fetchDocs();
    const interval = setInterval(() => {
      fetchDocs();
      fetchProgress();
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // Upload
  const uploadFile = async () => {
    if (!file) return alert("Select file first");
    const formData = new FormData();
    formData.append("file", file);
    await axios.post(`${API}/upload`, formData);
  };

  // Retry
  const retry = async (id) => {
    await axios.post(`${API}/retry/${id}`);
  };

  // Edit
  const update = async (id) => {
    const result = prompt("Enter result:");
    if (!result) return;
    await axios.put(`${API}/documents/${id}?result=${result}`);
  };

  // Finalize
  const finalize = async (id) => {
    await axios.put(`${API}/documents/${id}?result=Finalized`);
  };

  const getColor = (status) => {
    if (status === "completed") return "#22c55e";
    if (status === "processing") return "#f59e0b";
    if (status === "queued") return "#3b82f6";
    if (status === "failed") return "#ef4444";
    return "#6b7280";
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg,#1e3a8a,#9333ea)",
      padding: 30,
      fontFamily: "Segoe UI",
      color: "white"
    }}>

      <h1>🚀 AI Document Dashboard</h1>

      {/* Upload */}
      <div style={card}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button style={btnPrimary} onClick={uploadFile}>Upload</button>
      </div>

      {/* Progress */}
      <div style={card}>
        <p>Progress: {progress}</p>
        {progress !== "job_completed" && <p>⏳ Processing...</p>}
      </div>

      {/* Table */}
      <div style={card}>
        <table style={{ width: "100%", textAlign: "center" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>File</th>
              <th>Status</th>
              <th>Result</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {docs.length === 0 ? (
              <tr>
                <td colSpan="5">No documents uploaded yet 📄</td>
              </tr>
            ) : (
              docs.map((d) => (
                <tr key={d.id}>
                  <td>{d.id}</td>

                  <td
                    onClick={() => setSelectedDoc(d)}
                    style={{ cursor: "pointer", textDecoration: "underline" }}
                  >
                    {d.filename}
                  </td>

                  <td>
                    <span style={{
                      background: getColor(d.status),
                      padding: "5px 12px",
                      borderRadius: 10
                    }}>
                      {d.status}
                    </span>
                  </td>

                  <td>{d.result}</td>

                  <td>
                    <button style={btnWarn} onClick={() => retry(d.id)}>Retry</button>
                    <button style={btnSuccess} onClick={() => update(d.id)}>Edit</button>
                    <button style={btnFinalize} onClick={() => finalize(d.id)}>Finalize</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Detail Screen */}
      {selectedDoc && (
        <div style={card}>
          <h3>📄 Document Details</h3>
          <p><b>ID:</b> {selectedDoc.id}</p>
          <p><b>File:</b> {selectedDoc.filename}</p>
          <p><b>Status:</b> {selectedDoc.status}</p>
          <p><b>Result:</b> {selectedDoc.result}</p>

          <button onClick={() => setSelectedDoc(null)}>Close</button>
        </div>
      )}

      {/* Export */}
      <div style={{ textAlign: "center" }}>
        <a href={`${API}/export/json`} target="_blank">Export JSON</a> |{" "}
        <a href={`${API}/export/csv`} target="_blank">Export CSV</a>
      </div>

    </div>
  );
}

/* Styles */
const card = {
  background: "rgba(255,255,255,0.2)",
  padding: 20,
  borderRadius: 10,
  marginBottom: 20
};

const btnPrimary = {
  marginLeft: 10,
  padding: "8px 16px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: 5
};

const btnWarn = {
  marginRight: 5,
  padding: "6px 12px",
  background: "#f59e0b",
  color: "white",
  border: "none",
  borderRadius: 5
};

const btnSuccess = {
  marginRight: 5,
  padding: "6px 12px",
  background: "#22c55e",
  color: "white",
  border: "none",
  borderRadius: 5
};

const btnFinalize = {
  padding: "6px 12px",
  background: "#6366f1",
  color: "white",
  border: "none",
  borderRadius: 5
};

export default App;