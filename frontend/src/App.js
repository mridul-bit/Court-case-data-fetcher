import React, { useEffect, useState } from "react";
import CaseQueryForm from "./components/CaseQueryForm";
import ResultCard from "./components/ResultCard";
import { loadFormMeta, submitCase } from "./api/courtAPI";

export default function App() {
  const [meta, setMeta] = useState(null);
  const [loadingMeta, setLoadingMeta] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      setLoadingMeta(true);
      try {
        const data = await loadFormMeta();
        setMeta(data);
      } catch (err) {
        setError(err?.message || "Failed to load form data");
      } finally {
        setLoadingMeta(false);
      }
    })();
  }, []);

  const handleSubmit = async (payload) => {
    setSubmitting(true);
    setError(null);
    setResult(null);
    try {
      const resp = await submitCase(payload);
      if (resp.status === "success") {
        setResult(resp.data);
      } else {
        // server may return refreshed captcha in resp.captcha
        if (resp.captcha) setMeta((m) => ({ ...(m || {}), captcha: resp.captcha }));
        setError(resp.message || "Error from server");
      }
    } catch (err) {
      // err may contain updated captcha as well
      if (err && err.captcha) {
        setMeta((m) => ({ ...(m || {}), captcha: err.captcha }));
        setError(err.message || "CAPTCHA invalid. Try again.");
      } else {
        setError(err?.message || "Network or server error.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const refreshCaptcha = async () => {
    setLoadingMeta(true);
    try {
      const data = await loadFormMeta();
      setMeta(data);
      setError(null);
    } catch (err) {
      setError(err?.message || "Failed to refresh captcha");
    } finally {
      setLoadingMeta(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl text-center font-bold mb-6">Delhi High Court — Case Dashboard</h1>

      {loadingMeta && <div className="text-center">Loading form...</div>}

      {!loadingMeta && meta && (
        <CaseQueryForm meta={meta} onSubmit={handleSubmit} submitting={submitting} refreshCaptcha={refreshCaptcha} />
      )}

      {error && <div className="max-w-2xl mx-auto mt-4 text-center text-red-600">{error}</div>}

      {result && (
        <div className="max-w-3xl mx-auto mt-6">
          <ResultCard result={result} />
        </div>
      )}
    </div>
  );
}

