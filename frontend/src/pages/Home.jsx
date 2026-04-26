import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import FarmRow from '../components/FarmRow';

const VERIFICATION_OPTIONS = [
  { value: '', label: 'All verification levels' },
  { value: 'aajonus_verified', label: 'Aajonus-verified only' },
  { value: 'dev_recommended', label: 'Dev-recommended only' },
  { value: 'community_verified', label: 'Community-verified only' },
];

export default function Home() {
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ verification_level: '', q: '' });

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    api
      .listFarms({
        verification_level: filters.verification_level || undefined,
        q: filters.q.trim() || undefined,
      })
      .then((data) => {
        if (!cancelled) setFarms(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message || 'Failed to load farms');
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [filters.verification_level, filters.q]);

  return (
    <>
      <section style={{ marginBottom: '1rem' }}>
        <h1>Farm directory</h1>
        <p style={{ color: 'var(--color-muted)', maxWidth: '60ch' }}>
          Verified suppliers of raw dairy, grass-fed organs, wild seafood, and
          other raw food staples. Aajonus-verified entries are sourced from
          his published lists and books; dev-recommended are personally vetted.
        </p>
      </section>

      <div className="filter-bar">
        <input
          type="search"
          placeholder="Search farms…"
          value={filters.q}
          onChange={(e) => setFilters((f) => ({ ...f, q: e.target.value }))}
          style={{ flex: '1 1 12rem', minWidth: '12rem' }}
        />
        <select
          value={filters.verification_level}
          onChange={(e) =>
            setFilters((f) => ({ ...f, verification_level: e.target.value }))
          }
        >
          {VERIFICATION_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </div>

      {loading && (
        <p style={{ color: 'var(--color-muted)' }}>Loading farms…</p>
      )}
      {error && (
        <p style={{ color: 'var(--color-warning)' }}>
          Couldn&rsquo;t load farms: {error}. Is the backend running on port 8000?
        </p>
      )}
      {!loading && !error && farms.length === 0 && (
        <p style={{ color: 'var(--color-muted)' }}>
          No farms match those filters.
        </p>
      )}

      {!loading && !error && farms.length > 0 && (
        <>
          <div style={{
            color: 'var(--color-muted)',
            fontSize: '0.85rem',
            fontFamily: 'IBM Plex Mono, ui-monospace, monospace',
            padding: '0.5rem 0',
          }}>
            {farms.length} {farms.length === 1 ? 'farm' : 'farms'}
          </div>
          {farms.map((farm) => (
            <FarmRow key={farm.id} farm={farm} />
          ))}
        </>
      )}
    </>
  );
}
