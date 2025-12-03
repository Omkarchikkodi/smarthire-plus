// frontend/src/components/JobCard.jsx
/* One big translucent card, used in a 2-column grid */

function formatLocation(loc) {
  if (!loc) return "Location not specified";
  return loc.replace(/\s*,\s*/g, " · ");
}

export default function JobCard({ job }) {
  const title = job.title || "Untitled role";
  const location = formatLocation(job.location);
  const score = job.match_score != null ? job.match_score.toFixed(2) : null;
  const skills = Array.isArray(job.skills_required) ? job.skills_required : [];

  return (
    <article className="mt-[5px] pl-[20px] rounded-3xl border border-white/10 bg-slate-950/40 backdrop-blur-md 
                        px-6 py-6 md:px-8 md:py-7 shadow-xl shadow-black/60 flex flex-col gap-3">
      <h3 className="text-lg md:text-xl font-semibold leading-snug">
        {title}
      </h3>

      {/* location */}
      <div className="flex items-center gap-2 text-sm text-slate-300">
        <span className="text-base">📍</span>
        <span>{location}</span>
      </div>

      {/* match score */}
      {score && (
        <p className="text-sm text-slate-200 mt-1">
          <span className="font-semibold">Match Score:</span> {score}%
        </p>
      )}

      {/* skills */}
      <div className="mt-2">
        <p className="text-sm font-semibold text-slate-100">Skills Required:</p>
        {skills.length === 0 ? (
          <p className="text-sm text-slate-300 mt-1">Not specified</p>
        ) : (
          <ul className="mt-1 list-disc list-inside text-sm text-slate-200 space-y-0.5">
            {skills.map((s, idx) => (
              <li key={idx}>{s}</li>
            ))}
          </ul>
        )}
      </div>
    </article>
  );
}
