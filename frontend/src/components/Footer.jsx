import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <p>&copy; {new Date().getFullYear()} CineBook. All rights reserved.</p>
        <p className="footer-tagline">Your ultimate movie booking experience</p>
      </div>
    </footer>
  );
}
