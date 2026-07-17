import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchBooking } from '../api';
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
          {booking.theatre_location && (
            <div className="conf-row">
              <span className="conf-label">Location</span>
              <span className="conf-value">{booking.theatre_location}</span>
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
            <span className="conf-value total-price">₹{booking.total_amount.toFixed(0)}</span>
          </div>
        </div>

        <Link to="/" className="btn btn-primary btn-block">Back to Home</Link>
      </div>
    </div>
  );
}
