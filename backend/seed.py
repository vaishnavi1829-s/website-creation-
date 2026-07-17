"""
Seed script - Salem district theatres, Tamil & English movies, prices in INR.
Run: python seed.py from backend dir or python backend/seed.py from root
"""
from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import Movie, Theatre, Screen, Showtime, Seat, User
from auth import hash_password

# Recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Users ---
for u in [
    {"username": "john", "password": "password123", "email": "john@example.com", "full_name": "John Doe"},
    {"username": "jane", "password": "password123", "email": "jane@example.com", "full_name": "Jane Smith"},
]:
    db.add(User(username=u["username"], hashed_password=hash_password(u["password"]), email=u["email"], full_name=u["full_name"]))
db.flush()

# --- 10 Salem District Theatres ---
theatres_data = [
    {
        "name": "INOX - Reliance Mall",
        "location": "Reliance Mall, Meyyanur, Salem - 636004",
        "facilities": "Dolby Atmos, 4K Laser, Recliner Seats, Food Court, Parking, AC",
        "distance_km": 3.2,
    },
    {
        "name": "ARRS Multiplex",
        "location": "Meyyanur Bypass Road, Salem - 636004",
        "facilities": "4K Projection, Dolby 7.1, Cafe Lounge, Parking, AC, Wheelchair Access",
        "distance_km": 3.8,
    },
    {
        "name": "Aascars Multiplex",
        "location": "Erumapalayam, Salem - 636015",
        "facilities": "Dolby Atmos, 3D, Royal Seats, Food Court, Parking, AC",
        "distance_km": 2.5,
    },
    {
        "name": "Raajam Cineplex",
        "location": "Karuppur Main Road, Salem - 636012",
        "facilities": "4K Digital, Dolby Stereo, Snack Bar, Parking, AC",
        "distance_km": 5.0,
    },
    {
        "name": "SPR Cinecastle",
        "location": "Rajaji Street, Swarnapuri, Salem - 636004",
        "facilities": "Dolby Atmos, 4K, Luxury Seats, Parking, Cafe, AC",
        "distance_km": 2.0,
    },
    {
        "name": "ROX DNC Theatres",
        "location": "Sarada College Road, Fairlands, Salem - 636016",
        "facilities": "4K Projection, Dolby 7.1, Gold Class, Food Court, Parking, AC",
        "distance_km": 4.5,
    },
    {
        "name": "Sangeeth Complex",
        "location": "Gugai, Salem - 636006",
        "facilities": "Dolby Digital, 2K, Balcony, Parking, AC",
        "distance_km": 6.0,
    },
    {
        "name": "Sree Raja Sabari Theatre",
        "location": "Gugai Main Road, Salem - 636006",
        "facilities": "Dolby Stereo, 4K Digital, Balcony, Snack Counter, AC",
        "distance_km": 5.5,
    },
    {
        "name": "Dhivyam Cinemax",
        "location": "Kondalampatty Bypass, Salem - 636010",
        "facilities": "Dolby Atmos, 3D, Push Back Seats, Parking, Food Court, AC",
        "distance_km": 7.0,
    },
    {
        "name": "Prakash Cinema",
        "location": "Kitchipalayam, Salem - 636015",
        "facilities": "Dolby Digital, 2K, Balcony, Parking, AC",
        "distance_km": 3.0,
    },
]

theatres = []
for td in theatres_data:
    t = Theatre(**td)
    db.add(t)
    theatres.append(t)
db.flush()

# --- Screens (2 per theatre = 20 screens) ---
screen_configs = [
    ("Screen 1", 80, 8, 10),  # name, capacity, rows, cols
    ("Screen 2", 64, 8, 8),
]

screens = []
row_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for theatre in theatres:
    for sc_name, cap, rows, cols in screen_configs:
        screen = Screen(
            theatre_id=theatre.id,
            name=f"{sc_name}",
            capacity=cap,
            rows=rows,
            cols=cols,
        )
        db.add(screen)
        screens.append(screen)
db.flush()

# --- Seats for all screens ---
for screen in screens:
    for r in range(screen.rows):
        for c in range(1, screen.cols + 1):
            db.add(Seat(screen_id=screen.id, row_label=row_labels[r], seat_number=c))
db.flush()

# All seats created now

# --- 18 Movies ---
movies_data = [
    # Tamil
    {"title":"Leo","description":"A mild-mannered cafe owner in Kashmir becomes the target of a ruthless drug cartel who believe he is their former gangster partner.","poster_url":"https://image.tmdb.org/t/p/w500/pQFoHvH3f8FU87hGNY6Q7dfO88F.jpg","duration_min":163,"genre":"Action","language":"Tamil","rating":"UA","release_year":2023,"imdb_rating":7.4,"trending":95,"category":"Action"},
    {"title":"Vikram","description":"A special investigation team uncovers a vast conspiracy involving a drug syndicate and a ghost from the past.","poster_url":"https://image.tmdb.org/t/p/w500/8WRKBcHXPBzrKvKxKmqFVKTQtt9.jpg","duration_min":175,"genre":"Action","language":"Tamil","rating":"UA","release_year":2022,"imdb_rating":8.4,"trending":98,"category":"Action"},
    {"title":"Amaran","description":"Based on the true story of Major Mukund Varadarajan, a brave Indian Army officer who made the ultimate sacrifice.","poster_url":"https://image.tmdb.org/t/p/w500/6UxhTRgAmue0wIJbpWmbGHGs9Ar.jpg","duration_min":169,"genre":"Action","language":"Tamil","rating":"UA","release_year":2024,"imdb_rating":8.7,"trending":99,"category":"Action"},
    {"title":"Dragon","description":"A mythical dragon awakens beneath ancient temples. A young archeologist must decipher age-old secrets.","poster_url":"https://image.tmdb.org/t/p/w500/zxDDBrXiBPHCu5OpQjS5gS0gSJv.jpg","duration_min":155,"genre":"Action","language":"Tamil","rating":"UA","release_year":2025,"imdb_rating":8.0,"trending":88,"category":"Action"},
    {"title":"Good Night","description":"A charming romantic comedy about a young couple navigating modern relationships in Chennai.","poster_url":"https://image.tmdb.org/t/p/w500/3J0xM7UvTBKVe4CvSyjFvJ8AzhO.jpg","duration_min":142,"genre":"Romance","language":"Tamil","rating":"U","release_year":2023,"imdb_rating":8.1,"trending":82,"category":"Romantic"},
    {"title":"Parking","description":"An intense thriller that unfolds entirely in a parking garage when two strangers get trapped after hours.","poster_url":"https://image.tmdb.org/t/p/w500/2kCcgY1EKWdzF9oVSMDsE5DqJEa.jpg","duration_min":128,"genre":"Thriller","language":"Tamil","rating":"UA","release_year":2023,"imdb_rating":7.9,"trending":78,"category":"Thriller"},
    {"title":"Lubber Pandhu","description":"A feel-good sports drama following a middle-aged cricketer who gets one last shot at glory.","poster_url":"https://image.tmdb.org/t/p/w500/3uGgoXdMRzDANYYqsq6KlfNud8D.jpg","duration_min":148,"genre":"Romance","language":"Tamil","rating":"U","release_year":2024,"imdb_rating":8.3,"trending":85,"category":"Romantic"},
    {"title":"Raayan","description":"A young man rises through Chennai's underworld to avenge his family's brutal murder.","poster_url":"https://image.tmdb.org/t/p/w500/z9CfCXYGPlBZLZkq3WENKn3xTBL.jpg","duration_min":166,"genre":"Action","language":"Tamil","rating":"A","release_year":2024,"imdb_rating":7.8,"trending":90,"category":"Action"},
    {"title":"Thug Life","description":"A reformed gangster is pulled back into crime when his past catches up with him in Madurai.","poster_url":"https://image.tmdb.org/t/p/w500/3KzrLWNrnZUKYjrrGltE2XjGsCG.jpg","duration_min":172,"genre":"Action","language":"Tamil","rating":"UA","release_year":2025,"imdb_rating":8.2,"trending":92,"category":"Action"},
    # English
    {"title":"Avengers: Endgame","description":"The remaining Avengers must assemble once more to undo Thanos' actions and restore balance.","poster_url":"https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg","duration_min":181,"genre":"Action","language":"English","rating":"UA","release_year":2019,"imdb_rating":8.4,"trending":96,"category":"Action"},
    {"title":"Interstellar","description":"A team of astronauts travels through a wormhole in search of a new home for humanity.","poster_url":"https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg","duration_min":169,"genre":"Action","language":"English","rating":"UA","release_year":2014,"imdb_rating":8.7,"trending":97,"category":"Action"},
    {"title":"The Batman","description":"When a sadistic killer targets Gotham's elite, Batman must uncover corruption tied to his family.","poster_url":"https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg","duration_min":176,"genre":"Action","language":"English","rating":"UA","release_year":2022,"imdb_rating":7.8,"trending":89,"category":"Action"},
    {"title":"Oppenheimer","description":"The story of J. Robert Oppenheimer and his role in developing the atomic bomb.","poster_url":"https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg","duration_min":180,"genre":"Thriller","language":"English","rating":"UA","release_year":2023,"imdb_rating":8.4,"trending":100,"category":"Thriller"},
    {"title":"Inception","description":"A thief who steals secrets through dream-sharing technology is tasked with planting an idea.","poster_url":"https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg","duration_min":148,"genre":"Action","language":"English","rating":"UA","release_year":2010,"imdb_rating":8.8,"trending":94,"category":"Action"},
    {"title":"John Wick: Chapter 4","description":"John Wick faces a new enemy with global alliances on his path to defeating the High Table.","poster_url":"https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg","duration_min":169,"genre":"Action","language":"English","rating":"A","release_year":2023,"imdb_rating":7.9,"trending":93,"category":"Action"},
    {"title":"The Conjuring","description":"Paranormal investigators help a family terrorized by a dark presence in their farmhouse.","poster_url":"https://image.tmdb.org/t/p/w500/ejrD1XjwLMI47qP3xrVygKyPrLu.jpg","duration_min":112,"genre":"Horror","language":"English","rating":"A","release_year":2013,"imdb_rating":7.5,"trending":80,"category":"Horror/Ghost"},
    {"title":"Titanic","description":"A seventeen-year-old aristocrat falls in love with a poor artist aboard the R.M.S. Titanic.","poster_url":"https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg","duration_min":194,"genre":"Romance","language":"English","rating":"UA","release_year":1997,"imdb_rating":7.9,"trending":87,"category":"Romantic"},
    {"title":"Mission: Impossible - Dead Reckoning","description":"Ethan Hunt tracks down a terrifying new weapon before it falls into the wrong hands.","poster_url":"https://image.tmdb.org/t/p/w500/NNxYVw5z5ffJKyBJzHNJRnDIu.jpg","duration_min":163,"genre":"Action","language":"English","rating":"UA","release_year":2023,"imdb_rating":7.8,"trending":91,"category":"Action"},
]

movies = []
for m in movies_data:
    movie = Movie(**m)
    db.add(movie)
    movies.append(movie)
db.flush()

# --- Showtimes: each movie gets showtimes in 2 random theatres per day, 3 time slots ---
base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
time_slots = [(10, 30), (14, 0), (18, 30), (21, 15)]

import random as rnd
rnd.seed(42)

for day_offset in range(7):
    day = base_date + timedelta(days=day_offset)
    # shuffle theatres for each day to spread movies
    day_theatres = theatres[:]
    rnd.shuffle(day_theatres)
    for movie in movies:
        # Pick 2 different theatres per movie per day
        t1 = day_theatres[movie.id % len(day_theatres)]
        t2 = day_theatres[(movie.id + 3) % len(day_theatres)]
        for ti, theatre in enumerate([t1, t2]):
            # Pick 2 time slots
            slots = time_slots[day_offset % 2: day_offset % 2 + 2] if day_offset % 2 == 0 else time_slots[2:4]
            for slot in slots[:2]:
                start_time = day.replace(hour=slot[0], minute=slot[1])
                screen = screens[theatre.id * 2 - 2 + ti % 2]  # alternate screen 1/2
                # Check conflict
                existing = db.query(Showtime).filter(
                    Showtime.screen_id == screen.id,
                    Showtime.start_time == start_time,
                ).first()
                if existing:
                    continue
                # Price based on theatre tier
                if theatre.id <= 3:
                    price = rnd.choice([250, 280, 300])
                elif theatre.id <= 6:
                    price = rnd.choice([200, 220, 250])
                else:
                    price = rnd.choice([150, 180, 200])
                db.add(Showtime(movie_id=movie.id, screen_id=screen.id, start_time=start_time, price=price))

db.commit()

tamil_count = sum(1 for m in movies_data if m['language'] == 'Tamil')
eng_count = sum(1 for m in movies_data if m['language'] == 'English')
print("Database seeded successfully!")
print(f"   - {len(theatres_data)} theatres in Salem district")
print(f"   - {len(screens)} screens total")
print(f"   - {sum(s.rows*s.cols for s in screens)} seats")
print(f"   - {len(movies_data)} movies ({tamil_count} Tamil, {eng_count} English)")
print(f"   - Showtimes across next 7 days (prices in INR)")
db.close()
