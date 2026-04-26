import { Link } from 'react-router-dom';
import VerificationBadge from './VerificationBadge';

export default function FarmRow({ farm }) {
  const location = [farm.city, farm.state].filter(Boolean).join(', ');

  return (
    <Link to={`/farms/${farm.slug}`} className="farm-row">
      <div className="farm-row__head">
        <span className="farm-row__name">{farm.name}</span>
        <VerificationBadge level={farm.verification_level} />
        {location && <span className="farm-row__location">— {location}</span>}
      </div>
      {farm.description && (
        <div className="farm-row__desc">
          {truncate(farm.description, 220)}
        </div>
      )}
    </Link>
  );
}

function truncate(text, max) {
  if (text.length <= max) return text;
  const cut = text.slice(0, max);
  const lastSpace = cut.lastIndexOf(' ');
  return cut.slice(0, lastSpace > max - 30 ? lastSpace : max) + '…';
}
