const TOOLTIPS = {
  aajonus_verified:
    "Listed in Aajonus Vonderplanitz's official sourcing materials.",
  dev_recommended:
    "Personally vetted by the project maintainer.",
  community_verified:
    "Submitted and verified by community contributors.",
  unverified:
    "Listed without verification — use your own judgment.",
};

const LABELS = {
  aajonus_verified: "Aajonus-verified",
  dev_recommended: "Dev-recommended",
  community_verified: "Community-verified",
  unverified: "Unverified",
};

export default function VerificationBadge({ level }) {
  const label = LABELS[level] || level;
  const tooltip = TOOLTIPS[level] || "";
  const cls = `ph-badge ph-badge-${level}`;
  return (
    <span className={cls} title={tooltip} aria-label={tooltip}>
      {label}
    </span>
  );
}
