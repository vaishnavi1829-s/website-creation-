const API_BASE = '/api';
const AUTH_BASE = `${API_BASE}/auth`;

// Helper: get stored token
export function getToken() {
  return localStorage.getItem('token');
}

// Helper: set token
export function setToken(token) {
  localStorage.setItem('token', token);
}

// Helper: remove token
export function clearToken() {
  localStorage.removeItem('token');
}

// Helper: attach auth header
function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// --- Movies ---
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

export async function fetchNowShowingMovies(days = 7) {
  const res = await fetch(`${API_BASE}/movies/now-showing?days=${days}`);
  if (!res.ok) throw new Error('Failed to fetch now showing movies');
  return res.json();
}

// --- Theatres ---
export async function fetchTheatres() {
  const res = await fetch(`${API_BASE}/theatres`);
  if (!res.ok) throw new Error('Failed to fetch theatres');
  return res.json();
}

// --- Showtimes ---
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

// --- Bookings ---
export async function createBooking(bookingData) {
  const res = await fetch(`${API_BASE}/bookings`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
    },
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

export async function fetchMyBookings() {
  const res = await fetch(`${API_BASE}/bookings/mine`, {
    headers: authHeaders(),
  });
  if (!res.ok) {
    if (res.status === 401) throw new Error('Please log in to view your bookings');
    throw new Error('Failed to fetch your bookings');
  }
  return res.json();
}

// --- Auth ---
export async function register(data) {
  const res = await fetch(`${AUTH_BASE}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Registration failed');
  }
  return res.json();
}

export async function login(data) {
  const res = await fetch(`${AUTH_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Login failed');
  }
  const result = await res.json();
  setToken(result.access_token);
  return result;
}

export async function forgotPassword(email) {
  const res = await fetch(`${AUTH_BASE}/forgot-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export async function resetPassword(token, newPassword) {
  const res = await fetch(`${AUTH_BASE}/reset-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token, new_password: newPassword }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Reset failed');
  }
  return res.json();
}

export function logout() {
  clearToken();
}

export async function fetchMe() {
  const res = await fetch(`${AUTH_BASE}/me`, {
    headers: authHeaders(),
  });
  if (!res.ok) return null;
  return res.json();
}

export function isLoggedIn() {
  return !!getToken();
}

// --- Events (Kids Zone, Music Shows, Comedy Shows) ---
export async function fetchEvents(category = '', search = '', city = '', language = '', minPrice = null, maxPrice = null) {
  const params = new URLSearchParams();
  if (category) params.set('category', category);
  if (search) params.set('search', search);
  if (city) params.set('city', city);
  if (language) params.set('language', language);
  if (minPrice !== null) params.set('min_price', minPrice);
  if (maxPrice !== null) params.set('max_price', maxPrice);
  const res = await fetch(`${API_BASE}/events?${params}`);
  if (!res.ok) throw new Error('Failed to fetch events');
  return res.json();
}

export async function fetchEvent(id) {
  const res = await fetch(`${API_BASE}/events/${id}`);
  if (!res.ok) throw new Error('Event not found');
  return res.json();
}
