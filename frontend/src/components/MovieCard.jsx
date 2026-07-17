import { Link } from 'react-router-dom';
import './MovieCard.css';

export default function MovieCard({ movie }) {
  const { id, title, genre, language, duration_min, rating, release_year, imdb_rating } = movie;

  const hours = Math.floor(duration_min / 60);
  const mins = duration_min % 60;
  const duration = `${hours}h ${mins}m`;

  const posterSrc = `/api/posters/${id}`;

  return (
    <Link to={`/movie/${id}`} className="movie-card">
      <div className="movie-card-poster">
        <img
          src={posterSrc}
          alt={title}
          loading="lazy"
        />
        <div className="movie-card-overlay">
          <span className="btn btn-primary book-now-btn">Book Now</span>
        </div>
        {imdb_rating && (
          <div className="imdb-badge">
            <span className="imdb-star">★</span>
            {imdb_rating}
          </div>
        )}
      </div>
      <div className="movie-card-info">
        <h3 className="movie-card-title">{title}</h3>
        <div className="movie-card-meta">
          {language && <span className="meta-tag lang-tag">{language}</span>}
          {genre && <span className="meta-tag genre-tag">{genre}</span>}
          {rating && <span className="meta-tag rating-tag">{rating}</span>}
        </div>
        <div className="movie-card-details">
          {duration && <span>{duration}</span>}
          {release_year && <span>{release_year}</span>}
        </div>
      </div>
    </Link>
  );
}
