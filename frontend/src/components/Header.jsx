import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <Link to="/" className="site-header__title">GetRawFoods</Link>
        <nav className="site-header__nav">
          <Link to="/">Directory</Link>
          <Link to="/map">Map</Link>
          <Link to="/about">About</Link>
        </nav>
        <span className="site-header__tagline">
          Sourcing knowledge for raw carnivore + ancestral diets
        </span>
      </div>
    </header>
  );
}
