import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <>
      <h1>404 — page not found</h1>
      <p>
        Nothing here. <Link to="/">Back to the directory</Link>.
      </p>
    </>
  );
}
