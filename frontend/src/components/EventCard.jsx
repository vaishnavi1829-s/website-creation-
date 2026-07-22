import { useState } from 'react';
import './EventCard.css';

export default function EventCard({ event }) {
  const { id, title, description, category, artist_name, venue, city, event_date, event_time, price, language, age_recommendation, rating } = event;
  const [imgError, setImgError] = useState(false);

  // Use backend event poster endpoint for professional category-themed SVG posters
  const posterUrl = `/api/events/poster/${id}`;

  const formatDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
  };

  const categoryColors = {
    kids: { gradient: 'linear-gradient(135deg, #ff6b6b, #ffa502, #ff6348)', icon: '🧒', badge: 'Kids Zone' },
    music: { gradient: 'linear-gradient(135deg, #a855f7, #7c3aed, #6366f1)', icon: '🎵', badge: 'Music Show' },
    comedy: { gradient: 'linear-gradient(135deg, #f59e0b, #f97316, #ef4444)', icon: '😂', badge: 'Comedy Show' },
  };

  const theme = categoryColors[category] || categoryColors.kids;

  return (
    <div className="event-card">
      {/* Image Section — uses SVG poster from backend; fallback is hidden by default */}
      <div className="event-card-image">
        {!imgError ? (
          <img
            src={posterUrl}
            alt={title}
            loading="lazy"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="event-image-fallback" style={{ background: theme.gradient }}>
            <span className="event-placeholder-icon">{theme.icon}</span>
            <span className="event-placeholder-text">{title}</span>
          </div>
        )}

        {/* Category Badge */}
        <div className="event-category-badge" style={{ background: theme.gradient }}>
          {theme.icon} {theme.badge}
        </div>

        {/* Rating Badge for music/comedy */}
        {rating > 0 && (
          <div className="event-rating-badge">
            <span className="event-star">★</span>
            {rating}
          </div>
        )}
      </div>

      {/* Details Section */}
      <div className="event-card-details">
        <h3 className="event-card-title">{title}</h3>

        {artist_name && (
          <p className="event-card-artist">
            <span className="event-artist-icon">{category === 'comedy' ? '🎤' : '🎭'}</span>
            {artist_name}
          </p>
        )}

        <p className="event-card-desc">{description?.slice(0, 100)}...</p>

        <div className="event-card-info">
          <div className="event-info-row">
            <span className="event-info-label">📍</span>
            <span className="event-info-value">{venue}, {city}</span>
          </div>
          <div className="event-info-row">
            <span className="event-info-label">📅</span>
            <span className="event-info-value">{formatDate(event_date)} • {event_time}</span>
          </div>
          {language && (
            <div className="event-info-row">
              <span className="event-info-label">🗣️</span>
              <span className="event-info-value">{language}</span>
            </div>
          )}
        </div>

        {category === 'kids' && age_recommendation && (
          <div className="event-age-badge" title="Age Recommendation">
            👶 Ages {age_recommendation}
          </div>
        )}

        <div className="event-card-footer">
          <span className="event-price">₹{price.toLocaleString('en-IN')}</span>
          <button className="btn btn-primary event-book-btn">Book Now</button>
        </div>
      </div>
    </div>
  );
}
