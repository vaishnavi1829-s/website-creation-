# Theatre Movie Booking App — Implementation Plan

## Tech Stack
- **Frontend:** React 18 + Vite + CSS Modules
- **Backend:** Python FastAPI
- **Database:** PostgreSQL
- **No authentication required**

---

## Database Schema

### movies
| Column | Type | Constraints |
|---|---|---|
| id | SERIAL | PK |
| title | VARCHAR(255) | NOT NULL |
| description | TEXT | |
| poster_url | VARCHAR(500) | |
| duration_min | INTEGER | |
| genre | VARCHAR(100) | |
| language | VARCHAR(50) | |
| rating | VARCHAR(10) | |

### screens
| Column | Type | Constraints |
|---|---|---|
| id | SERIAL | PK |
| name | VARCHAR(100) | NOT NULL |
| capacity | INTEGER | |
| rows | INTEGER | (e.g., 8) |
| cols | INTEGER | (e.g., 12) |

### showtimes
| Column | Type | Constraints |
|---|---|---|
| id | SERIAL | PK |
| movie_id | INTEGER | FK → movies.id |
| screen_id | INTEGER | FK → screens.id |
| start_time | TIMESTAMP | NOT NULL |
| price | DECIMAL(10,2) | NOT NULL |

### seats
| Column | Type | Constraints |
|---|---|---|
| id | SERIAL | PK |
| screen_id | INTEGER | FK → screens.id |
| row_label | CHAR(1) | (A, B, C...) |
| seat_number | INTEGER | (1, 2, 3...) |

### bookings
| Column | Type | Constraints |
|---|---|---|
| id | SERIAL | PK |
| booking_ref | VARCHAR(10) | UNIQUE, NOT NULL |
| customer_name | VARCHAR(150) | NOT NULL |
| customer_email | VARCHAR(255) | NOT NULL |
| customer_phone | VARCHAR(20) | |
| showtime_id | INTEGER | FK → showtimes.id |
| total_amount | DECIMAL(10,2) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

### booking_seats
| Column | Type | Constraints |
|---|---|---|
| id | SERIAL | PK |
| booking_id | INTEGER | FK → bookings.id |
| seat_id | INTEGER | FK → seats.id |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/movies` | List movies (query: `?search=&genre=`) |
| GET | `/api/movies/{id}` | Single movie detail |
| GET | `/api/showtimes` | List showtimes (`?movie_id=&date=`) |
| GET | `/api/showtimes/{id}/seats` | Seat map with booked/available status |
| POST | `/api/bookings` | Create booking |
| GET | `/api/bookings/{ref}` | Get booking by reference |

### POST `/api/bookings` Request Body
```json
{
  "showtime_id": 1,
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "555-0100",
  "seat_ids": [12, 13, 14]
}
```

---

## Frontend Routes & Components

| Route | Component | Purpose |
|---|---|---|
| `/` | `MovieGrid` | Browse movies with search & genre filter |
| `/movie/:id` | `MovieDetail` + `ShowtimeList` | Movie info + pick a showtime |
| `/book/:showtimeId` | `SeatPicker` + `BookingForm` | Choose seats + enter details |
| `/confirmation/:ref` | `BookingConfirmation` | Booking summary & ticket info |

### Component Tree
```
App
├── Navbar
├── Routes
│   ├── MovieGrid
│   │   ├── SearchBar
│   │   ├── GenreFilter
│   │   └── MovieCard (×N)
│   ├── MovieDetail
│   │   ├── MovieInfo
│   │   └── ShowtimeList
│   │       └── ShowtimeCard (×N)
│   ├── BookPage
│   │   ├── SeatMap
│   │   │   └── Seat (×N)
│   │   └── BookingForm
│   └── BookingConfirmation
│       └── TicketSummary
└── Footer
```

---

## Project Structure

```
/backend
├── main.py              # FastAPI app entry
├── database.py          # DB connection & session
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── routers/
│   ├── movies.py
│   ├── showtimes.py
│   └── bookings.py
├── seed.py              # Seed data script
└── requirements.txt

/frontend
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── api.js           # API helper functions
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── Navbar.css
│   │   ├── Footer.jsx
│   │   ├── Footer.css
│   │   ├── MovieCard.jsx
│   │   ├── MovieCard.css
│   │   ├── SearchBar.jsx
│   │   ├── GenreFilter.jsx
│   │   ├── SeatMap.jsx
│   │   ├── SeatMap.css
│   │   └── BookingForm.jsx
│   │   └── BookingForm.css
│   └── pages/
│       ├── Home.jsx
│       ├── Home.css
│       ├── MovieDetail.jsx
│       ├── MovieDetail.css
│       ├── BookPage.jsx
│       ├── BookPage.css
│       ├── Confirmation.jsx
│       └── Confirmation.css
```

---

## Seed Data
- 6 movies across different genres
- 3 screens with different capacities
- Showtimes spanning the next 7 days
- Auto-generated seat grids per screen
