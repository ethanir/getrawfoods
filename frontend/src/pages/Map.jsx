import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { fetchFarmPins } from "../lib/api";

const PROFILES = [
  { slug: null, label: "All diets" },
  { slug: "raw_carnivore", label: "Raw carnivore" },
  { slug: "aajonus_primal", label: "Aajonus primal" },
  { slug: "weston_a_price", label: "Weston A. Price" },
];

// ADR 0002 palette: verification level -> marker color.
const PIN_COLORS = {
  aajonus_verified:   "#6b1f1f", // oxblood
  dev_recommended:    "#2d5a3d", // forest
  community_verified: "#5a4a2d", // tan
  unverified:         "#6b6b6b", // muted
};

const VERIFICATION_LABELS = {
  aajonus_verified: "Aajonus-verified",
  dev_recommended: "Dev-recommended",
  community_verified: "Community-verified",
  unverified: "Unverified",
};

// Continental US bounding box for the empty / single-pin fallback.
const US_BOUNDS = [
  [24.4, -125.0],
  [49.4, -66.9],
];

function FitBounds({ pins }) {
  const map = useMap();
  useEffect(() => {
    if (pins.length >= 2) {
      map.fitBounds(
        pins.map((p) => [p.lat, p.lng]),
        { padding: [40, 40] }
      );
    } else if (pins.length === 1) {
      map.setView([pins[0].lat, pins[0].lng], 6);
    } else {
      map.fitBounds(US_BOUNDS);
    }
  }, [pins, map]);
  return null;
}

export default function MapPage() {
  const [pins, setPins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dietProfile, setDietProfile] = useState(null);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (dietProfile) params.diet_profile = dietProfile;
    fetchFarmPins(params)
      .then((data) => {
        setPins(data);
        setError(null);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [dietProfile]);

  const legend = useMemo(
    () =>
      Object.entries(PIN_COLORS).filter(([level]) =>
        pins.some((p) => p.verification_level === level)
      ),
    [pins]
  );

  return (
    <div className="ph-container">
      <div className="ph-page-header">
        <h1 className="ph-page-title">Map</h1>
        <p className="ph-page-subtitle">
          Geographic view of the directory. Click a pin for farm details.
          Color reflects verification level.
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

      <div className="ph-result-count">
        {loading ? "loading…" : `${pins.length} pins`}
      </div>

      {error && <div className="ph-error">Failed to load: {error}</div>}

      <div className="ph-map-wrap" style={{ height: "560px" }}>
        <MapContainer
          center={[39.5, -98.35]}
          zoom={4}
          scrollWheelZoom={true}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <FitBounds pins={pins} />
          {pins.map((pin) => (
            <CircleMarker
              key={pin.slug}
              center={[pin.lat, pin.lng]}
              radius={7}
              pathOptions={{
                color: PIN_COLORS[pin.verification_level] || "#6b6b6b",
                fillColor: PIN_COLORS[pin.verification_level] || "#6b6b6b",
                fillOpacity: 0.8,
                weight: 2,
              }}
            >
              <Popup>
                <div className="ph-map-popup">
                  <Link to={`/farms/${pin.slug}`} className="ph-farm-name">
                    {pin.name}
                  </Link>
                  <div className="ph-map-popup__meta">
                    <span
                      className={`ph-badge ph-badge-${pin.verification_level}`}
                    >
                      {VERIFICATION_LABELS[pin.verification_level] ||
                        pin.verification_level}
                    </span>
                    {pin.best_for && (
                      <span className="ph-best-for">
                        best for {pin.best_for}
                      </span>
                    )}
                  </div>
                  {(pin.city || pin.state) && (
                    <div className="ph-map-popup__location">
                      {[pin.city, pin.state].filter(Boolean).join(", ")}
                    </div>
                  )}
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      <div className="ph-map-legend" aria-label="Verification level legend">
        {legend.map(([level, color]) => (
          <span key={level} className="ph-map-legend__item">
            <span
              className="ph-map-legend__dot"
              style={{ background: color }}
            />
            {VERIFICATION_LABELS[level] || level}
          </span>
        ))}
      </div>
    </div>
  );
}
