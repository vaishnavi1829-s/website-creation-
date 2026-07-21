import { useState, useEffect, useMemo } from 'react';
import { fetchMovies, fetchNowShowingMovies, fetchShowtimes, fetchTheatres } from '../api';
import MovieCard from '../components/MovieCard';
import './Home.css';

const SECTION_ORDER = [
  { key: 'trending', label: '🔥 Trending Movies', filter: null, sort: (m) => m.trending, min: 1 },
  { key: 'tamil', label: '🎭 Tamil Movies', filter: { language: 'Tamil' } },
  { key: 'english', label: '🎬 English Movies', filter: { language: 'English' } },
  { key: 'romantic', label: '💕 Romantic', filter: { category: 'Romantic' } },
  { key: 'action', label: '💥 Action', filter: { category: 'Action' } },
  { key: 'thriller', label: '🔪 Thriller', filter: { category: 'Thriller' } },
  { key: 'horror', label: '👻 Horror/Ghost', filter: { category: 'Horror/Ghost' } },
];

export default function Home({ search, filters }) {
  const [allMovies, setAllMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nowShowingMovies, setNowShowingMovies] = useState([]);
  const [nowShowingByTheatre, setNowShowingByTheatre] = useState([]);
  const [showtimesLoading, setShowtimesLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetchMovies().then(data => { setAllMovies(data.movies || []); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  // Fetch now-showing data: theatres + showtimes grouped by theatre
  useEffect(() => {
    setShowtimesLoading(true);
    Promise.all([
      fetchTheatres(),
      fetchNowShowingMovies(7),
      fetchShowtimes(),
    ])
      .then(([theatres, nowMovies, showtimes]) => {
        setNowShowingMovies(nowMovies);
        // Build theatre -> movies -> showtimes mapping
        const movieMap = {};
        nowMovies.forEach(m => { movieMap[m.id] = m; });

        const theatreMap = {};
        theatres.forEach(t => {
          theatreMap[t.id] = { ...t, movies: [] };
        });

        const theatreMovieMap = {}; // theatre_id -> { movie_id -> { movie, showtimes[] } }
        showtimes.forEach(st => {
          const tid = null; // theatre_id not directly on showtime, we need the screen join
          // Actually showtimes returned from API have theatre_name etc. but not theatre_id.
          // We'll group by theatre_name instead.
          const key = st.theatre_name || 'Unknown';
          if (!theatreMovieMap[key]) {
            theatreMovieMap[key] = {
              name: key,
              location: st.theatre_location || '',
              facilities: st.theatre_facilities || '',
              movies: {},
            };
          }
          if (!theatreMovieMap[key].movies[st.movie_id]) {
            theatreMovieMap[key].movies[st.movie_id] = {
              movie: movieMap[st.movie_id],
              showtimes: [],
            };
          }
          if (theatreMovieMap[key].movies[st.movie_id]) {
            theatreMovieMap[key].movies[st.movie_id].showtimes.push(st);
          }
        });

        // Convert to array and sort showtimes; only include theatres with showtimes
        const grouped = Object.values(theatreMovieMap)
          .map(t => ({
            ...t,
            movies: Object.values(t.movies).filter(m => m.movie && m.showtimes.length > 0),
          }))
          .filter(t => t.movies.length > 0)
          .sort((a, b) => b.movies.length - a.movies.length);

        setNowShowingByTheatre(grouped);
        setShowtimesLoading(false);
      })
      .catch(() => setShowtimesLoading(false));
  }, []);

  // Filter based on search + active filters
  const filteredMovies = useMemo(() => {
    let list = allMovies;
    if (search) {
      const s = search.toLowerCase();
      list = list.filter(m => m.title.toLowerCase().includes(s));
    }
    if (filters.genre) list = list.filter(m => m.genre === filters.genre);
    if (filters.language) list = list.filter(m => m.language === filters.language);
    if (filters.rating) list = list.filter(m => m.rating === filters.rating);
    if (filters.release_year) list = list.filter(m => m.release_year === filters.release_year);
    return list;
  }, [allMovies, search, filters]);

  // Extract unique genres and languages for filters
  const genres = useMemo(() => [...new Set(allMovies.map(m => m.genre).filter(Boolean))].sort(), [allMovies]);
  const languages = useMemo(() => [...new Set(allMovies.map(m => m.language).filter(Boolean))].sort(), [allMovies]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner" />
        <p>Loading movies...</p>
      </div>
    );
  }

  const hasFilters = search || filters.genre || filters.language || filters.rating || filters.release_year;

  // Filtered view
  if (hasFilters) {
    return (
      <div className="home-page">
        <div className="section-container">
          <h2 className="section-title">Search Results ({filteredMovies.length})</h2>
          {filteredMovies.length === 0 ? (
            <div className="empty-state">
              <p>No movies found matching your criteria.</p>
              <p>Try adjusting your search or filters.</p>
            </div>
          ) : (
            <div className="movies-grid">{filteredMovies.map(m => <MovieCard key={m.id} movie={m} />)}</div>
          )}
        </div>
      </div>
    );
  }

  const formatShowtime = (iso) => {
    const d = new Date(iso);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
  };

  const formatDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' });
  };

  return (
    <div className="home-page">
      {/* Hero banner */}
      <div className="hero-banner">
        <div className="hero-content animate-fade-in">
          <h1>Experience Cinema Like Never Before</h1>
          <p>Book your tickets for the latest blockbusters. Tamil & English movies in IMAX, Dolby & Standard screens.</p>
        </div>
        <div className="hero-overlay" />
      </div>

      {/* Now Showing by Theatre */}
      {!showtimesLoading && nowShowingByTheatre.length > 0 && (
        <div className="now-showing-section section-container animate-fade-in-up">
          <h2 className="section-title">🎬 Now Showing in Theatres</h2>
          <div className="theatre-list">
            {nowShowingByTheatre.map(theatre => (
              <div key={theatre.name} className="theatre-group">
                <div className="theatre-header">
                  <h3 className="theatre-name">{theatre.name}</h3>
                  <span className="theatre-location">{theatre.location}</span>
                </div>
                <div className="theatre-movies">
                  {theatre.movies.map(({ movie, showtimes }) => {
                    // Group showtimes by date
                    const byDate = {};
                    showtimes.forEach(st => {
                      const d = formatDate(st.start_time);
                      if (!byDate[d]) byDate[d] = [];
                      byDate[d].push(st);
                    });
                    return (
                      <div key={movie.id} className="theatre-movie-card">
                        <div className="tms-poster" onClick={() => window.location.href = `/movie/${movie.id}`}>
                          <img
                            src={`/api/posters/${movie.id}`}
                            alt={movie.title}
                            loading="lazy"
                            onError={(e) => {
                              e.target.style.display = 'none';
                              e.target.nextElementSibling.style.display = 'flex';
                            }}
                          />
                          <div className="tms-no-poster" style={{ display: 'none' }}>
                            <svg className="tms-placeholder-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <rect width="48" height="48" rx="6" fill="#1a1a2e" stroke="#3a3a55" strokeWidth="1.5" />
                              <path d="M16 32V16l10 8-10 8z" fill="#6b6b80" />
                              <rect x="28" y="16" width="8" height="16" rx="1" fill="#6b6b80" />
                            </svg>
                            <span className="tms-placeholder-text">No Poster</span>
                          </div>
                        </div>
                        <div className="tms-details">
                          <h4
                            className="tms-title"
                            onClick={() => window.location.href = `/movie/${movie.id}`}
                          >
                            {movie.title}
                          </h4>
                          <span className="tms-meta">
                            {movie.language} • {movie.rating} • {movie.duration_min} min
                          </span>
                          <div className="tms-showtimes">
                            {Object.entries(byDate).slice(0, 3).map(([date, sts]) => (
                              <div key={date} className="tms-date-group">
                                <span className="tms-date">{date}</span>
                                <div className="tms-times">
                                  {sts.slice(0, 4).map(st => (
                                    <button
                                      key={st.id}
                                      className="tms-time-btn"
                                      onClick={() => window.location.href = `/book/${movie.id}`}
                                    >
                                      {formatShowtime(st.start_time)}
                                    </button>
                                  ))}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {SECTION_ORDER.map(section => {
        let sectionMovies;
        if (section.key === 'trending') {
          sectionMovies = filteredMovies.filter(m => m.trending > 0).sort((a, b) => b.trending - a.trending).slice(0, 6);
        } else if (section.filter) {
          sectionMovies = filteredMovies.filter(m => {
            return Object.entries(section.filter).every(([k, v]) => m[k] === v);
          });
        }
        if (!sectionMovies || sectionMovies.length === 0) return null;
        return (
          <div key={section.key} className="section-container animate-fade-in-up">
            <h2 className="section-title">{section.label}</h2>
            <div className="movies-grid">{sectionMovies.map(m => <MovieCard key={m.id} movie={m} />)}</div>
          </div>
        );
      })}
    </div>
  );
}
