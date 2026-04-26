import { Link } from "react-router-dom";
import VerificationBadge from "./VerificationBadge";

export default function FarmRow({ farm }) {
  const location = [farm.city, farm.state].filter(Boolean).join(", ");
  return (
    <div className="ph-farm-row">
      <div className="ph-farm-row-header">
        <Link to={`/farms/${farm.slug}`} className="ph-farm-name">
          {farm.name}
        </Link>
        <VerificationBadge level={farm.verification_level} />
        {farm.best_for && (
          <span
            className="ph-best-for"
            title={`This farm is the directory's pick for: ${farm.best_for}`}
          >
            best for {farm.best_for}
          </span>
        )}
        {location && <span className="ph-farm-location">— {location}</span>}
      </div>
      {farm.description && (
        <p className="ph-farm-description">{farm.description}</p>
      )}
    </div>
  );
}
