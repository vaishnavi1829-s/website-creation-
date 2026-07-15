import { useState, useEffect, useCallback } from 'react';
import { fetchMovies } from '../api';
import MovieCard from '../components/MovieCard';
import './Home.css';

export default function Home() {
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadMovies = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchMovies(search, selectedGenre);
      setMovies(data.movies);
      setGenres(data.genres);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [search, selectedGenre]);

  useEffect(() => {
    const debounce = setTimeout(loadMovies, 300);
    return () => clearTimeout(debounce);
  }, [loadMovies]);

  return (
    <div className="home">
      <div className="home-hero">
        <h1>Now Showing</h1>
        <p>Discover and book the latest blockbusters</p>
      </div>

      <div className="home-filters">
        <input
          type="text"
          className="search-input"
          placeholder="Search movies..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="genre-select"
          value={selectedGenre}
          onChange={(e) => setSelectedGenre(e.target.value)}
        >
          <option value="">All Genres</option>
          {genres.map((g) => (
            <option key={g} value={g}>{g}</option>
          ))}
        </select>
      </div>

      {loading && <div className="loading">Loading movies...</div>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && movies.length === 0 && (
        <div className="empty-state">
          <p>No movies found. Try a different search or genre.</p>
        </div>
      )}

      <div className="movie-grid">
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
}
