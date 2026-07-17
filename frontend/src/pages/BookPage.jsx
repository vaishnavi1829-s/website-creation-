import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { fetchSeatMap, createBooking } from '../api';
import './BookPage.css';

export default function BookPage() {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const [seatMap, setSeatMap] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [booking, setBooking] = useState(false);
  const [form, setForm] = useState({ customer_name: '', customer_email: '', customer_phone: '' });
  const [formError, setFormError] = useState(null);
  const [step, setStep] = useState('details'); // 'details' | 'payment' | 'processing'
  const [paymentMethod, setPaymentMethod] = useState(null); // 'phonepe' | 'gpay' | 'paytm'

  useEffect(() => {
    setLoading(true);
    fetchSeatMap(showtimeId).then(data => {
      setSeatMap(data);
      setLoading(false);
    }).catch(err => { setError(err.message); setLoading(false); });
  }, [showtimeId]);

  const toggleSeat = (seat) => {
    if (seat.is_booked) return;
    setSelectedSeats(prev => {
      const exists = prev.find(s => s.id === seat.id);
      if (exists) return prev.filter(s => s.id !== seat.id);
      return [...prev, seat];
    });
  };

  const handleProceedToPayment = (e) => {
    e.preventDefault();
    setFormError(null);
    if (selectedSeats.length === 0) { setFormError('Please select at least one seat.'); return; }
    if (!form.customer_name.trim()) { setFormError('Please enter your name.'); return; }
    if (!form.customer_email.trim()) { setFormError('Please enter your email.'); return; }
    setStep('payment');
  };

  const handlePayNow = async () => {
    if (!paymentMethod) return;
    setStep('processing');

    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    setBooking(true);
    try {
      const result = await createBooking({
        showtime_id: parseInt(showtimeId),
        customer_name: form.customer_name.trim(),
        customer_email: form.customer_email.trim(),
        customer_phone: form.customer_phone.trim() || undefined,
        seat_ids: selectedSeats.map(s => s.id),
        payment_method: paymentMethod,
      });
      navigate(`/confirmation/${result.booking_ref}`);
    } catch (err) {
      setFormError(err.message);
      setStep('payment');
    } finally {
      setBooking(false);
    }
  };

  if (loading) return <div className="loading-container"><div className="loading-spinner" /><p>Loading seat map...</p></div>;
  if (error) return <div className="loading-container"><p className="error-text">{error}</p><Link to="/" className="btn btn-primary">Back to Home</Link></div>;
  if (!seatMap) return null;

  const rowLabels = [...new Set(seatMap.seats.map(s => s.row_label))].sort();
  const cols = seatMap.cols;
  const totalPrice = selectedSeats.length * seatMap.price;

  return (
    <div className="book-page">
      <h1 className="book-title">Select Your Seats</h1>
      <div className="book-meta">
        <span className="book-screen-name">{seatMap.screen_name}</span>
        <span className="book-price-tag">₹{seatMap.price.toFixed(0)} / seat</span>
      </div>
      {seatMap.theatre_name && (
        <div className="book-theatre-info">
          <h3>{seatMap.theatre_name}</h3>
          <p>{seatMap.theatre_location}</p>
        </div>
      )}

      {/* Screen indicator */}
      <div className="screen-indicator">
        <div className="screen-curve">SCREEN</div>
      </div>

      {/* Seat grid */}
      <div className="seat-grid">
        {rowLabels.map(row => (
          <div key={row} className="seat-row">
            <span className="row-label">{row}</span>
            <div className="seat-cells">
              {Array.from({ length: cols }, (_, i) => {
                const seat = seatMap.seats.find(s => s.row_label === row && s.seat_number === i + 1);
                if (!seat) return <div key={`empty-${row}-${i}`} className="seat empty" />;
                const isSelected = selectedSeats.some(s => s.id === seat.id);
                return (
                  <button
                    key={seat.id}
                    className={`seat ${seat.is_booked ? 'booked' : ''} ${isSelected ? 'selected' : ''}`}
                    onClick={() => toggleSeat(seat)}
                    disabled={seat.is_booked}
                    title={`${row}${i+1} - ${seat.is_booked ? 'Booked' : isSelected ? 'Selected' : 'Available'}`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>
            <span className="row-label">{row}</span>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="seat-legend">
        <span><span className="legend-dot available" /> Available</span>
        <span><span className="legend-dot selected" /> Selected</span>
        <span><span className="legend-dot booked" /> Booked</span>
      </div>

      {/* Booking form */}
      <div className="booking-form-container">
        <h2>{step === 'payment' ? 'Choose Payment Method' : step === 'processing' ? 'Processing Payment...' : 'Complete Your Booking'}</h2>
        <div className="selected-summary">
          <span>{selectedSeats.length} seat(s) selected: {selectedSeats.map(s => `${s.row_label}${s.seat_number}`).join(', ')}</span>
          {selectedSeats.length > 0 && <span className="total-amount">Total: ₹{totalPrice.toFixed(0)}</span>}
        </div>

        {formError && <div className="form-error">{formError}</div>}

        {/* STEP 1: Customer Details */}
        {step === 'details' && (
          <form className="booking-form" onSubmit={handleProceedToPayment}>
            <div className="form-row">
              <div className="form-group">
                <label>Your Name *</label>
                <input type="text" value={form.customer_name} onChange={e => setForm({...form, customer_name: e.target.value})} placeholder="Enter your name" required />
              </div>
              <div className="form-group">
                <label>Email *</label>
                <input type="email" value={form.customer_email} onChange={e => setForm({...form, customer_email: e.target.value})} placeholder="you@example.com" required />
              </div>
              <div className="form-group">
                <label>Phone (optional)</label>
                <input type="tel" value={form.customer_phone} onChange={e => setForm({...form, customer_phone: e.target.value})} placeholder="+91 98765 43210" />
              </div>
            </div>
            <button type="submit" className="btn btn-primary btn-block btn-lg" disabled={selectedSeats.length === 0}>
              Proceed to Pay — ₹{totalPrice.toFixed(0)}
            </button>
          </form>
        )}

        {/* STEP 2: Payment Selection */}
        {step === 'payment' && (
          <div className="payment-step">
            <p className="payment-instruction">Select a UPI payment method to complete your booking of ₹{totalPrice.toFixed(0)}</p>

            <div className="payment-options">
              <button
                className={`payment-option${paymentMethod === 'phonepe' ? ' active' : ''}`}
                onClick={() => setPaymentMethod('phonepe')}
              >
                <span className="payment-icon">📱</span>
                <span className="payment-name">PhonePe</span>
                <span className="payment-upi">UPI ID: cinebook@phonepe</span>
              </button>

              <button
                className={`payment-option${paymentMethod === 'gpay' ? ' active' : ''}`}
                onClick={() => setPaymentMethod('gpay')}
              >
                <span className="payment-icon">💳</span>
                <span className="payment-name">Google Pay</span>
                <span className="payment-upi">UPI ID: cinebook@okhdfc</span>
              </button>

              <button
                className={`payment-option${paymentMethod === 'paytm' ? ' active' : ''}`}
                onClick={() => setPaymentMethod('paytm')}
              >
                <span className="payment-icon">💰</span>
                <span className="payment-name">Paytm</span>
                <span className="payment-upi">UPI ID: cinebook@paytm</span>
              </button>
            </div>

            <div className="payment-actions">
              <button className="btn btn-secondary" onClick={() => setStep('details')}>
                ← Back
              </button>
              <button
                className="btn btn-primary btn-lg"
                disabled={!paymentMethod}
                onClick={handlePayNow}
              >
                Pay ₹{totalPrice.toFixed(0)} with {paymentMethod === 'phonepe' ? 'PhonePe' : paymentMethod === 'gpay' ? 'GPay' : paymentMethod === 'paytm' ? 'Paytm' : 'UPI'}
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: Processing */}
        {step === 'processing' && (
          <div className="processing-step">
            <div className="loading-spinner" />
            <p>Processing your payment via {paymentMethod === 'phonepe' ? 'PhonePe' : paymentMethod === 'gpay' ? 'Google Pay' : 'Paytm'}...</p>
            <p className="processing-hint">Please do not close this page</p>
          </div>
        )}
      </div>
    </div>
  );
}
