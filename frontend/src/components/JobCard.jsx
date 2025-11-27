import React from "react";

export default function JobCard({ job }) {
  return (
    <div className="sb-card sb-p-4 sb-rounded sb-bg-white sb-card-hover sb-shadow-sm">
      <h2 className="sb-text-lg sb-font-bold sb-mb-2">{job.title}</h2>

      <p><strong>Location:</strong> {job.location || "—"}</p>
      <p><strong>Industry:</strong> {job.industry || "—"}</p>

      <p className="sb-mt-2">
        <strong>Match Score: </strong>
        <span className="sb-badge sb-badge-success">{job.match_score}%</span>
      </p>

      <div className="sb-mt-3">
        <strong>Skills Required:</strong>
        <div className="sb-flex sb-flex-wrap sb-gap-1 sb-mt-1">
          {job.skills_required.map((s,i) => (
            <span key={i} className="sb-badge sb-badge-primary">{s}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
