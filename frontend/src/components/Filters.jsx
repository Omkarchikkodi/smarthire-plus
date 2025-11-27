import React from "react";

export default function Filters({ setMinScore }) {
  return (
    <div className="sb-card sb-p-3 sb-rounded sb-bg-white sb-shadow-sm sb-flex sb-gap-3 sb-items-center sb-mb-4">
      <label className="sb-text-sm sb-opacity-70">Minimum Match Score:</label>

      <select
        className="sb-select"
        onChange={(e) => setMinScore(Number(e.target.value))}
      >
        <option value="0">Show All</option>
        <option value="50">50%+</option>
        <option value="60">60%+</option>
        <option value="70">70%+</option>
      </select>
    </div>
  );
}
