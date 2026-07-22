import { useState, useEffect, useMemo } from 'react';
import { fetchEvents } from '../api';
import EventCard from '../components/EventCard';
import '../components/EventCard.css';

const CATEGORY = 'music';

export default function MusicShows() {
  const [events, setEvents] = useState([]);
  const [cities, setCities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [city, setCity] = useState('');
  const [language, setLanguage] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  useEffect(() => {
    setLoading(true);
    fetchEvents(CATEGORY)
      .then(data => {
        setEvents(data.events || []);
        setCities(data.cities || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filteredEvents = useMemo(() => {
    let list = events;
    if (search) {
      const s = search.toLowerCase();
      list = list.filter(e =>
        e.title.toLowerCase().includes(s) ||
        (e.artist_name && e.artist_name.toLowerCase().includes(s)) ||
        (e.venue && e.venue.toLowerCase().includes(s)) ||
        (e.description && e.description.toLowerCase().includes(s))
      );
    }
    if (city) {
      list = list.filter(e => e.city && e.city.toLowerCase().includes(city.toLowerCase()));
    }
    if (language) {
      list = list.filter(e => e.language && e.language.toLowerCase().includes(language.toLowerCase()));
    }
    if (minPrice) {
      list = list.filter(e => e.price >= parseFloat(minPrice));
    }
    if (maxPrice) {
      list = list.filter(e => e.price <= parseFloat(maxPrice));
    }
    return list;
  }, [events, search, city, language, minPrice, maxPrice]);

  const clearFilters = () => {
    setSearch('');
    setCity('');
    setLanguage('');
    setMinPrice('');
    setMaxPrice('');
  };

  const hasFilters = search || city || language || minPrice || maxPrice;

  if (loading) {
    return (
      <div className="events-loading">
        <div className="loading-spinner" />
        <p>Loading music events...</p>
      </div>
    );
  }

  const featured = [...events].sort((a, b) => b.trending - a.trending).slice(0, 2);

  return (
    <div className="music-shows-page">
      {/* Hero Banner */}
      <div className="event-banner event-banner-music">
        <div className="event-banner-content animate-fade-in">
          <h1>🎵 Music Shows</h1>
          <p>From classical concerts to EDM festivals — discover live music experiences that move your soul</p>
        </div>
        <div className="event-banner-overlay" />
      </div>

      <div className="events-section">
        {/* Featured Highlights */}
        {!hasFilters && featured.length > 0 && (
          <div className="event-highlights animate-fade-in-up">
            {featured.map(e => (
              <div key={e.id} className="event-highlight-card">
                <img src={e.image_url || ''} alt={e.title} loading="lazy" onError={(ev) => { ev.target.style.display = 'none'; }} />
                <div className="event-highlight-overlay">
                  <h3>{e.title}</h3>
                  <p>{e.artist_name} • {e.venue} • ₹{e.price.toLocaleString('en-IN')}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Filters */}
        <div className="event-filters animate-fade-in-up">
          <div className="event-filter-group" style={{ flex: 2, minWidth: 200 }}>
            <label>Search Artists & Events</label>
            <input
              type="text"
              placeholder="Search by artist, event name, venue..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="event-filter-group">
            <label>City</label>
            <select value={city} onChange={(e) => setCity(e.target.value)}>
              <option value="">All Cities</option>
              {cities.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="event-filter-group">
            <label>Language</label>
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              <option value="">All Languages</option>
              <option value="English">English</option>
              <option value="Tamil">Tamil</option>
              <option value="Hindi">Hindi</option>
            </select>
          </div>
          <div className="event-filter-group">
            <label>Min Price (₹)</label>
            <input type="number" placeholder="Min" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} />
          </div>
          <div className="event-filter-group">
            <label>Max Price (₹)</label>
            <input type="number" placeholder="Max" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
          </div>
          {hasFilters && (
            <button className="btn btn-secondary event-filter-clear" onClick={clearFilters}>
              Clear Filters
            </button>
          )}
        </div>

        {/* Results */}
        <h2 className="events-section-title">
          {hasFilters ? `Search Results (${filteredEvents.length})` : '🎶 All Music Events'}
        </h2>

        {filteredEvents.length === 0 ? (
          <div className="event-empty">
            <span className="event-empty-icon">🎧</span>
            <h3>No music events found</h3>
            <p>Try adjusting your search or filters to find the perfect music experience!</p>
          </div>
        ) : (
          <div className="events-grid">
            {filteredEvents.map(e => <EventCard key={e.id} event={e} />)}
          </div>
        )}
      </div>
    </div>
  );
}
