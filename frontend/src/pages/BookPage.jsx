import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { fetchSeatMap, createBooking } from '../api';
import { formatINR, getGoogleMapsUrl } from '../format';
import './BookPage.css';

export default function BookPage() {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const [seatMap, setSeatMap] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ customer_name: '', customer_email: '', customer_phone: '' });
  const [formError, setFormError] = useState(null);
  const [step, setStep] = useState('details');
  const [paymentMethod, setPaymentMethod] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);

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
    await new Promise(resolve => setTimeout(resolve, 2000));
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
    }
  };

  // Calculate total with tiered pricing
  const totalPrice = selectedSeats.reduce((sum, s) => {
    const multiplier = s.price_multiplier || 1.0;
    return sum + Math.round(seatMap.price * multiplier);
  }, 0);

  if (loading) return <div className="loading-container"><div className="loading-spinner" /><p>Loading seat map...</p></div>;
  if (error) return <div className="loading-container"><p className="error-text">{error}</p><Link to="/" className="btn btn-primary">Back to Home</Link></div>;
  if (!seatMap) return null;

  const { seats, sections, aisles, price, screen_name, theatre_name, theatre_location } = seatMap;

  // Group seats by row
  const rowMap = {};
  seats.forEach(s => {
    if (!rowMap[s.row_label]) rowMap[s.row_label] = [];
    rowMap[s.row_label].push(s);
  });

  const rowLabels = Object.keys(rowMap).sort();
  const maxSeatsPerRow = Math.max(...Object.values(rowMap).map(r => r.length));

  // Find section for a seat
  const getSection = (rowLabel) => {
    const rowIdx = rowLabels.indexOf(rowLabel);
    for (const sec of sections) {
      if (rowIdx >= sec.row_start && rowIdx <= sec.row_end) return sec;
    }
    return null;
  };

  // Check if a column index is an aisle
  const isAisle = (colNum) => aisles.includes(colNum);

  // Build a map of colNum -> max seat number per row for proper alignment
  const colMap = {};
  let actualCol = 0;
  for (let c = 1; c <= maxSeatsPerRow + aisles.length; c++) {
    if (isAisle(c)) {
      colMap[c] = -1; // aisle marker
    } else {
      actualCol++;
      colMap[c] = actualCol;
    }
  }

  const totalCols = maxSeatsPerRow + aisles.length;

  return (
    <div className="book-page">
      <h1 className="book-title">Select Your Seats</h1>
      <div className="book-meta">
        <span className="book-screen-name">{screen_name}</span>
        <span className="book-base-price">Base: {formatINR(price)}/seat</span>
      </div>

      {theatre_name && (
        <div className="book-theatre-info">
          <h3>{theatre_name}</h3>
          {theatre_location ? (
            <a
              className="book-theatre-location-link"
              href={getGoogleMapsUrl(theatre_name, theatre_location)}
              target="_blank" rel="noopener noreferrer"
              title="View on Google Maps"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
              </svg>
              {theatre_location}
            </a>
          ) : <p>Location unavailable</p>}
        </div>
      )}

      {/* Section legend with pricing */}
      {sections.length > 0 && (
        <div className="section-legend">
          {sections.map(sec => (
            <div key={sec.name} className="section-legend-item">
              <span className="section-dot" style={{ backgroundColor: sec.color }} />
              <span className="section-name">{sec.name}</span>
              <span className="section-price">{formatINR(Math.round(price * sec.price_multiplier))}</span>
            </div>
          ))}
        </div>
      )}

      {/* Zoom controls */}
      <div className="zoom-controls">
        <button className="zoom-btn" onClick={() => setZoomLevel(z => Math.max(0.6, z - 0.15))} title="Zoom out">−</button>
        <span className="zoom-label">{Math.round(zoomLevel * 100)}%</span>
        <button className="zoom-btn" onClick={() => setZoomLevel(z => Math.min(2.0, z + 0.15))} title="Zoom in">+</button>
      </div>

      {/* Screen indicator */}
      <div className="screen-indicator">
        <div className="screen-curve">{screen_name} — SCREEN THIS WAY</div>
      </div>

      {/* Seat grid with sections and aisles */}
      <div className="seat-grid-wrapper">
        <div className="seat-grid" style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'top center' }}>
          {rowLabels.map((row, rowIdx) => {
            const section = getSection(row);
            const isNewSection = rowIdx === 0 || getSection(rowLabels[rowIdx - 1])?.name !== section?.name;
            return (
              <div key={row}>
                {isNewSection && section && (
                  <div className="section-divider">
                    <span className="section-divider-line" />
                    <span className="section-divider-label" style={{ color: section.color, borderColor: section.color }}>
                      {section.name} — {formatINR(Math.round(price * section.price_multiplier))}
                    </span>
                    <span className="section-divider-line" />
                  </div>
                )}
                <div className="seat-row">
                  <span className="row-label">{row}</span>
                  <div className="seat-cells">
                    {Array.from({ length: totalCols }, (_, i) => {
                      const colNum = i + 1;
                      if (isAisle(colNum)) {
                        return <div key={`aisle-${row}-${colNum}`} className="seat-aisle" />;
                      }
                      const seatNum = colMap[colNum];
                      const seat = rowMap[row]?.find(s => s.seat_number === seatNum);
                      if (!seat) return <div key={`empty-${row}-${colNum}`} className="seat seat-empty" />;
                      const isSelected = selectedSeats.some(s => s.id === seat.id);
                      const seatSection = sections.find(s => {
                        const ri = rowLabels.indexOf(seat.row_label);
                        return ri >= s.row_start && ri <= s.row_end;
                      });
                      return (
                        <button
                          key={seat.id}
                          className={`seat ${seat.is_booked ? 'seat-booked' : ''} ${isSelected ? 'seat-selected' : ''} seat-section-${(seatSection?.name || 'Executive').toLowerCase()}`}
                          onClick={() => toggleSeat(seat)}
                          disabled={seat.is_booked}
                          title={`${seat.row_label}${seat.seat_number} - ${seat.section} - ${seat.is_booked ? 'BOOKED' : isSelected ? 'Selected' : formatINR(Math.round(price * (seat.price_multiplier || 1)))}`}
                        >
                          {seat.seat_number}
                        </button>
                      );
                    })}
                  </div>
                  <span className="row-label">{row}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="seat-legend">
        <span><span className="legend-dot available" /> Available</span>
        <span><span className="legend-dot selected-dot" /> Selected</span>
        <span><span className="legend-dot booked-dot" /> Booked</span>
        <span><span className="legend-dot aisle-dot" /> Aisle</span>
      </div>

      {/* Booking form */}
      <div className="booking-form-container">
        <h2>{step === 'payment' ? 'Choose Payment Method' : step === 'processing' ? 'Processing Payment...' : 'Complete Your Booking'}</h2>
        <div className="selected-summary">
          <span>{selectedSeats.length} seat(s): {selectedSeats.map(s => `${s.row_label}${s.seat_number}`).join(', ')}</span>
          {selectedSeats.length > 0 && <span className="total-amount">Total: {formatINR(totalPrice)}</span>}
        </div>

        {formError && <div className="form-error">{formError}</div>}

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
              Proceed to Pay — {formatINR(totalPrice)}
            </button>
          </form>
        )}

        {step === 'payment' && (
          <div className="payment-step">
            <p className="payment-instruction">Select a UPI payment method to complete your booking of {formatINR(totalPrice)}</p>
            <div className="payment-options">
              <button className={`payment-option${paymentMethod === 'phonepe' ? ' active' : ''}`} onClick={() => setPaymentMethod('phonepe')}>
                <span className="payment-icon">📱</span><span className="payment-name">PhonePe</span><span className="payment-upi">UPI: cinebook@phonepe</span>
              </button>
              <button className={`payment-option${paymentMethod === 'gpay' ? ' active' : ''}`} onClick={() => setPaymentMethod('gpay')}>
                <span className="payment-icon">💳</span><span className="payment-name">Google Pay</span><span className="payment-upi">UPI: cinebook@okhdfc</span>
              </button>
              <button className={`payment-option${paymentMethod === 'paytm' ? ' active' : ''}`} onClick={() => setPaymentMethod('paytm')}>
                <span className="payment-icon">💰</span><span className="payment-name">Paytm</span><span className="payment-upi">UPI: cinebook@paytm</span>
              </button>
            </div>
            <div className="payment-actions">
              <button className="btn btn-secondary" onClick={() => setStep('details')}>← Back</button>
              <button className="btn btn-primary btn-lg" disabled={!paymentMethod} onClick={handlePayNow}>
                Pay {formatINR(totalPrice)} with {paymentMethod === 'phonepe' ? 'PhonePe' : paymentMethod === 'gpay' ? 'GPay' : paymentMethod === 'paytm' ? 'Paytm' : 'UPI'}
              </button>
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="processing-step">
            <div className="loading-spinner" />
            <p>Processing your payment...</p>
            <p className="processing-hint">Please do not close this page</p>
          </div>
        )}
      </div>
    </div>
  );
}
