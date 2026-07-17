import { useState, useEffect, useMemo } from 'react';
import { fetchMovies } from '../api';
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

  useEffect(() => {
    setLoading(true);
    fetchMovies().then(data => { setAllMovies(data.movies || []); setLoading(false); }).catch(() => setLoading(false));
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
