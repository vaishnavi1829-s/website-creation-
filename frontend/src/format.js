/**
 * Format a number as Indian Rupee (INR) with comma separators.
 * Examples: 1440 → "₹1,440", 125000 → "₹1,25,000"
 *
 * @param {number} amount - The numeric amount to format
 * @returns {string} Formatted string like "₹1,440"
 */
export function formatINR(amount) {
  const num = typeof amount === 'number' ? amount : parseFloat(amount);
  if (isNaN(num)) return '₹0';
  return '₹' + new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0,
  }).format(num);
}

/**
 * PDF-safe currency format.
 * jsPDF's built-in Helvetica font does NOT support the ₹ symbol (U+20B9),
 * so this falls back to "Rs." prefix when useSymbol is false.
 *
 * @param {number} amount - The numeric amount to format
 * @param {boolean} useSymbol - If true uses ₹, if false uses Rs. (default: true)
 * @returns {string} Formatted string like "₹1,440" or "Rs. 1,440"
 */
export function formatINRPdf(amount) {
  const num = typeof amount === 'number' ? amount : parseFloat(amount);
  if (isNaN(num)) return 'Rs. 0';
  const formatted = new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: 0,
  }).format(num);
  // jsPDF's helvetica (WinAnsiEncoding) lacks the ₹ glyph, so use "Rs." for PDF
  return `Rs. ${formatted}`;
}

/**
 * Generate a Google Maps URL for a theatre name + location.
 * Opens in Google Maps app on mobile, website on desktop.
 *
 * @param {string} theatreName - Theatre name
 * @param {string} location - Theatre address/location string
 * @returns {string} Google Maps search URL
 */
export function getGoogleMapsUrl(theatreName, location) {
  const query = encodeURIComponent(`${theatreName}, ${location}`);
  return `https://www.google.com/maps/search/?api=1&query=${query}`;
}
