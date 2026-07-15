import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { fetchSeatMap, createBooking } from '../api';
import './BookPage.css';

export default function BookPage() {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const [seatMap, setSeatMap] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Booking form
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [bookingError, setBookingError] = useState(null);
  const [step, setStep] = useState(1); // 1 = seats, 2 = details

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchSeatMap(showtimeId);
        setSeatMap(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [showtimeId]);

  const toggleSeat = useCallback((seat) => {
    if (submitting) return;
    setSelectedSeats((prev) => {
      const next = new Set(prev);
      if (next.has(seat.id)) {
        next.delete(seat.id);
      } else {
        next.add(seat.id);
      }
      return next;
    });
  }, [submitting]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim()) {
      setBookingError('Name and email are required');
      return;
    }

    setSubmitting(true);
    setBookingError(null);

    try {
      const booking = await createBooking({
        showtime_id: parseInt(showtimeId),
        customer_name: name.trim(),
        customer_email: email.trim(),
        customer_phone: phone.trim() || undefined,
        seat_ids: Array.from(selectedSeats),
      });
      navigate(`/confirmation/${booking.booking_ref}`);
    } catch (err) {
      setBookingError(err.message);
      setSubmitting(false);
    }
  };

  if (loading) return <div className="loading">Loading seat map...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!seatMap) return <div className="error">Seat map not found</div>;

  // Build row/col grid
  const grid = [];
  for (let r = 0; r < seatMap.rows; r++) {
    const rowSeats = seatMap.seats.filter(
      (s) => s.row_label === String.fromCharCode(65 + r)
    );
    grid.push(rowSeats);
  }

  const totalPrice = selectedSeats.size * seatMap.price;

  return (
    <div className="book-page">
      <Link to="/" className="back-link">&larr; Back to Movies</Link>
      <h1 className="book-title">Book Tickets</h1>
      <p className="book-subtitle">
        {seatMap.screen_name} — ${seatMap.price.toFixed(2)} per seat
      </p>

      {/* Step indicators */}
      <div className="step-indicators">
        <div className={`step ${step >= 1 ? 'active' : ''}`}>1. Choose Seats</div>
        <div className="step-divider" />
        <div className={`step ${step >= 2 ? 'active' : ''}`}>2. Your Details</div>
      </div>

      {step === 1 && (
        <>
          {/* Screen indicator */}
          <div className="screen-indicator">
            <div className="screen-curve" />
            <span>SCREEN</span>
          </div>

          {/* Legend */}
          <div className="seat-legend">
            <div className="legend-item">
              <div className="seat-box available" />
              <span>Available</span>
            </div>
            <div className="legend-item">
              <div className="seat-box selected" />
              <span>Selected</span>
            </div>
            <div className="legend-item">
              <div className="seat-box booked" />
              <span>Booked</span>
            </div>
          </div>

          {/* Seat Grid */}
          <div className="seat-grid">
            {grid.map((row, ri) => (
              <div key={ri} className="seat-row">
                <span className="row-label">
                  {String.fromCharCode(65 + ri)}
                </span>
                <div className="seat-group">
                  {row.map((seat) => {
                    let className = 'seat';
                    if (seat.is_booked) className += ' booked';
                    else if (selectedSeats.has(seat.id)) className += ' selected';
                    else className += ' available';

                    return (
                      <button
                        key={seat.id}
                        className={className}
                        disabled={seat.is_booked}
                        onClick={() => toggleSeat(seat)}
                        title={`${seat.row_label}${seat.seat_number}`}
                      >
                        {seat.seat_number}
                      </button>
                    );
                  })}
                </div>
                <span className="row-label">
                  {String.fromCharCode(65 + ri)}
                </span>
              </div>
            ))}
          </div>

          {/* Summary and continue */}
          <div className="seat-summary">
            <div className="summary-info">
              <span>{selectedSeats.size} seat{selectedSeats.size !== 1 ? 's' : ''} selected</span>
              <span className="summary-price">${totalPrice.toFixed(2)}</span>
            </div>
            <button
              className="btn btn-primary"
              disabled={selectedSeats.size === 0}
              onClick={() => setStep(2)}
            >
              Continue to Details
            </button>
          </div>
        </>
      )}

      {step === 2 && (
        <>
          <div className="review-section">
            <h3>Your Selection</h3>
            <div className="review-card">
              <p><strong>Seats:</strong> {Array.from(selectedSeats).map((sid) => {
                const seat = seatMap.seats.find((s) => s.id === sid);
                return seat ? `${seat.row_label}${seat.seat_number}` : '';
              }).join(', ')}</p>
              <p><strong>Total:</strong> ${totalPrice.toFixed(2)}</p>
              <button className="btn btn-secondary" onClick={() => setStep(1)}>
                Change Seats
              </button>
            </div>
          </div>

          <form className="booking-form" onSubmit={handleSubmit}>
            <h3>Your Details</h3>
            {bookingError && <div className="error">{bookingError}</div>}

            <div className="form-group">
              <label htmlFor="name">Full Name *</label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email *</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="john@example.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="phone">Phone (optional)</label>
              <input
                id="phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="555-0100"
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={submitting}
            >
              {submitting ? 'Booking...' : `Confirm Booking — $${totalPrice.toFixed(2)}`}
            </button>
          </form>
        </>
      )}
    </div>
  );
}
