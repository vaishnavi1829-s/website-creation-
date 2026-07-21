import { useState } from 'react';
import { Link } from 'react-router-dom';
import './MovieCard.css';

export default function MovieCard({ movie }) {
  const { id, title, genre, language, duration_min, rating, release_year, imdb_rating, poster_url } = movie;
  const [imgError, setImgError] = useState(false);

  const hours = Math.floor((duration_min || 0) / 60);
  const mins = (duration_min || 0) % 60;
  const duration = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;

  // Use backend proxy for reliable poster delivery (handles TMDB + SVG fallback)
  const proxyPoster = `/api/posters/${id}`;

  return (
    <Link to={`/movie/${id}`} className="movie-card">
      {/* Poster */}
      <div className="movie-card-poster">
        {!imgError ? (
          <img
            src={proxyPoster}
            alt={title}
            loading="lazy"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="poster-placeholder">
            <svg className="placeholder-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="6" fill="#1a1a2e" stroke="#3a3a55" strokeWidth="1.5" />
              <path d="M16 32V16l10 8-10 8z" fill="#6b6b80" />
              <rect x="28" y="16" width="8" height="16" rx="1" fill="#6b6b80" />
            </svg>
            <span className="placeholder-text">No Poster</span>
          </div>
        )}

        {/* IMDB Rating Badge */}
        {imdb_rating && (
          <div className="imdb-badge">
            <span className="imdb-star">★</span>
            {imdb_rating}
          </div>
        )}

        {/* Rating badge for A/UA/U */}
        {rating && (
          <div className="rating-badge">{rating}</div>
        )}
      </div>

      {/* Details */}
      <div className="movie-card-details">
        <h3 className="movie-card-title">{title}</h3>

        <div className="movie-card-meta">
          {language && <span className="meta-tag lang-tag">{language}</span>}
          {genre && <span className="meta-tag genre-tag">{genre}</span>}
          {rating && <span className="meta-tag cert-tag">{rating}</span>}
        </div>

        <div className="movie-card-sub">
          {duration_min > 0 && <span className="sub-item">{duration}</span>}
          {release_year && <span className="sub-item">{release_year}</span>}
        </div>

        <div className="movie-card-actions">
          <span className="btn btn-primary book-btn">Book Now</span>
        </div>
      </div>
    </Link>
  );
}
