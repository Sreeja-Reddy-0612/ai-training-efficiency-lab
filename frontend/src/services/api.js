const BASE_URL = "http://localhost:8000";

export async function fetchLatest() {
  const res = await fetch(`${BASE_URL}/latest`);
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${BASE_URL}/history`);
  return res.json();
}
