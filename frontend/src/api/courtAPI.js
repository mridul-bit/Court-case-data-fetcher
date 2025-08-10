
const API_BASE = "http://127.0.0.1:8000/api/fetch-case/";

export async function loadFormMeta() {
  const res = await fetch(API_BASE, { method: "GET" });
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function submitCase(payload) {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

