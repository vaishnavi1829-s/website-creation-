"""
Seed script — populates the database with sample movies, screens, showtimes, and seats.
Run: python seed.py
"""
from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import Movie, Screen, Showtime, Seat

# Recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Movies ---
movies_data = [
    {
        "title": "The Last Horizon",
        "description": "A crew of astronauts embarks on humanity's final mission to find a new home among the stars, only to discover they are not alone in the void.",
        "poster_url": "https://picsum.photos/seed/movie1/400/600",
        "duration_min": 148,
        "genre": "Sci-Fi",
        "language": "English",
        "rating": "PG-13",
    },
    {
        "title": "Whispers in the Rain",
        "description": "Two strangers meet at a rainy bus stop and form an unexpected bond that changes both their lives forever.",
        "poster_url": "https://picsum.photos/seed/movie2/400/600",
        "duration_min": 112,
        "genre": "Romance",
        "language": "English",
        "rating": "PG",
    },
    {
        "title": "Shadow Protocol",
        "description": "A disavowed intelligence agent must stop a global conspiracy while being hunted by the very agency she once served.",
        "poster_url": "https://picsum.photos/seed/movie3/400/600",
        "duration_min": 135,
        "genre": "Action",
        "language": "English",
        "rating": "R",
    },
    {
        "title": "The Glass Garden",
        "description": "In a post-apocalyptic world, a botanist discovers a hidden greenhouse that holds the key to restoring life on Earth.",
        "poster_url": "https://picsum.photos/seed/movie4/400/600",
        "duration_min": 126,
        "genre": "Drama",
        "language": "English",
        "rating": "PG-13",
    },
    {
        "title": "Crimson Night",
        "description": "A detective with a troubled past investigates a series of bizarre murders in a neon-lit city where nothing is as it seems.",
        "poster_url": "https://picsum.photos/seed/movie5/400/600",
        "duration_min": 141,
        "genre": "Thriller",
        "language": "English",
        "rating": "R",
    },
    {
        "title": "Laugh Factory",
        "description": "A struggling comedian enters a high-stakes comedy competition and discovers that winning isn't everything.",
        "poster_url": "https://picsum.photos/seed/movie6/400/600",
        "duration_min": 98,
        "genre": "Comedy",
        "language": "English",
        "rating": "PG-13",
    },
    {
        "title": "96",
        "description": "A travel photographer reunites with his high school sweetheart after 22 years, rekindling memories of their unforgettable school days and the love that never faded.",
        "poster_url": "https://picsum.photos/seed/movie7/400/600",
        "duration_min": 158,
        "genre": "Romance",
        "language": "Tamil",
        "rating": "U",
    },
    {
        "title": "Bigil",
        "description": "A retired footballer turned coach trains an underdog women's football team to compete at the national level while battling personal demons and a ruthless rival.",
        "poster_url": "https://picsum.photos/seed/movie8/400/600",
        "duration_min": 177,
        "genre": "Action",
        "language": "Tamil",
        "rating": "UA",
    },
    {
        "title": "Vada Chennai",
        "description": "Set across three decades in North Chennai, a skilled carrom player gets entangled in the brutal gang wars that define the city's underworld.",
        "poster_url": "https://picsum.photos/seed/movie9/400/600",
        "duration_min": 164,
        "genre": "Drama",
        "language": "Tamil",
        "rating": "A",
    },
    {
        "title": "Love Today",
        "description": "A young couple is forced to swap their unlocked phones for 24 hours as a trust test before marriage, leading to hilarious and shocking revelations about their digital lives.",
        "poster_url": "https://picsum.photos/seed/movie10/400/600",
        "duration_min": 154,
        "genre": "Romance",
        "language": "Tamil",
        "rating": "UA",
    },
]

movies = []
for m in movies_data:
    movie = Movie(**m)
    db.add(movie)
    movies.append(movie)
db.flush()

# --- Screens ---
screens_data = [
    {"name": "Screen 1 - IMAX", "capacity": 96, "rows": 8, "cols": 12},
    {"name": "Screen 2 - Dolby", "capacity": 80, "rows": 8, "cols": 10},
    {"name": "Screen 3 - Standard", "capacity": 64, "rows": 8, "cols": 8},
]

screens = []
for s in screens_data:
    screen = Screen(**s)
    db.add(screen)
    screens.append(screen)
db.flush()

# --- Seats ---
row_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for screen in screens:
    for r in range(screen.rows):
        for c in range(1, screen.cols + 1):
            seat = Seat(screen_id=screen.id, row_label=row_labels[r], seat_number=c)
            db.add(seat)
db.flush()

# --- Showtimes ---
# Generate showtimes for the next 7 days
base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
time_slots = [
    (10, 30),  # 10:30 AM
    (13, 45),  # 1:45 PM
    (17, 0),   # 5:00 PM
    (20, 15),  # 8:15 PM
]

for day_offset in range(7):
    day = base_date + timedelta(days=day_offset)
    for movie_idx, movie in enumerate(movies):
        # Assign screen round-robin
        screen = screens[movie_idx % len(screens)]
        # Pick 1-2 showtimes per movie per day
        slots_to_use = [time_slots[day_offset % len(time_slots)], time_slots[(day_offset + 2) % len(time_slots)]]
        for slot in slots_to_use[:2]:
            start_time = day.replace(hour=slot[0], minute=slot[1])
            # Skip if slot already used
            existing = db.query(Showtime).filter(
                Showtime.screen_id == screen.id,
                Showtime.start_time == start_time,
            ).first()
            if existing:
                # Use different slot
                start_time = day.replace(hour=time_slots[0][0], minute=time_slots[0][1])
                existing2 = db.query(Showtime).filter(
                    Showtime.screen_id == screen.id,
                    Showtime.start_time == start_time,
                ).first()
                if existing2:
                    continue

            price = 12.0 if "Standard" in screen.name else (16.0 if "Dolby" in screen.name else 20.0)
            showtime = Showtime(
                movie_id=movie.id,
                screen_id=screen.id,
                start_time=start_time,
                price=price,
            )
            db.add(showtime)

db.commit()
print("Database seeded successfully!")
print(f"   - {len(movies_data)} movies")
print(f"   - {len(screens_data)} screens")
print(f"   - {sum(s.rows * s.cols for s in screens)} seats")
print(f"   - Showtimes across the next 7 days")
db.close()
