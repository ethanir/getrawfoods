const LABELS = {
  aajonus_verified: { text: 'Aajonus-verified', cls: 'badge--aajonus' },
  dev_recommended: { text: 'Dev-recommended', cls: 'badge--dev' },
  community_verified: { text: 'Community', cls: 'badge--community' },
  unverified: { text: 'Unverified', cls: 'badge--unverified' },
};

export default function VerificationBadge({ level }) {
  const meta = LABELS[level] || LABELS.unverified;
  return <span className={`badge ${meta.cls}`}>{meta.text}</span>;
}
