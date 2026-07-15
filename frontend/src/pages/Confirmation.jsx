import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchBooking } from '../api';
import './Confirmation.css';

export default function Confirmation() {
  const { ref } = useParams();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchBooking(ref);
        setBooking(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [ref]);

  if (loading) return <div className="loading">Loading booking...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!booking) return <div className="error">Booking not found</div>;

  const startTime = new Date(booking.start_time);

  return (
    <div className="confirmation">
      <div className="conf-header">
        <div className="conf-success">&#10003; Booking Confirmed!</div>
        <p className="conf-ref">Reference: <strong>{booking.booking_ref}</strong></p>
      </div>

      <div className="ticket">
        <div className="ticket-header">
          <h2>{booking.movie_title}</h2>
        </div>

        <div className="ticket-body">
          <div className="ticket-row">
            <span className="ticket-label">Screen</span>
            <span className="ticket-value">{booking.screen_name}</span>
          </div>
          <div className="ticket-row">
            <span className="ticket-label">Date</span>
            <span className="ticket-value">{startTime.toLocaleDateString('en-US', {
              weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
            })}</span>
          </div>
          <div className="ticket-row">
            <span className="ticket-label">Time</span>
            <span className="ticket-value">{startTime.toLocaleTimeString('en-US', {
              hour: '2-digit', minute: '2-digit',
            })}</span>
          </div>
          <div className="ticket-row">
            <span className="ticket-label">Seats</span>
            <span className="ticket-value">
              {booking.seats.map((s) => `${s.row_label}${s.seat_number}`).join(', ')}
            </span>
          </div>
          <div className="ticket-row">
            <span className="ticket-label">Customer</span>
            <span className="ticket-value">{booking.customer_name}</span>
          </div>
          <div className="ticket-row total-row">
            <span className="ticket-label">Total Paid</span>
            <span className="ticket-total">${booking.total_amount.toFixed(2)}</span>
          </div>
        </div>

        <div className="ticket-footer">
          <p>Booked on {new Date(booking.created_at).toLocaleString()}</p>
          <p className="ticket-email">Confirmation sent to {booking.customer_email}</p>
        </div>
      </div>

      <div className="conf-actions">
        <Link to="/" className="btn btn-primary">Book More Movies</Link>
      </div>
    </div>
  );
}
