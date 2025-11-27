import React from "react";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2 className="sb-text-xl sb-mb-4 sb-font-bold">SmartHire+</h2>

      <nav className="sb-flex sb-flex-column sb-gap-3">
        <a href="#" className="sb-text-sm">Dashboard</a>
        <a href="#" className="sb-text-sm">Upload Resume</a>
        <a href="#" className="sb-text-sm">Job Matching</a>
      </nav>

      <footer className="sb-text-xs sb-mt-6 sb-opacity-50">
        powered by SmartHire AI
      </footer>
    </div>
  );
}
