import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { fetchMovie, fetchShowtimes } from '../api';
import './MovieDetail.css';

export default function MovieDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [showtimes, setShowtimes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [m, st] = await Promise.all([
          fetchMovie(id),
          fetchShowtimes(id),
        ]);
        setMovie(m);
        setShowtimes(st);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!movie) return <div className="error">Movie not found</div>;

  // Group showtimes by date
  const grouped = {};
  showtimes.forEach((st) => {
    const dateKey = new Date(st.start_time).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
    });
    if (!grouped[dateKey]) grouped[dateKey] = [];
    grouped[dateKey].push(st);
  });

  return (
    <div className="movie-detail">
      <Link to="/" className="back-link">&larr; Back to Movies</Link>

      <div className="movie-detail-layout">
        <div className="movie-detail-poster">
          <img
            src={movie.poster_url || 'https://picsum.photos/seed/default/400/600'}
            alt={movie.title}
          />
        </div>

        <div className="movie-detail-info">
          <h1>{movie.title}</h1>
          <div className="movie-detail-meta">
            {movie.rating && <span className="meta-badge rating">{movie.rating}</span>}
            {movie.genre && <span className="meta-badge genre">{movie.genre}</span>}
            {movie.duration_min && <span className="meta-badge duration">{movie.duration_min} min</span>}
            {movie.language && <span className="meta-badge language">{movie.language}</span>}
          </div>
          <p className="movie-detail-desc">{movie.description}</p>
        </div>
      </div>

      <div className="showtimes-section">
        <h2>Showtimes</h2>
        {showtimes.length === 0 && (
          <p className="text-muted">No showtimes available for this movie.</p>
        )}

        {Object.entries(grouped).map(([date, times]) => (
          <div key={date} className="showtime-group">
            <h3 className="showtime-date">{date}</h3>
            <div className="showtime-chips">
              {times.map((st) => (
                <button
                  key={st.id}
                  className="showtime-chip"
                  onClick={() => navigate(`/book/${st.id}`)}
                >
                  <span className="chip-time">
                    {new Date(st.start_time).toLocaleTimeString('en-US', {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                  <span className="chip-screen">{st.screen_name}</span>
                  <span className="chip-price">${st.price.toFixed(2)}</span>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
