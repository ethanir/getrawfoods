export default function About() {
  return (
    <article style={{ maxWidth: '70ch' }}>
      <h1>About GetRawFoods</h1>

      <p style={{ fontFamily: 'IBM Plex Serif, Georgia, serif', fontSize: '1.05rem' }}>
        GetRawFoods is a community-built sourcing knowledge base for the
        primal/raw food diet, oriented around the work of{' '}
        <a href="https://aajonus.net" target="_blank" rel="noreferrer">
          Aajonus Vonderplanitz
        </a>
        .
      </p>

      <h2>What this is</h2>
      <p>
        Sourcing primal-quality food is hard. The information is scattered
        across decade-old PDFs, broken websites, Telegram groups, Reddit
        threads, and word-of-mouth. The farms that meet Aajonus&rsquo;s
        standards often don&rsquo;t have websites at all.
      </p>
      <p>
        This site consolidates what&rsquo;s known: a directory of vetted
        suppliers, with the <em>operational knowledge</em> that turns
        &ldquo;I&rsquo;ve heard of Amos Miller&rdquo; into &ldquo;I just
        placed a successful $400 fresh-shipment order with the right
        checkout note and the right shipping window.&rdquo;
      </p>

      <h2>Verification levels</h2>
      <ul>
        <li>
          <strong>Aajonus-verified</strong> — Listed on{' '}
          <a href="https://aajonus.net" target="_blank" rel="noreferrer">aajonus.net</a>{' '}
          or in his books, with a citation.
        </li>
        <li>
          <strong>Dev-recommended</strong> — Personally vetted by the
          maintainer; meets Aajonus&rsquo;s published criteria even if not on
          his original lists.
        </li>
        <li>
          <strong>Community-verified</strong> — Submitted by community
          members and confirmed by multiple users.
        </li>
        <li>
          <strong>Unverified</strong> — Submitted but not yet confirmed.
        </li>
      </ul>

      <h2>What this isn&rsquo;t</h2>
      <p>
        Not a marketplace. Not a medical resource. Not affiliated with
        Aajonus&rsquo;s estate. Citations <em>link to</em> his original work
        on aajonus.net — they don&rsquo;t reproduce it. His writings remain
        under copyright; this site is a navigator into them, not a copy of
        them.
      </p>

      <h2>Disclaimers</h2>
      <p>
        Information on this site is presented for reference only. Nothing
        here constitutes medical, dietary, or legal advice. Raw foods carry
        inherent risks. Consult appropriate professionals.
      </p>
    </article>
  );
}
