import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchBooking } from '../api';
import { downloadTicketPdf } from '../ticketPdf';
import { formatINR, getGoogleMapsUrl } from '../format';
import './Confirmation.css';

export default function Confirmation() {
  const { ref } = useParams();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBooking(ref).then(setBooking).catch(() => {}).finally(() => setLoading(false));
  }, [ref]);

  if (loading) return <div className="loading-container"><div className="loading-spinner" /><p>Loading booking...</p></div>;
  if (!booking) return <div className="loading-container"><p>Booking not found.</p><Link to="/" className="btn btn-primary">Back to Home</Link></div>;

  const formatTime = (dt) => dt ? new Date(dt + 'Z').toLocaleString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit', hour12: true }) : '';

  return (
    <div className="confirmation-page">
      <div className="confirmation-card animate-fade-in-up">
        <div className="confirmation-check">✅</div>
        <h1>Booking Confirmed!</h1>
        <p className="confirmation-ref">Reference: <strong>{booking.booking_ref}</strong></p>

        <div className="confirmation-details">
          <div className="conf-row">
            <span className="conf-label">Movie</span>
            <span className="conf-value">{booking.movie_title}</span>
          </div>
          {booking.theatre_name && (
            <div className="conf-row">
              <span className="conf-label">Theatre</span>
              <span className="conf-value">{booking.theatre_name}</span>
            </div>
          )}
          {booking.theatre_location ? (
            <div className="conf-row">
              <span className="conf-label">Location</span>
              <a
                className="conf-value conf-location-link"
                href={getGoogleMapsUrl(booking.theatre_name, booking.theatre_location)}
                target="_blank"
                rel="noopener noreferrer"
                title="View on Google Maps"
              >
                <svg className="conf-location-pin" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                {booking.theatre_location}
                <svg className="conf-location-external" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15 3 21 3 21 9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
              </a>
            </div>
          ) : (
            <div className="conf-row">
              <span className="conf-label">Location</span>
              <span className="conf-value conf-location-unavailable">Not available</span>
            </div>
          )}
          <div className="conf-row">
            <span className="conf-label">Screen</span>
            <span className="conf-value">{booking.screen_name}</span>
          </div>
          <div className="conf-row">
            <span className="conf-label">Showtime</span>
            <span className="conf-value">{formatTime(booking.start_time)}</span>
          </div>
          <div className="conf-row">
            <span className="conf-label">Seats</span>
            <span className="conf-value">{booking.seats?.map(s => `${s.row_label}${s.seat_number}`).join(', ')}</span>
          </div>
          <div className="conf-row">
            <span className="conf-label">Name</span>
            <span className="conf-value">{booking.customer_name}</span>
          </div>
          <div className="conf-row conf-total">
            <span className="conf-label">Total Amount</span>
            <span className="conf-value total-price">{formatINR(booking.total_amount)}</span>
          </div>
        </div>

        <div className="confirmation-actions">
          <button className="btn btn-download" onClick={() => downloadTicketPdf(booking)}>
            📥 Download Ticket (PDF)
          </button>
          <Link to="/" className="btn btn-primary btn-block">Back to Home</Link>
        </div>
      </div>
    </div>
  );
}
