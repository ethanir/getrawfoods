import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchFarm } from "../lib/api";
import VerificationBadge from "../components/VerificationBadge";

const PRODUCT_LABELS = {
  raw_milk: "Raw milk",
  raw_cow_milk: "Raw cow milk",
  raw_goat_milk: "Raw goat milk",
  raw_sheep_milk: "Raw sheep milk",
  raw_water_buffalo_milk: "Raw water buffalo milk",
  raw_camel_milk: "Raw camel milk",
  raw_cream: "Raw cream",
  raw_butter: "Raw butter",
  raw_cheese: "Raw cheese",
  raw_cottage_cheese: "Raw cottage cheese",
  raw_kefir: "Raw kefir",
  raw_colostrum: "Raw colostrum",
  grass_fed_meat: "Grass-fed meat",
  ground_beef: "Ground beef",
  beef_cuts: "Beef cuts",
  beef_organs: "Beef organs",
  organ_meats: "Organ meats",
  lamb: "Lamb",
  bison: "Bison",
  pork: "Pork",
  poultry: "Poultry",
  raw_eggs: "Raw eggs",
  raw_eggs_fertile: "Raw fertile eggs",
  wild_meat: "Wild meat",
  raw_honey: "Raw honey",
  wild_seafood: "Wild seafood",
  shellfish: "Shellfish",
  live_oysters: "Live oysters",
  raw_fish: "Raw fish",
  wild_fish: "Wild fish",
  bone_marrow: "Bone marrow",
  tallow_suet: "Tallow / suet",
};

const FULFILLMENT_LABELS = {
  in_person: "In-person",
  herd_share: "Herd share",
  ships_nationwide: "Ships nationwide",
  ships_regional: "Ships regionally",
  local_delivery: "Local delivery",
};

const TIP_LABELS = {
  checkout_note: "Checkout note",
  phone_script: "Phone script",
  shipping: "Shipping",
  insider: "Insider",
  warning: "Warning",
};

const TIER_ORDER = [
  "aajonus_verified",
  "dev_verified",
  "community_verified",
  "unverified",
];

function sortLevels(levels) {
  return (levels || []).slice().sort(
    (a, b) => TIER_ORDER.indexOf(a) - TIER_ORDER.indexOf(b)
  );
}

export default function FarmDetail() {
  const { slug } = useParams();
  const [farm, setFarm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetchFarm(slug)
      .then((data) => {
        if (!cancelled) setFarm(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.status === 404 ? "not-found" : err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [slug]);

  if (loading) return <p style={{ color: "var(--color-muted)" }}>Loading…</p>;
  if (error === "not-found") {
    return (
      <>
        <h1>Farm not found</h1>
        <p>
          No farm with slug <code>{slug}</code>.{" "}
          <Link to="/">Back to directory</Link>.
        </p>
      </>
    );
  }
  if (error) return <p style={{ color: "var(--color-warning)" }}>Error: {error}</p>;
  if (!farm) return null;

  const location = [farm.city, farm.state, farm.country !== "USA" ? farm.country : null]
    .filter(Boolean)
    .join(", ");

  const levels = sortLevels(farm.verification_levels);

  return (
    <>
      <p style={{ marginBottom: "0.5rem" }}>
        <Link to="/">← Directory</Link>
      </p>

      <h1 style={{ marginBottom: "0.25rem" }}>{farm.name}</h1>
      <div className="farm-detail__head">
        {levels.map((level) => (
          <VerificationBadge key={level} level={level} />
        ))}
        {location && (
          <span style={{ color: "var(--color-muted)" }}>{location}</span>
        )}
        {farm.status !== "active" && (
          <span className="badge badge--unverified">{farm.status}</span>
        )}
      </div>

      {farm.description && (
        <p style={{ marginTop: "1rem", maxWidth: "65ch" }}>{farm.description}</p>
      )}

      {farm.verification_source && (
        <p className="farm-detail__source">
          Source: {farm.verification_source}
        </p>
      )}

      <h2 style={{ marginTop: "2rem" }}>Contact</h2>
      <dl className="definition-list">
        {farm.website && (
          <>
            <dt>Website</dt>
            <dd>
              <a href={farm.website} target="_blank" rel="noreferrer">
                {farm.website.replace(/^https?:\/\//, "")}
              </a>
            </dd>
          </>
        )}
        {farm.phone && (
          <>
            <dt>Phone</dt>
            <dd className="mono">{farm.phone}</dd>
          </>
        )}
        {farm.email && (
          <>
            <dt>Email</dt>
            <dd className="mono">{farm.email}</dd>
          </>
        )}
        {farm.contact_person && (
          <>
            <dt>Contact</dt>
            <dd>{farm.contact_person}</dd>
          </>
        )}
        {farm.fulfillment.length > 0 && (
          <>
            <dt>Fulfillment</dt>
            <dd>
              {farm.fulfillment
                .map((f) => FULFILLMENT_LABELS[f.method] || f.method)
                .join(" · ")}
            </dd>
          </>
        )}
      </dl>

      {farm.products.length > 0 && (
        <>
          <h2 style={{ marginTop: "2rem" }}>Products</h2>
          <table className="product-table">
            <thead>
              <tr>
                <th style={{ width: "14rem" }}>Product</th>
                <th>Notes</th>
                <th style={{ width: "10rem" }}>Price</th>
              </tr>
            </thead>
            <tbody>
              {farm.products.map((p, i) => (
                <tr key={i}>
                  <td>{PRODUCT_LABELS[p.product_type] || p.product_type}</td>
                  <td>
                    {p.notes || (
                      <span style={{ color: "var(--color-muted)" }}>—</span>
                    )}
                  </td>
                  <td className="mono" style={{ fontSize: "0.85rem" }}>
                    {p.price_per_unit
                      ? `${p.price_per_unit}${p.unit ? ` / ${p.unit}` : ""}`
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      {farm.tips.length > 0 && (
        <>
          <h2 style={{ marginTop: "2rem" }}>Sourcing tips</h2>
          {farm.tips.map((tip, i) => (
            <div key={i} className={`tip tip--${tip.tip_type}`}>
              <div className="tip__type">
                {TIP_LABELS[tip.tip_type] || tip.tip_type}
              </div>
              <div className="tip__title">{tip.title}</div>
              <div className="tip__body">{tip.body}</div>
            </div>
          ))}
        </>
      )}

      {farm.citations.length > 0 && (
        <>
          <h2 style={{ marginTop: "2rem" }}>Sources</h2>
          <ul style={{ paddingLeft: "1.25rem", fontSize: "0.95rem" }}>
            {farm.citations.map((c, i) => (
              <li key={i} style={{ marginBottom: "0.5rem" }}>
                <strong>{c.source_name}</strong>
                {c.source_detail && <span> — {c.source_detail}</span>}
                {c.source_url && (
                  <>
                    {" "}
                    <a href={c.source_url} target="_blank" rel="noreferrer">
                      [link]
                    </a>
                  </>
                )}
                {c.quote && (
                  <div
                    style={{
                      marginTop: "0.25rem",
                      paddingLeft: "0.75rem",
                      borderLeft: "2px solid var(--color-border)",
                      color: "var(--color-muted)",
                      fontStyle: "italic",
                    }}
                  >
                    {c.quote}
                  </div>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}
