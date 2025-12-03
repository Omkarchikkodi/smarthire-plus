import { useState } from "react";
import axios from "axios";
import Topbar from "../components/Topbar";
import Loader from "../components/Loader";
import JobCard from "../components/JobCard";

export default function Recommend() {
  const [loading, setLoading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [resume, setResume] = useState(null);

  const API_URL = "http://localhost:8000/resume/recommend-sbert";

  const submitResume = async () => {
    if (!resume) return;

    const formData = new FormData();
    formData.append("file", resume);

    setLoading(true);

    try {
      const res = await axios.post(API_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setJobs(res.data.results);
    } catch (err) {
      console.error(err);
      alert("Error processing resume");
    }

    setLoading(false);
  };

  return (
    <div>
      <Topbar />

      <div className="p-6 max-w-4xl mx-auto">
        <h2 className="text-xl font-bold mb-4">Upload Resume</h2>

        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setResume(e.target.files[0])}
          className="mb-4"
        />

        <button
          onClick={submitResume}
          className="px-6 py-2 bg-blue-600 text-white rounded"
        >
          Get Recommendations
        </button>

        {loading && <Loader />}

        <div className="mt-6">
          {jobs.map((job, i) => (
            <JobCard key={i} job={job} />
          ))}
        </div>
      </div>
    </div>
  );
}
