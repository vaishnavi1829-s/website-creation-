const API_BASE = '/api';

export async function fetchMovies(search = '', genre = '') {
  const params = new URLSearchParams();
  if (search) params.set('search', search);
  if (genre) params.set('genre', genre);
  const res = await fetch(`${API_BASE}/movies?${params}`);
  if (!res.ok) throw new Error('Failed to fetch movies');
  return res.json();
}

export async function fetchMovie(id) {
  const res = await fetch(`${API_BASE}/movies/${id}`);
  if (!res.ok) throw new Error('Movie not found');
  return res.json();
}

export async function fetchShowtimes(movieId = null, date = null) {
  const params = new URLSearchParams();
  if (movieId) params.set('movie_id', movieId);
  if (date) params.set('date', date);
  const res = await fetch(`${API_BASE}/showtimes?${params}`);
  if (!res.ok) throw new Error('Failed to fetch showtimes');
  return res.json();
}

export async function fetchSeatMap(showtimeId) {
  const res = await fetch(`${API_BASE}/showtimes/${showtimeId}/seats`);
  if (!res.ok) throw new Error('Failed to fetch seat map');
  return res.json();
}

export async function createBooking(bookingData) {
  const res = await fetch(`${API_BASE}/bookings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookingData),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Booking failed');
  }
  return res.json();
}

export async function fetchBooking(ref) {
  const res = await fetch(`${API_BASE}/bookings/${ref}`);
  if (!res.ok) throw new Error('Booking not found');
  return res.json();
}
