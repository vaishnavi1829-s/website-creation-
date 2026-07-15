import { Link } from 'react-router-dom';
import './MovieCard.css';

export default function MovieCard({ movie }) {
  return (
    <Link to={`/movie/${movie.id}`} className="movie-card">
      <div className="movie-poster">
        <img
          src={movie.poster_url || 'https://picsum.photos/seed/default/400/600'}
          alt={movie.title}
          loading="lazy"
        />
        <div className="movie-rating">{movie.rating}</div>
      </div>
      <div className="movie-info">
        <h3 className="movie-title">{movie.title}</h3>
        <div className="movie-meta">
          <span className="movie-genre">{movie.genre}</span>
          {movie.duration_min && <span className="movie-duration">{movie.duration_min} min</span>}
        </div>
      </div>
    </Link>
  );
}
