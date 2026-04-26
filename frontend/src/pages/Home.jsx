import { useEffect, useState } from "react";
import { fetchFarms } from "../lib/api";
import FarmRow from "../components/FarmRow";

const PROFILES = [
  { slug: null, label: "All diets" },
  { slug: "raw_carnivore", label: "Raw carnivore" },
  { slug: "aajonus_primal", label: "Aajonus primal" },
  { slug: "weston_a_price", label: "Weston A. Price" },
];

export default function Home() {
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const [verificationLevel, setVerificationLevel] = useState("");
  const [dietProfile, setDietProfile] = useState(null);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (verificationLevel) params.verification_level = verificationLevel;
    if (dietProfile) params.diet_profile = dietProfile;
    fetchFarms(params)
      .then((data) => {
        setFarms(data);
        setError(null);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [verificationLevel, dietProfile]);

  const filtered = search
    ? farms.filter((f) =>
        f.name.toLowerCase().includes(search.toLowerCase()) ||
        (f.description || "").toLowerCase().includes(search.toLowerCase())
      )
    : farms;

  return (
    <div className="ph-container">
      <div className="ph-page-header">
        <h1 className="ph-page-title">Farm directory</h1>
        <p className="ph-page-subtitle">
          A small, curated set of suppliers for raw meat, organs, dairy, and
          wild seafood. Aajonus-verified entries are sourced from his published
          materials; dev-recommended are personally vetted.
        </p>
      </div>

      <div className="ph-profile-pills" role="tablist" aria-label="Diet profile">
        {PROFILES.map((p) => (
          <button
            key={p.slug || "all"}
            role="tab"
            aria-selected={dietProfile === p.slug}
            className={`ph-profile-pill ${
              dietProfile === p.slug ? "is-active" : ""
            }`}
            onClick={() => setDietProfile(p.slug)}
          >
            {p.label}
          </button>
        ))}
      </div>

      <div className="ph-filter-bar">
        <input
          type="text"
          className="ph-input"
          placeholder="Search farms…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="ph-select"
          value={verificationLevel}
          onChange={(e) => setVerificationLevel(e.target.value)}
        >
          <option value="">All verification levels</option>
          <option value="aajonus_verified">Aajonus-verified</option>
          <option value="dev_recommended">Dev-recommended</option>
          <option value="community_verified">Community-verified</option>
        </select>
      </div>

      <div className="ph-result-count">
        {loading ? "loading…" : `${filtered.length} farms`}
      </div>

      {error && <div className="ph-error">Failed to load: {error}</div>}

      <div>
        {filtered.map((farm) => (
          <FarmRow key={farm.id} farm={farm} />
        ))}
        {!loading && filtered.length === 0 && (
          <div className="ph-empty">No farms match those filters.</div>
        )}
      </div>
    </div>
  );
}
