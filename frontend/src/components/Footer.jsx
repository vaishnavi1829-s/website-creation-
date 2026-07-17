import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-brand">
          <h3>🎬 CineBook</h3>
          <p>Your premium movie ticket booking experience. Watch the latest Tamil & English movies in IMAX, Dolby & Standard screens.</p>
        </div>
        <div className="footer-links">
          <div className="footer-col">
            <h4>Movies</h4>
            <Link to="/">Trending</Link>
            <Link to="/">Tamil Movies</Link>
            <Link to="/">English Movies</Link>
          </div>
          <div className="footer-col">
            <h4>Genres</h4>
            <Link to="/">Action</Link>
            <Link to="/">Romantic</Link>
            <Link to="/">Thriller</Link>
          </div>
          <div className="footer-col">
            <h4>Contact</h4>
            <span>support@cinebook.com</span>
            <span>+91 98765 43210</span>
            <span>Chennai, Tamil Nadu</span>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} CineBook. All rights reserved. All prices in ₹.</p>
      </div>
    </footer>
  );
}
