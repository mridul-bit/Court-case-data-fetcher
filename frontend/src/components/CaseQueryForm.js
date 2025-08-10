import React, { useEffect, useState } from "react";

// Default mock values to fill form initially
const MOCK_CASE_TYPE = "W.P.(C)";
const MOCK_CASE_NUMBER = "1234";
const MOCK_FILING_YEAR = "2023";

export default function CaseQueryForm({ meta = {}, onSubmit, submitting, refreshCaptcha }) {
  const [caseType, setCaseType] = useState(MOCK_CASE_TYPE);
  const [caseNumber, setCaseNumber] = useState(MOCK_CASE_NUMBER);
  const [filingYear, setFilingYear] = useState(MOCK_FILING_YEAR);
  const [captchaText, setCaptchaText] = useState("");

  useEffect(() => {
    // clear captcha input on meta change
    setCaptchaText("");
  }, [meta?.captcha]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!caseType || !caseNumber || !filingYear) {
      alert("Please fill Case Type, Case Number and Filing Year.");
      return;
    }
    if (!captchaText || captchaText.trim() === "") {
      alert("Please enter CAPTCHA shown on the page.");
      return;
    }
    onSubmit({
      case_type: caseType,
      case_number: caseNumber,
      filing_year: filingYear,
      captcha_text: captchaText.trim()
    });
  };

  return (
    <div className="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1">Case Type</label>
          <select value={caseType} onChange={(e) => setCaseType(e.target.value)} className="w-full p-2 border rounded" required>
            <option value="">Select case type</option>
            {meta.case_types && meta.case_types.map((ct, i) => <option key={i} value={ct}>{ct}</option>)}
          </select>
        </div>

        <div>
          <label className="block mb-1">Case Number</label>
          <input className="w-full p-2 border rounded" value={caseNumber} onChange={(e) => setCaseNumber(e.target.value)} required />
        </div>

        <div>
          <label className="block mb-1">Filing Year</label>
          <select className="w-full p-2 border rounded" value={filingYear} onChange={(e) => setFilingYear(e.target.value)} required>
            <option value="">Select year</option>
            {meta.years && meta.years.map((y) => <option key={y} value={y}>{y}</option>)}
          </select>
        </div>

        <div>
          <label className="block mb-1">CAPTCHA (type the code shown)</label>
          <div className="flex items-center gap-3 mb-2">
            <div className="inline-block px-4 py-2 bg-gray-100 border rounded text-2xl font-mono">
              {meta.captcha || "—"}
            </div>
            <button type="button" onClick={refreshCaptcha} className="px-3 py-1 border rounded bg-white">Refresh</button>
          </div>
          <input className="w-full p-2 border rounded" value={captchaText} onChange={(e) => setCaptchaText(e.target.value)} placeholder="Enter CAPTCHA" required />
        </div>

        <div className="text-center">
          <button className="bg-blue-600 text-white px-6 py-2 rounded" type="submit" disabled={submitting}>
            {submitting ? "Searching..." : "Fetch Case Details"}
          </button>
        </div>
      </form>
    </div>
  );
}

