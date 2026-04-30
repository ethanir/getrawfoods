const TOOLTIPS = {
  aajonus_verified:
    "Listed in Aajonus Vonderplanitz's published sourcing materials.",
  dev_verified:
    "Personally verified by the maintainer — orders from this farm regularly.",
  community_verified:
    "Submitted and verified by community contributors.",
  unverified:
    "Listed without verification — use your own judgment.",
};

const LABELS = {
  aajonus_verified: "Aajonus-verified",
  dev_verified: "Dev-verified",
  community_verified: "Community-verified",
  unverified: "Unverified",
};

export default function VerificationBadge({ level }) {
  const label = LABELS[level] || level;
  const tooltip = TOOLTIPS[level] || "";
  return (
    <span
      className={`badge badge--${level}`}
      title={tooltip}
      aria-label={tooltip}
    >
      {label}
    </span>
  );
}
