import { Link } from "react-router-dom";
import VerificationBadge from "./VerificationBadge";

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

export default function FarmRow({ farm }) {
  const location = [farm.city, farm.state].filter(Boolean).join(", ");
  const levels = sortLevels(farm.verification_levels);

  return (
    <article className="farm-row">
      <header className="farm-row__head">
        <Link to={`/farms/${farm.slug}`} className="farm-row__name">
          {farm.name}
        </Link>
        {levels.length > 0 && (
          <span className="farm-row__badges">
            {levels.map((level) => (
              <VerificationBadge key={level} level={level} />
            ))}
          </span>
        )}
        {location && (
          <span className="farm-row__location">— {location}</span>
        )}
      </header>
      {farm.description && (
        <p className="farm-row__desc">{farm.description}</p>
      )}
    </article>
  );
}
