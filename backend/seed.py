"""
Seed script - Salem district theatres, realistic multiplex seat layouts.
Each theatre has a unique layout with sections (Recliner, Premium, Executive, Gold, Silver, Balcony),
aisles, and theatre-specific capacities (120-300 seats).
Run: python seed.py from backend dir or python backend/seed.py from root
"""
from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import Movie, Theatre, Screen, Showtime, Seat, User, Event
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
    {"name":"INOX - Reliance Mall","location":"Reliance Mall, Meyyanur, Salem - 636004","facilities":"Dolby Atmos, 4K Laser, Recliner, Food Court, Parking","distance_km":3.2},
    {"name":"ARRS Multiplex","location":"Meyyanur Bypass Road, Salem - 636004","facilities":"4K Projection, Dolby 7.1, Cafe Lounge, Parking, Wheelchair","distance_km":3.8},
    {"name":"Aascars Multiplex","location":"Erumapalayam, Salem - 636015","facilities":"Dolby Atmos, 3D, Royal Seats, Food Court, Parking","distance_km":2.5},
    {"name":"Raajam Cineplex","location":"Karuppur Main Road, Salem - 636012","facilities":"4K Digital, Dolby Stereo, Snack Bar, Parking","distance_km":5.0},
    {"name":"SPR Cinecastle","location":"Rajaji Street, Swarnapuri, Salem - 636004","facilities":"Dolby Atmos, 4K, Luxury Seats, Cafe, Parking","distance_km":2.0},
    {"name":"ROX DNC Theatres","location":"Sarada College Road, Fairlands, Salem - 636016","facilities":"4K Projection, Dolby 7.1, Gold Class, Food Court, Parking","distance_km":4.5},
    {"name":"Sangeeth Complex","location":"Gugai, Salem - 636006","facilities":"Dolby Digital, 2K, Balcony, Parking","distance_km":6.0},
    {"name":"Sree Raja Sabari Theatre","location":"Gugai Main Road, Salem - 636006","facilities":"Dolby Stereo, 4K Digital, Balcony, Snack Counter","distance_km":5.5},
    {"name":"Dhivyam Cinemax","location":"Kondalampatty Bypass, Salem - 636010","facilities":"Dolby Atmos, 3D, Push Back Seats, Food Court, Parking","distance_km":7.0},
    {"name":"Prakash Cinema","location":"Kitchipalayam, Salem - 636015","facilities":"Dolby Digital, 2K, Balcony, Parking","distance_km":3.0},
]

theatres = []
for td in theatres_data:
    t = Theatre(**td)
    db.add(t)
    theatres.append(t)
db.flush()

row_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# --- Layout definitions ---
# (section_name, num_rows, seats_per_row, price_multiplier, color)
# aisles: list of 1-based col indices where aisle breaks occur

LAYOUT_PREMIUM_LARGE = {
    "sections": [
        ("Recliner",  2, 16, 2.0, "#c9a84c"),
        ("Premium",   5, 20, 1.5, "#9b59b6"),
        ("Executive", 6, 22, 1.0, "#e63946"),
        ("Gold",      4, 24, 0.8, "#f4a261"),
    ],
    "aisles": [8, 16],
}

LAYOUT_MEDIUM = {
    "sections": [
        ("Premium",   3, 18, 1.5, "#9b59b6"),
        ("Executive", 5, 20, 1.0, "#e63946"),
        ("Gold",      4, 22, 0.8, "#f4a261"),
    ],
    "aisles": [7, 14],
}

LAYOUT_STANDARD = {
    "sections": [
        ("Executive", 4, 16, 1.0, "#e63946"),
        ("Silver",    6, 18, 0.7, "#4a90d9"),
    ],
    "aisles": [8],
}

LAYOUT_BALCONY = {
    "sections": [
        ("Balcony",   5, 14, 1.3, "#9b59b6"),
        ("Executive", 7, 16, 1.0, "#e63946"),
        ("Silver",    5, 18, 0.7, "#4a90d9"),
    ],
    "aisles": [6, 12],
}

# Assign layouts to theatres
theatre_layouts = [
    (0, "Screen 1", LAYOUT_PREMIUM_LARGE),
    (0, "Screen 2", LAYOUT_MEDIUM),
    (1, "Screen 1", LAYOUT_MEDIUM),
    (1, "Screen 2", LAYOUT_STANDARD),
    (2, "Screen 1", LAYOUT_PREMIUM_LARGE),
    (2, "Screen 2", LAYOUT_MEDIUM),
    (3, "Screen 1", LAYOUT_BALCONY),
    (3, "Screen 2", LAYOUT_STANDARD),
    (4, "Screen 1", LAYOUT_MEDIUM),
    (4, "Screen 2", LAYOUT_STANDARD),
    (5, "Screen 1", LAYOUT_BALCONY),
    (5, "Screen 2", LAYOUT_MEDIUM),
    (6, "Screen 1", LAYOUT_STANDARD),
    (6, "Screen 2", LAYOUT_STANDARD),
    (7, "Screen 1", LAYOUT_BALCONY),
    (7, "Screen 2", LAYOUT_STANDARD),
    (8, "Screen 1", LAYOUT_PREMIUM_LARGE),
    (8, "Screen 2", LAYOUT_MEDIUM),
    (9, "Screen 1", LAYOUT_STANDARD),
    (9, "Screen 2", LAYOUT_STANDARD),
]

screens = []

for theatre_idx, screen_name, layout in theatre_layouts:
    theatre = theatres[theatre_idx]
    total_seats = 0
    max_cols = 0
    total_rows = 0
    for section_name, num_rows, seats_per_row, mult, color in layout["sections"]:
        total_seats += num_rows * seats_per_row
        total_rows += num_rows
        if seats_per_row > max_cols:
            max_cols = seats_per_row

    screen = Screen(
        theatre_id=theatre.id,
        name=screen_name,
        capacity=total_seats,
        rows=total_rows,
        cols=max_cols,
    )
    db.add(screen)
    db.flush()  # CRITICAL: flush to get screen.id
    screens.append(screen)

    # Generate seats with sections for this screen
    current_row = 0
    for section_name, num_rows, seats_per_row, mult, color in layout["sections"]:
        for r in range(num_rows):
            row_label = row_labels[current_row + r]
            seat_num = 0
            for col in range(1, seats_per_row + 1):
                if col in set(layout["aisles"]):
                    pass  # skip aisle positions in numbering
                seat_num += 1
                db.add(Seat(
                    screen_id=screen.id,
                    row_label=row_label,
                    seat_number=seat_num,
                    section=section_name,
                    price_multiplier=mult,
                ))
        current_row += num_rows

db.flush()

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

# --- Showtimes ---
base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
time_slots = [(10, 30), (14, 0), (18, 30), (21, 15)]

import random as rnd
rnd.seed(42)

for day_offset in range(7):
    day = base_date + timedelta(days=day_offset)
    day_theatres = theatres[:]
    rnd.shuffle(day_theatres)
    for movie in movies:
        t1 = day_theatres[movie.id % len(day_theatres)]
        t2 = day_theatres[(movie.id + 3) % len(day_theatres)]
        for ti, theatre in enumerate([t1, t2]):
            slots = time_slots[day_offset % 2: day_offset % 2 + 2] if day_offset % 2 == 0 else time_slots[2:4]
            for slot in slots[:2]:
                start_time = day.replace(hour=slot[0], minute=slot[1])
                screen_idx = theatre.id * 2 - 2 + ti % 2
                if screen_idx >= len(screens):
                    continue
                screen = screens[screen_idx]
                existing = db.query(Showtime).filter(
                    Showtime.screen_id == screen.id,
                    Showtime.start_time == start_time,
                ).first()
                if existing:
                    continue
                if theatre.id <= 3:
                    base_price = rnd.choice([220, 250, 280])
                elif theatre.id <= 6:
                    base_price = rnd.choice([180, 200, 220])
                else:
                    base_price = rnd.choice([140, 160, 180])
                db.add(Showtime(movie_id=movie.id, screen_id=screen.id, start_time=start_time, price=base_price))

# --- Events ---
event_data = [
    # Kids
    {"title":"Maya Bazaar – Grand Magic Show","description":"Chennai's most spectacular magic extravaganza!","image_url":"","category":"kids","artist_name":"Gopinath Muthukad","venue":"Kamarajar Arangam","city":"Chennai","location":"Teynampet, Chennai - 600018","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=5),"event_time":"4:00 PM","price":350,"language":"Tamil","age_recommendation":"All Ages","rating":0,"trending":95},
    {"title":"Bommalattam – Traditional Puppet Festival","description":"500-year-old Tamil art of Bommalattam!","image_url":"","category":"kids","artist_name":"Thanjavur Puppetry Troupe","venue":"DakshinaChitra Heritage Museum","city":"Chennai","location":"Muttukadu, Chennai - 603112","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=8),"event_time":"5:00 PM","price":200,"language":"Tamil","age_recommendation":"3+","rating":0,"trending":88},
    {"title":"Kathai Kalatta – Storytelling","description":"Magical evening of Tamil folk tales.","image_url":"","category":"kids","artist_name":"Jeeva Raghunath","venue":"Theosophical Society Gardens","city":"Chennai","location":"Adyar, Chennai - 600020","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=6),"event_time":"6:00 PM","price":250,"language":"Tamil","age_recommendation":"3+","rating":0,"trending":85},
    {"title":"Chutti TV Carnival","description":"Chutti TV's biggest character meet-and-greet!","image_url":"","category":"kids","artist_name":"Chutti TV Stars","venue":"Chennai Trade Centre","city":"Chennai","location":"Nandambakkam, Chennai - 600089","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=12),"event_time":"10:00 AM","price":450,"language":"Tamil","age_recommendation":"All Ages","rating":0,"trending":98},
    {"title":"Jr. Scientist Lab","description":"60+ interactive science exhibits!","image_url":"","category":"kids","artist_name":"Anna Science Centre","venue":"Birla Planetarium","city":"Chennai","location":"Guindy, Chennai - 600025","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=9),"event_time":"9:30 AM","price":300,"language":"Tamil","age_recommendation":"6+","rating":0,"trending":92},
    {"title":"Kumki – Bubble Mania","description":"Biggest bubble festival in South India!","image_url":"","category":"kids","artist_name":"Bubble Planet India","venue":"VGP Universal Kingdom","city":"Chennai","location":"East Coast Road, Chennai - 600041","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=4),"event_time":"11:00 AM","price":500,"language":"English","age_recommendation":"All Ages","rating":0,"trending":90},
    {"title":"Silly Sampradayam","description":"Laughter riot exclusively for kids!","image_url":"","category":"kids","artist_name":"Bosskey & Madhan Bob","venue":"Alliance Française","city":"Chennai","location":"Nungambakkam, Chennai - 600034","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=10),"event_time":"10:30 AM","price":250,"language":"Tamil","age_recommendation":"5+","rating":0,"trending":82},
    {"title":"Kalai Kovil – Art & Pottery","description":"Vibrant celebration of Tamil arts!","image_url":"","category":"kids","artist_name":"Cholamandal Artists Village","venue":"Cholamandal Centre for Arts","city":"Chennai","location":"Injambakkam, Chennai - 600041","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=14),"event_time":"10:00 AM","price":400,"language":"Tamil","age_recommendation":"4+","rating":0,"trending":80},
    {"title":"Jungle Book – Musical","description":"Broadway-style Tamil musical!","image_url":"","category":"kids","artist_name":"Little Theatre Chennai","venue":"Music Academy","city":"Chennai","location":"TTK Road, Chennai - 600014","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=18),"event_time":"4:00 PM","price":550,"language":"Tamil","age_recommendation":"All Ages","rating":0,"trending":94},
    # Music
    {"title":"A.R. Rahman – Isai Puyal Live","description":"The Mozart of Madras returns home!","image_url":"","category":"music","artist_name":"A.R. Rahman","venue":"YMCA Grounds","city":"Chennai","location":"Nandanam, Chennai - 600035","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=20),"event_time":"6:30 PM","price":2500,"language":"Tamil","age_recommendation":None,"rating":4.9,"trending":100},
    {"title":"Anirudh – Kolaveri Night","description":"Rockstar Anirudh live!","image_url":"","category":"music","artist_name":"Anirudh Ravichander","venue":"Nehru Indoor Stadium","city":"Chennai","location":"Periamet, Chennai - 600003","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=22),"event_time":"7:00 PM","price":2200,"language":"Tamil","age_recommendation":None,"rating":4.8,"trending":99},
    {"title":"Sid Sriram – Carnatic to Cinema","description":"Golden voice bridges classical & contemporary!","image_url":"","category":"music","artist_name":"Sid Sriram","venue":"Narada Gana Sabha","city":"Chennai","location":"TTK Road, Chennai - 600014","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=10),"event_time":"6:00 PM","price":1500,"language":"Tamil","age_recommendation":None,"rating":4.8,"trending":96},
    {"title":"Tamil Indie Music Fest","description":"25+ emerging Tamil artists!","image_url":"","category":"music","artist_name":"25+ Indie Artists","venue":"Mahabs Beach Resort","city":"Chennai","location":"Mahabalipuram, Chennai - 603104","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=28),"event_time":"4:00 PM","price":700,"language":"Tamil","age_recommendation":None,"rating":4.2,"trending":86},
    {"title":"Chennai Sangamam – Margazhi","description":"Iconic music season with 50+ artists!","image_url":"","category":"music","artist_name":"Various Maestros","venue":"Music Academy","city":"Chennai","location":"TTK Road, Chennai - 600014","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=30),"event_time":"8:00 AM","price":500,"language":"Tamil","age_recommendation":None,"rating":4.9,"trending":98},
    # Comedy
    {"title":"Madurai Muthu – Sirikalam","description":"Tamil Nadu's most loved comedian!","image_url":"","category":"comedy","artist_name":"Madurai Muthu","venue":"Kalaignar Arangam","city":"Chennai","location":"Teynampet, Chennai - 600018","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=8),"event_time":"6:30 PM","price":499,"language":"Tamil","age_recommendation":"12+","rating":4.7,"trending":100},
    {"title":"Vadivelu Tribute Night","description":"Tribute to Tamil cinema's greatest!","image_url":"","category":"comedy","artist_name":"Chennai Mimicry Stars","venue":"Vani Mahal","city":"Chennai","location":"T. Nagar, Chennai - 600017","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=6),"event_time":"6:00 PM","price":299,"language":"Tamil","age_recommendation":"All Ages","rating":4.8,"trending":99},
    {"title":"Goundamani Senthil Night","description":"Celebration of Tamil cinema's greatest duo!","image_url":"","category":"comedy","artist_name":"Tamil Cinema Fan Club","venue":"Bharatiya Vidya Bhavan","city":"Chennai","location":"Mylapore, Chennai - 600004","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=9),"event_time":"5:00 PM","price":250,"language":"Tamil","age_recommendation":"All Ages","rating":4.9,"trending":96},
    {"title":"Evam Open Mic Night","description":"20 new comedians, 5 mins each!","image_url":"","category":"comedy","artist_name":"Evam Comedy Collective","venue":"Medai – The Stage","city":"Chennai","location":"Alwarpet, Chennai - 600018","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=3),"event_time":"7:00 PM","price":199,"language":"Tamil","age_recommendation":"16+","rating":4.1,"trending":84},
    {"title":"Robo Shankar – Enna Comedy","description":"Stand-up, mimicry, movie dialogues!","image_url":"","category":"comedy","artist_name":"Robo Shankar","venue":"Sir Mutha Venkatasubba Rao Hall","city":"Chennai","location":"Harrington Road, Chennai - 600031","event_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=10),"event_time":"7:00 PM","price":599,"language":"Tamil","age_recommendation":"12+","rating":4.6,"trending":98},
]

for ed in event_data:
    db.add(Event(**ed))

db.commit()

tamil_count = sum(1 for m in movies_data if m['language'] == 'Tamil')
eng_count = sum(1 for m in movies_data if m['language'] == 'English')
total_seats = db.query(Seat).count()
section_counts = db.query(Seat.section).distinct().all()

print("Database seeded successfully!")
print(f"   - {len(theatres_data)} theatres in Salem district")
print(f"   - {len(screens)} screens with realistic multiplex layouts")
print(f"   - {total_seats} seats across sections: {[s[0] for s in section_counts]}")
print(f"   - Theatre capacities: 120-300+ seats per screen")
print(f"   - {len(movies_data)} movies ({tamil_count} Tamil, {eng_count} English)")
print(f"   - Showtimes across next 7 days with tiered pricing")
print(f"   - {len(event_data)} events (Kids, Music, Comedy)")
db.close()
