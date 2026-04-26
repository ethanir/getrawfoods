const API_BASE = "http://localhost:8000";

/**
 * Fetch farms with optional filters.
 * @param {Object} params - { verification_level, diet_profile, state, limit, offset }
 */
export async function fetchFarms(params = {}) {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, value);
    }
  }
  const url = `${API_BASE}/api/farms${query.toString() ? "?" + query.toString() : ""}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

export async function fetchFarm(slug) {
  const res = await fetch(`${API_BASE}/api/farms/${slug}`);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}
