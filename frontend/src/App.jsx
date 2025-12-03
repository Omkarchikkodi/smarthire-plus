// frontend/src/App.jsx
import { useState } from "react";
import JobCard from "./components/JobCard";

const API_BASE = "http://127.0.0.1:8000"; // change if your backend URL is different

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0] || null);
    setError("");
    setResults([]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setError("");
      setResults([]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select a resume first.");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_BASE}/resume/recommend-sbert`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Server error while getting recommendations.");
      }

      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations. Check backend URL and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-slate-950 via-slate-900 to-rose-900 text-slate-50">
      {/* top bar with logo */}
      <header className="flex items-center px-8 pt-6">
        <div className="inline-flex items-center rounded-full bg-gradient-to-r from-indigo-900/60 to-pink-800/60 px-8 py-3 backdrop-blur-sm shadow-md shadow-black/40">
          <h1 className="text-5xl md:text-6xl font-serif font-bold tracking-wide text-white">
            SmartHire<span className="text-pink-200">+</span>
          </h1>
        </div>
      </header>

      {/* center upload section */}
      <main className="flex flex-col items-center mt-10 px-4">
        {/* title */}
        <div className="inline-flex items-center rounded-full bg-gradient-to-r from-indigo-900/60 to-pink-800/60 px-8 py-3 backdrop-blur-sm shadow-md shadow-black/40">
          <h2 className="text-[28px] font-serif font-bold tracking-wide text-white">
            Upload your resume
          </h2>
        </div>
        <div
          className="mt-10 mx-6 md:mx-auto w-full max-w-4xl border-2 rounded-full border-slate-200/80 bg-slate-950/30 px-6 py-10 md:px-16 md:py-12 backdrop-blur-sm shadow-2xl shadow-black/60 flex items-center justify-center text-center"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="space-y-4 mb-[50px]">
            {/* Added mb-6 for space below the text */}
            <p className="text-base md:text-lg text-slate-100 mb-6">
              Drag and drop here or{" "}
              <label
                htmlFor="resume-input"
                className="underline font-semibold cursor-pointer text-sky-200 hover:text-sky-100"
              >
                upload
              </label>{" "}
              your file
            </p>
            <input
              id="resume-input"
              type="file"
              accept=".pdf,.doc,.docx"
              className="hidden"
              onChange={handleFileChange}
            />
            {file && (
              <p className="text-xs md:text-sm text-slate-300">
                Selected: <span className="font-medium">{file.name}</span>
              </p>
            )}
          </div>
        </div>

        {/* button */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="mt-[8px] rounded-full border border-slate-200/80 px-[50px] py-[20px] text-sm md:text-base font-semibold
                    bg-slate-950/40 hover:bg-slate-900/80 transition-colors
                    disabled:opacity-60 disabled:cursor-not-allowed shadow-lg shadow-black/60"
        >
          {loading ? "Getting recommendations..." : "Get recommendation"}
        </button>

        {/* error message */}
        {error && (
          <p className="mt-4 text-sm text-red-300 bg-red-950/40 px-4 py-2 rounded-lg  border-red-500/40">
            {error}
          </p>
        )}

        {/* results */}
        <section className="w-full max-w-6xl mt-14 pb-12">
          {results.length > 0 && (
            <>
              <h2 className="text-xl md:text-2xl font-semibold mb-6 px-4">
                Top matches for you
              </h2>

              {/* two-column layout like your mock (left and right big boxes) */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 px-4">
                {results.map((job) => (
                  <JobCard key={job.jobid} job={job} />
                ))}
              </div>
            </>
          )}

          {!loading && !error && results.length === 0 && (
            <p className="mt-10 text-center text-sm text-slate-300">
              Upload your resume and click{" "}
              <span className="font-semibold">Get recommendation</span> to see jobs here.
            </p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
