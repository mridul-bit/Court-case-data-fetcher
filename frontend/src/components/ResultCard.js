import React from "react";

export default function ResultCard({ result }) {
  if (!result) return null;

  // If raw_html is present, show it as escaped text (not rendered HTML)
  if (result.raw_html) {
    return (
      <div className="bg-white p-6 rounded shadow whitespace-pre-wrap max-h-[600px] overflow-auto font-mono text-sm">
        {result.raw_html}
      </div>
    );
  }

  // fallback for any old parsed data structure (unlikely now)
  return (
    <div className="bg-white p-6 rounded shadow">
      <h3 className="text-lg font-bold mb-2">Case: {result.case_number || "—"}</h3>
      <p><strong>Petitioner:</strong> {result.parties && result.parties[0] ? result.parties[0] : "N/A"}</p>
      <p><strong>Respondent:</strong> {result.parties && result.parties[1] ? result.parties[1] : "N/A"}</p>
      {result.dates && result.dates.length > 0 && <p><strong>Dates:</strong> {result.dates.join(", ")}</p>}
      {result.judgments && result.judgments.length > 0 && (
        <p className="mt-2"><a href={result.judgments[0]} target="_blank" rel="noreferrer" className="text-blue-600 underline">Download latest PDF</a></p>
      )}
    </div>
  );
}

