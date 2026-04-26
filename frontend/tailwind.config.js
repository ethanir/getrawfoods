/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    // We use CSS variables (defined in src/index.css) so tokens are
    // a single source of truth and easy to adjust later.
    extend: {
      colors: {
        bg: 'var(--color-bg)',
        surface: 'var(--color-surface)',
        ink: 'var(--color-ink)',
        muted: 'var(--color-muted)',
        accent: 'var(--color-accent)',
        accentInk: 'var(--color-accent-ink)',
        border: 'var(--color-border)',
      },
      fontFamily: {
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        serif: ['"IBM Plex Serif"', 'Georgia', 'serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: {
        // Sharp edges by default (utilitarian aesthetic, ADR 0002).
        DEFAULT: '0',
        none: '0',
        sm: '0',
      },
      maxWidth: {
        prose: '72ch',
        content: '1100px',
      },
    },
  },
  plugins: [],
  corePlugins: {
    // Disable rounded corners globally — utilitarian aesthetic.
    // If we ever need a rounded element we'll opt back in.
  },
};
