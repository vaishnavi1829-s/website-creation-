import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchMovie, fetchShowtimes } from '../api';
import './MovieDetail.css';

export default function MovieDetail() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [showtimes, setShowtimes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([fetchMovie(id), fetchShowtimes(id)]).then(([m, s]) => {
      setMovie(m);
      setShowtimes(Array.isArray(s) ? s : s.showtimes || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading-container"><div className="loading-spinner" /><p>Loading...</p></div>;
  if (!movie) return <div className="loading-container"><p>Movie not found.</p><Link to="/" className="btn btn-primary">Back</Link></div>;

  const formatTime = (dt) => new Date(dt + 'Z').toLocaleString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', hour12: true });

  const theatreMap = {};
  showtimes.forEach(st => {
    const key = st.theatre_name || 'Unknown Theatre';
    if (!theatreMap[key]) theatreMap[key] = { location: st.theatre_location, facilities: st.theatre_facilities, showtimes: [] };
    theatreMap[key].showtimes.push(st);
  });

  return (
    <div className="movie-detail-page">
      <div className="movie-detail-hero">
        <div className="detail-hero-overlay" />
        <div className="detail-hero-content animate-fade-in-up">
          <div className="detail-poster-col">
            <img src={`/api/posters/${movie.id}`} alt={movie.title} className="detail-poster" />
          </div>
          <div className="detail-info-col">
            <h1>{movie.title}</h1>
            <div className="detail-badges">
              {movie.imdb_rating && <span className="detail-badge imdb-badge-detail">★ {movie.imdb_rating}</span>}
              {movie.language && <span className="detail-badge">{movie.language}</span>}
              {movie.genre && <span className="detail-badge">{movie.genre}</span>}
              {movie.rating && <span className="detail-badge cert-badge">{movie.rating}</span>}
              {movie.release_year && <span className="detail-badge">{movie.release_year}</span>}
              {movie.duration_min && <span className="detail-badge">{Math.floor(movie.duration_min/60)}h {movie.duration_min%60}m</span>}
            </div>
            <p className="detail-description">{movie.description}</p>
          </div>
        </div>
      </div>

      <div className="showtimes-section">
        <h2>Select Theatre & Showtime</h2>
        {showtimes.length === 0 ? (
          <p className="no-showtimes">No showtimes available.</p>
        ) : (
          Object.entries(theatreMap).map(([theatreName, data]) => (
            <div key={theatreName} className="theatre-block">
              <div className="theatre-header">
                <h3>{theatreName}</h3>
                <span className="theatre-location">{data.location}</span>
                <span className="theatre-facilities">{data.facilities}</span>
              </div>
              <div className="showtimes-row">
                {data.showtimes.map(st => (
                  <Link key={st.id} to={`/book/${st.id}`} className="showtime-chip">
                    <span className="chip-time">{formatTime(st.start_time)}</span>
                    <span className="chip-screen">{st.screen_name}</span>
                    <span className="chip-price">₹{st.price.toFixed(0)}</span>
                  </Link>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
