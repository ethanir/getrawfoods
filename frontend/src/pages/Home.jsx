import { useEffect, useState } from "react";
import { fetchFarms } from "../lib/api";
import FarmRow from "../components/FarmRow";

const CATEGORIES = [
  { slug: "raw_dairy", label: "Raw dairy" },
  { slug: "raw_meat", label: "Raw meat" },
  { slug: "raw_organs", label: "Raw organs" },
  { slug: "oysters", label: "Oysters" },
];

export default function Home() {
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchFarms()
      .then((data) => {
        setFarms(data);
        setError(null);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <section className="page-intro">
        <h1 className="page-intro__title">Farm directory</h1>
        <p className="page-intro__desc">
          A small, hand-verified set of suppliers for raw meat, organs, dairy,
          and wild seafood. Aajonus-verified entries appear in his published
          sourcing materials; dev-verified are personally vetted by the
          maintainer.
        </p>
      </section>

      {error && (
        <p style={{ color: "var(--color-warning)" }}>Failed to load: {error}</p>
      )}

      {loading && !error && (
        <p style={{ color: "var(--color-muted)" }}>Loading…</p>
      )}

      {!loading &&
        !error &&
        CATEGORIES.map((cat) => {
          const farmsInCat = farms.filter(
            (f) => f.categories && f.categories.includes(cat.slug)
          );
          return (
            <section key={cat.slug} className="section">
              <h2 className="section__label">{cat.label}</h2>
              {farmsInCat.length === 0 ? (
                <p className="section__empty">
                  No verified suppliers yet — coming soon.
                </p>
              ) : (
                farmsInCat.map((farm) => (
                  <FarmRow key={`${cat.slug}-${farm.id}`} farm={farm} />
                ))
              )}
            </section>
          );
        })}
    </>
  );
}
