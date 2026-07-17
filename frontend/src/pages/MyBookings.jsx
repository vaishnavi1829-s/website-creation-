import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { fetchMyBookings, isLoggedIn } from '../api';
import { downloadTicketPdf } from '../ticketPdf';
import './MyBookings.css';

export default function MyBookings() {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate('/login');
      return;
    }

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchMyBookings();
        setBookings(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [navigate]);

  if (loading) return <div className="loading">Loading your bookings...</div>;
  if (error) {
    return (
      <div className="my-bookings-page">
        <div className="error-state">
          <span className="error-icon">🔒</span>
          <h2>{error}</h2>
          <Link to="/login" className="btn btn-primary">Go to Login</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="my-bookings-page">
      <div className="my-bookings-header">
        <h1>My Bookings</h1>
        <p>All your ticket bookings in one place</p>
      </div>

      {bookings.length === 0 ? (
        <div className="empty-state">
          <span className="empty-icon">🎟️</span>
          <h2>No bookings yet</h2>
          <p>Book your first movie ticket and it will appear here!</p>
          <Link to="/" className="btn btn-primary">Browse Movies</Link>
        </div>
      ) : (
        <div className="bookings-list">
          {bookings.map((booking) => {
            const startTime = new Date(booking.start_time);
            const createdDate = new Date(booking.created_at);
            return (
              <div key={booking.id} className="booking-card">
                <div className="booking-card-left">
                  <div className="booking-ref">#{booking.booking_ref}</div>
                  <h3 className="booking-movie">{booking.movie_title}</h3>
                  <div className="booking-meta">
                    <span>{startTime.toLocaleDateString('en-US', {
                      weekday: 'short', month: 'short', day: 'numeric',
                    })}</span>
                    <span className="meta-sep">•</span>
                    <span>{startTime.toLocaleTimeString('en-US', {
                      hour: '2-digit', minute: '2-digit',
                    })}</span>
                    <span className="meta-sep">•</span>
                    <span>{booking.screen_name}</span>
                  </div>
                  <div className="booking-seats">
                    Seats: {booking.seats.map((s) => `${s.row_label}${s.seat_number}`).join(', ')}
                  </div>
                </div>
                <div className="booking-card-right">
                  <div className="booking-amount">${booking.total_amount.toFixed(2)}</div>
                  <div className="booking-date">
                    Booked {createdDate.toLocaleDateString()}
                  </div>
                  <Link to={`/confirmation/${booking.booking_ref}`} className="btn btn-small btn-secondary">
                    View Ticket
                  </Link>
                  <button className="btn btn-small btn-download" onClick={() => downloadTicketPdf(booking)}>
                    📥 PDF
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
