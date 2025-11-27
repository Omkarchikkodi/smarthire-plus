// import Sidebar from "./components/Sidebar";
// import Topbar from "./components/Topbar";
// import Recommend from "./pages/Recommend";

// export default function App() {
//   return (
//     <div className="sb-flex">
//       <Sidebar />
//       <div className="sb-flex-grow">
//         <Topbar />
//         <Recommend />
//       </div>
//     </div>
//   );
// }


import React, { useState } from "react";
import axios from "axios";

/* ============================
   GLOBAL STYLES (STONE PALETTE)
   ============================ */
const styles = `
  body {
    margin: 0;
    background: #e7e5e4; /* stone-200 */
    font-family: 'Inter', sans-serif;
  }

  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-thumb {
    background: #a8a29e; /* stone-400 */
    border-radius: 8px;
  }

  /* ===== Sidebar ===== */
  .sidebar {
    height: 100vh;
    width: 240px;
    position: fixed;
    background: #292524; /* stone-800 */
    color: #fff;
    padding: 30px 22px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    box-shadow: 4px 0 15px rgba(0,0,0,0.15);
  }

  .sidebar h2 {
    font-size: 1.6rem;
    margin-bottom: 20px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }

  .sidebar a {
    color: #e7e5e4; 
    text-decoration: none;
    padding: 8px 0;
    font-size: 0.95rem;
    transition: 0.2s;
  }
  .sidebar a:hover {
    color: #fafaf9; /* stone-50 */
    margin-left: 4px;
  }

  /* ===== Topbar ===== */
  .topbar {
    margin-left: 240px;
    backdrop-filter: blur(8px);
    background: rgba(250, 250, 249, 0.7); /* stone-50 with glass */
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    padding: 18px 30px;
    position: sticky;
    top: 0;
    z-index: 5;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  /* ===== Cards ===== */
  .card {
    background: #fafaf9; /* stone-50 */
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: 0.25s ease;
  }
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.09);
  }

  /* ===== Buttons ===== */
  .btn {
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    border: none;
    margin-top: 12px;
    cursor: pointer;
    font-weight: 600;
    background: #57534e; /* stone-600 */
    color: white;
    transition: 0.25s;
  }
  .btn:hover {
    background: #44403c; /* stone-700 */
  }

  /* ===== Inputs ===== */
  .input {
    width: 100%;
    padding: 10px;
    border: 1px solid #d6d3d1;
    border-radius: 10px;
    background: #f5f5f4; /* stone-100 */
  }

  /* ===== Spinner ===== */
  .spinner {
    width: 46px;
    height: 46px;
    border: 4px solid #d6d3d1;
    border-top-color: #57534e;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    margin-top: 40px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* ===== Grid ===== */
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 18px;
    margin-top: 20px;
  }

  .badge {
    display: inline-block;
    padding: 4px 8px;
    background: #d6d3d1; /* stone-300 */
    border-radius: 6px;
    font-size: 0.8rem;
    margin-right: 4px;
    margin-top: 4px;
  }
  .badge.success {
    background: #57534e;
    color: white;
  }
`;

/* Inject global style tag */
const StyleInject = () => <style>{styles}</style>;

/* ============================
   Components
   ============================ */

const Sidebar = () => (
  <div className="sidebar">
    <h2>SmartHire+</h2>

    <nav>
      <a href="#">Dashboard</a>
      <a href="#">Upload Resume</a>
      <a href="#">Job Matching</a>
    </nav>

    <footer style={{ marginTop: "auto", fontSize: "0.8rem", opacity: 0.6 }}>
      powered by SmartHire AI
    </footer>
  </div>
);

const Topbar = () => (
  <div className="topbar">
    <h1 style={{ fontWeight: 600 }}>Job Recommendations</h1>
    <div style={{ opacity: 0.7 }}>v1.5</div>
  </div>
);

const Loader = () => <div className="spinner"></div>;

const Filters = ({ setMinScore }) => (
  <div className="card" style={{ maxWidth: "300px", marginTop: 20 }}>
    <label>Minimum Match Score</label>
    <select className="input" onChange={(e) => setMinScore(Number(e.target.value))}>
      <option value="0">Show All</option>
      <option value="50">50%+</option>
      <option value="60">60%+</option>
      <option value="70">70%+</option>
    </select>
  </div>
);

const JobCard = ({ job }) => (
  <div className="card">
    <h2 style={{ marginBottom: 10 }}>{job.title}</h2>

    <p><strong>Location:</strong> {job.location || "—"}</p>
    <p><strong>Industry:</strong> {job.industry || "—"}</p>

    <p style={{ marginTop: 10 }}>
      <strong>Match Score:</strong>
      <span className="badge success" style={{ marginLeft: 8 }}>
        {job.match_score}%
      </span>
    </p>

    <div style={{ marginTop: 12 }}>
      <strong>Skills:</strong>
      <div>
        {job.skills_required.map((s, i) => (
          <span className="badge" key={i}>{s}</span>
        ))}
      </div>
    </div>
  </div>
);

const Recommend = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [minScore, setMinScore] = useState(0);

  const submit = async () => {
    if (!file) return alert("Upload resume first!");

    const form = new FormData();
    form.append("file", file);

    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/resume/recommend-sbert",
        form
      );
      setResults(res.data.results);
    } catch {
      alert("Server error");
    }

    setLoading(false);
  };

  const filtered = results.filter((job) => job.match_score >= minScore);

  return (
    <div style={{ marginLeft: 260, padding: "30px" }}>
      <h1 style={{ fontSize: "2rem", fontWeight: 800 }}>SmartHire+ Recommendations</h1>

      <div className="card" style={{ width: "340px", marginTop: 20 }}>
        <input
          type="file"
          accept="application/pdf"
          className="input"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button className="btn" onClick={submit}>
          Analyze Resume
        </button>
      </div>

      <Filters setMinScore={setMinScore} />

      {loading ? (
        <Loader />
      ) : (
        <div className="grid">
          {filtered.map((job, i) => (
            <JobCard key={i} job={job} />
          ))}
        </div>
      )}
    </div>
  );
};

/* ============================
   MAIN APP
   ============================ */
export default function App() {
  return (
    <>
      <StyleInject />
      <Sidebar />
      <Topbar />
      <Recommend />
    </>
  );
}
