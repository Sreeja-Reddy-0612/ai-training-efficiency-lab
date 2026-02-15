const BASE_URL = "http://127.0.0.1:8000";

export async function fetchLatest() {
  const res = await fetch(`${BASE_URL}/benchmarks/latest`);
  return await res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${BASE_URL}/benchmarks/history`);
  return await res.json();
}

export async function fetchSummary() {
  const res = await fetch(`${BASE_URL}/analytics/summary`);
  return await res.json();
}
