/**
 * API client. Single place to change if we move endpoints around.
 *
 * No fancy fetch wrapper — just thin functions returning parsed JSON.
 * If we ever need caching, retries, or auth headers, they go here.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new ApiError(res.status, text || res.statusText);
  }

  return res.json();
}

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

export const api = {
  listFarms: ({ state, verification_level, q, limit = 50, offset = 0 } = {}) => {
    const params = new URLSearchParams();
    if (state) params.set('state', state);
    if (verification_level) params.set('verification_level', verification_level);
    if (q) params.set('q', q);
    params.set('limit', String(limit));
    params.set('offset', String(offset));
    return request(`/api/farms?${params.toString()}`);
  },

  getFarm: (slug) => request(`/api/farms/${encodeURIComponent(slug)}`),

  health: () => request('/health'),
};
