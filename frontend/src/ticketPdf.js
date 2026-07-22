import { jsPDF } from 'jspdf';
import { formatINRPdf } from './format';

/**
 * Generate and trigger download of a PDF ticket for a booking.
 * @param {object} booking - Booking object from the API
 */
export function downloadTicketPdf(booking) {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
  const pageW = 210;
  const margin = 15;
  const innerW = pageW - margin * 2;

  let y = 20;

  // ── Branding header ──
  doc.setFillColor(230, 57, 70); // #e63946
  doc.rect(0, 0, pageW, 30, 'F');
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(22);
  doc.setFont('helvetica', 'bold');
  doc.text('CINeBOOK', margin, 20);
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text('Movie Ticket Booking', margin, 27);

  y = 40;

  // ── Ticket title ──
  doc.setTextColor(230, 57, 70);
  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.text('E-TICKET', margin, y);
  y += 8;

  // Booking ref
  doc.setTextColor(100, 100, 100);
  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.text(`Booking Ref: ${booking.booking_ref}`, margin, y);
  y += 12;

  // ── Divider ──
  doc.setDrawColor(220, 220, 220);
  doc.line(margin, y, pageW - margin, y);
  y += 10;

  // ── Movie details ──
  doc.setTextColor(30, 30, 30);
  doc.setFontSize(18);
  doc.setFont('helvetica', 'bold');
  doc.text(truncateStr(booking.movie_title || 'Movie', 35), margin, y);
  y += 10;

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(80, 80, 80);

  const startTime = booking.start_time
    ? formatDateTime(new Date(booking.start_time + 'Z'))
    : 'N/A';

  addDetail(doc, 'Date & Time', startTime, margin, y, innerW);
  y += 7;
  addDetail(doc, 'Theatre', booking.theatre_name || 'N/A', margin, y, innerW);
  y += 7;
  addDetail(doc, 'Location', booking.theatre_location || 'N/A', margin, y, innerW);
  y += 7;
  addDetail(doc, 'Screen', booking.screen_name || 'N/A', margin, y, innerW);
  y += 7;
  addDetail(doc, 'Seats', booking.seats?.map(s => `${s.row_label}${s.seat_number}`).join(', ') || 'N/A', margin, y, innerW);
  y += 7;
  addDetail(doc, 'Customer', booking.customer_name || 'N/A', margin, y, innerW);
  if (booking.customer_email) {
    y += 7;
    addDetail(doc, 'Email', booking.customer_email, margin, y, innerW);
  }

  y += 6;

  // ── Divider ──
  doc.setDrawColor(220, 220, 220);
  doc.line(margin, y, pageW - margin, y);
  y += 8;

  // ── Amount ──
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(30, 30, 30);
  doc.text('Total Amount:', margin, y);
  doc.setTextColor(230, 57, 70);
  doc.setFontSize(18);
  const amountText = formatINRPdf(booking.total_amount);
  doc.text(amountText, pageW - margin - doc.getTextWidth(amountText), y);
  y += 12;

  // ── Divider ──
  doc.setDrawColor(220, 220, 220);
  doc.line(margin, y, pageW - margin, y);
  y += 10;

  // ── Barcode / QR-like booking ref ──
  doc.setFillColor(245, 245, 245);
  doc.roundedRect(margin, y, innerW, 18, 3, 3, 'F');
  doc.setTextColor(60, 60, 60);
  doc.setFontSize(14);
  doc.setFont('courier', 'bold');
  doc.text(booking.booking_ref || '', pageW / 2, y + 12, { align: 'center' });
  y += 25;

  // ── Footer ──
  doc.setTextColor(160, 160, 160);
  doc.setFontSize(8);
  doc.setFont('helvetica', 'normal');
  doc.text('This is an electronically generated ticket. Show this at the theatre entrance.', pageW / 2, y, { align: 'center' });
  y += 5;
  doc.text(`Booked on: ${formatDateTime(new Date(booking.created_at + 'Z'))}`, pageW / 2, y, { align: 'center' });
  y += 5;
  doc.text('CineBook - www.cinebook.com', pageW / 2, y, { align: 'center' });

  // ── Save ──
  const filename = `CineBook_Ticket_${booking.booking_ref}.pdf`;
  doc.save(filename);
}

function addDetail(doc, label, value, x, y, innerW) {
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(60, 60, 60);
  doc.setFontSize(10);
  doc.text(label, x, y);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(30, 30, 30);
  doc.text(String(value), x + 35, y, { maxWidth: innerW - 35 });
}

function formatDateTime(date) {
  if (isNaN(date.getTime())) return String(date);
  return date.toLocaleString('en-IN', {
    weekday: 'short', day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: true,
  });
}

function truncateStr(str, maxLen) {
  return str.length > maxLen ? str.substring(0, maxLen - 1) + '\u2026' : str;
}
