import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Navbar.css';

export default function Navbar({ search, onSearch, filters, onFilterChange, genres, languages }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [filterOpen, setFilterOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🎬</span>
          <span className="brand-text">CineBook</span>
        </Link>

        <div className="navbar-search">
          <div className="search-wrapper">
            <input
              type="text"
              className="search-input"
              placeholder="Search movies by title..."
              value={search}
              onChange={(e) => onSearch(e.target.value)}
            />
            <button
              className="filter-toggle"
              onClick={() => setFilterOpen(!filterOpen)}
              title="Filters"
            >
              ⚙ Filters
            </button>
          </div>
        </div>

        <div className="navbar-actions">
          <Link to="/" className="nav-link">Home</Link>
          <button className="mobile-toggle" onClick={() => setMobileOpen(!mobileOpen)}>
            {mobileOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>

      {/* Filter panel */}
      {filterOpen && (
        <div className="filter-panel animate-fade-in">
          <div className="filter-grid">
            <div className="filter-group">
              <label>Genre</label>
              <select
                value={filters.genre || ''}
                onChange={(e) => onFilterChange('genre', e.target.value || null)}
              >
                <option value="">All Genres</option>
                {genres.map(g => <option key={g} value={g}>{g}</option>)}
              </select>
            </div>
            <div className="filter-group">
              <label>Language</label>
              <select
                value={filters.language || ''}
                onChange={(e) => onFilterChange('language', e.target.value || null)}
              >
                <option value="">All Languages</option>
                {languages.map(l => <option key={l} value={l}>{l}</option>)}
              </select>
            </div>
            <div className="filter-group">
              <label>Rating</label>
              <select
                value={filters.rating || ''}
                onChange={(e) => onFilterChange('rating', e.target.value || null)}
              >
                <option value="">All Ratings</option>
                <option value="U">U</option>
                <option value="UA">UA</option>
                <option value="A">A</option>
              </select>
            </div>
            <div className="filter-group">
              <label>Release Year</label>
              <select
                value={filters.release_year || ''}
                onChange={(e) => onFilterChange('release_year', e.target.value ? parseInt(e.target.value) : null)}
              >
                <option value="">All Years</option>
                {[2025,2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2010,1997].map(y => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
            </div>
          </div>
          <button
            className="btn btn-secondary filter-clear"
            onClick={() => {
              onFilterChange('genre', null);
              onFilterChange('language', null);
              onFilterChange('rating', null);
              onFilterChange('release_year', null);
            }}
          >
            Clear All Filters
          </button>
        </div>
      )}
    </nav>
  );
}
