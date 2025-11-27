import React, { useState } from "react";
import axios from "axios";

import JobCard from "../components/JobCard";
import Loader from "../components/Loader";
import Filters from "../components/Filters";

export default function Recommend() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [minScore, setMinScore] = useState(0);

  const submit = async () => {
    if (!file) return alert("Upload resume first!");

    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/resume/recommend-sbert",
        form
      );
      setResults(res.data.results);
    } catch (err) {
      alert("Server error");
    }

    setLoading(false);
  };

  const filtered = results.filter(job => job.match_score >= minScore);

  return (
    <div className="sb-container sb-ml-64 sb-mt-6">
      <h1 className="sb-text-3xl sb-font-bold">SmartHire+ Recommendations</h1>

      <div className="sb-card sb-rounded sb-p-4 sb-bg-white sb-shadow-sm sb-w-96 sb-mt-4">
        <input
          type="file"
          accept="application/pdf"
          className="sb-input"
          onChange={e => setFile(e.target.files[0])}
        />
        <button onClick={submit} className="sb-btn sb-btn-primary sb-w-full sb-mt-3">
          Analyze Resume
        </button>
      </div>

      <Filters setMinScore={setMinScore} />

      {loading ? (
        <Loader />
      ) : (
        <div className="sb-grid sb-grid-3 sb-gap-4 sb-mt-4">
          {filtered.map((job, i) => (
            <JobCard key={i} job={job} />
          ))}
        </div>
      )}
    </div>
  );
}
