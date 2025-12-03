export default function Filters({ setFilter }) {
  return (
    <div className="bg-white p-4 shadow rounded flex gap-4">
      <button
        onClick={() => setFilter("high")}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        High Match
      </button>

      <button
        onClick={() => setFilter("all")}
        className="px-4 py-2 bg-gray-200 rounded"
      >
        All Jobs
      </button>
    </div>
  );
}
