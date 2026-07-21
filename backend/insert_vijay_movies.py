"""
Insert Joseph Vijay (Thalapathy Vijay) complete filmography into the existing database.
Run: python insert_vijay_movies.py   from backend dir
  or: python backend/insert_vijay_movies.py  from root
"""
import sys
import os

# Ensure backend dir is on path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Movie, Theatre, Screen, Showtime
from datetime import datetime, timedelta
import random as rnd

rnd.seed(7)

db = SessionLocal()

# ──────────────────────────────────────────────
# Joseph Vijay – Complete Filmography
# ──────────────────────────────────────────────
vijay_movies = [
    # 2026–2020
    {"title": "Jana Nayagan",                "description": "Thalapathy Vijay's final film — a political action drama where a common man rises to take on a corrupt system, marking his swansong before entering full-time politics.", "poster_url": "https://image.tmdb.org/t/p/w500/tnAuCzyCXvPS9PVcAR75lCwNXij.jpg", "duration_min": 170, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2026, "imdb_rating": 9.0, "trending": 100, "category": "Action"},
    {"title": "GOAT",                        "description": "An elite anti-terrorist squad leader faces his most dangerous mission when a ghost from his past resurfaces with a devastating plan.", "poster_url": "https://image.tmdb.org/t/p/w500/A7KjMn9nI4MgkrlGVHWHFehOUIh.jpg", "duration_min": 178, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2024, "imdb_rating": 7.1, "trending": 93, "category": "Action"},
    {"title": "Varisu",                      "description": "The carefree youngest son of a business tycoon must step up and take over the family empire when tragedy strikes.", "poster_url": "https://image.tmdb.org/t/p/w500/yNkjnvHFb4DTR0ro3GFcSMfMttl.jpg", "duration_min": 169, "genre": "Drama", "language": "Tamil", "rating": "UA", "release_year": 2023, "imdb_rating": 6.0, "trending": 88, "category": "Action"},

    # 2022–2019
    {"title": "Beast",                       "description": "A former RAW agent must single-handedly rescue hostages trapped inside a hijacked shopping mall.", "poster_url": "https://image.tmdb.org/t/p/w500/9qGvLhlYzVfM1GhJAkITMKhYIDq.jpg", "duration_min": 155, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2022, "imdb_rating": 5.5, "trending": 85, "category": "Action"},
    {"title": "Master",                      "description": "An alcoholic but brilliant professor is sent to a juvenile correction facility where he clashes with a ruthless gangster running the institution.", "poster_url": "https://image.tmdb.org/t/p/w500/6UxhTRgAmue0wIJbpWmbGHGs9Ar.jpg", "duration_min": 179, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2021, "imdb_rating": 7.4, "trending": 90, "category": "Action"},
    {"title": "Bigil",                       "description": "A former football player turned gangster coaches a women's football team to victory while confronting his violent past.", "poster_url": "https://image.tmdb.org/t/p/w500/rP5wFwY5ZXA89tqHaYxLAI3XuhV.jpg", "duration_min": 177, "genre": "Sports", "language": "Tamil", "rating": "UA", "release_year": 2019, "imdb_rating": 6.8, "trending": 87, "category": "Action"},

    # 2018–2017
    {"title": "Sarkar",                      "description": "An NRI corporate giant returns to India to vote, only to discover his vote was cast fraudulently — sparking a war against political corruption.", "poster_url": "https://image.tmdb.org/t/p/w500/jFj2hfvRnsjiGspOWaqkBGPHKZ8.jpg", "duration_min": 165, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2018, "imdb_rating": 7.0, "trending": 86, "category": "Action"},
    {"title": "Mersal",                      "description": "A doctor seeks vengeance against the medical mafia responsible for his father's death, uncovering a web of corruption across three generations.", "poster_url": "https://image.tmdb.org/t/p/w500/A1Z4cMq6yWbRl2s3FcPkH7dQeN0.jpg", "duration_min": 169, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2017, "imdb_rating": 7.5, "trending": 84, "category": "Action"},
    {"title": "Bairavaa",                    "description": "A debt collector in Chennai takes on a powerful medical college chairman who runs a massive education racket.", "poster_url": "https://image.tmdb.org/t/p/w500/xKd0nLwjf0aHT9nFkP8oZmqKkHw.jpg", "duration_min": 153, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2017, "imdb_rating": 6.0, "trending": 79, "category": "Action"},

    # 2016–2014
    {"title": "Theri",                       "description": "A former police officer living a quiet life as a baker is forced back into action when his daughter's safety is threatened.", "poster_url": "https://image.tmdb.org/t/p/w500/3ZvHpL1TqBTgXPqKXn9QKxLMEsw.jpg", "duration_min": 157, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2016, "imdb_rating": 7.3, "trending": 83, "category": "Action"},
    {"title": "Puli",                        "description": "A blacksmith ventures into a mystical kingdom to rescue his kidnapped wife from a tyrannical queen.", "poster_url": "https://image.tmdb.org/t/p/w500/pYHqKJ8lMZmB5R0cWv2kK9F5tRw.jpg", "duration_min": 155, "genre": "Fantasy", "language": "Tamil", "rating": "UA", "release_year": 2015, "imdb_rating": 4.5, "trending": 72, "category": "Action"},
    {"title": "Kaththi",                     "description": "An escaped prisoner assumes the identity of a look-alike activist and leads a farmer's rebellion against a corporate land-grab.", "poster_url": "https://image.tmdb.org/t/p/w500/s2QxL1PRQyGcK4NqVH8fJkTwKx.jpg", "duration_min": 166, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2014, "imdb_rating": 8.0, "trending": 91, "category": "Action"},
    {"title": "Jilla",                       "description": "A loyal right-hand man to a powerful don must choose between his mentor and the law when he's forced to become a police officer.", "poster_url": "https://image.tmdb.org/t/p/w500/rQxP9mDZfK4nJhLqKXcWmFfSj8v.jpg", "duration_min": 178, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2014, "imdb_rating": 6.8, "trending": 80, "category": "Action"},

    # 2013–2011
    {"title": "Thalaivaa",                   "description": "The son of a legendary Mumbai don returns from Australia to lead the family empire, facing betrayal and rival gangs.", "poster_url": "https://image.tmdb.org/t/p/w500/jRkGpMqKjNtR8Pv9QeFzYwM2Xc.jpg", "duration_min": 181, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2013, "imdb_rating": 6.5, "trending": 78, "category": "Action"},
    {"title": "Thuppakki",                   "description": "An army captain on vacation in Mumbai discovers and dismantles a terrorist sleeper cell network in this edge-of-the-seat thriller.", "poster_url": "https://image.tmdb.org/t/p/w500/5xKd0nLwjf0aHT9nFkP8oZmqKkHw.jpg", "duration_min": 165, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2012, "imdb_rating": 8.1, "trending": 92, "category": "Action"},
    {"title": "Nanban",                      "description": "Two friends search for their long-lost college buddy who taught them to chase excellence over success. Remake of 3 Idiots.", "poster_url": "https://image.tmdb.org/t/p/w500/lPmKqKjNtR8Pv9QeFzYwM2XcBv.jpg", "duration_min": 170, "genre": "Comedy", "language": "Tamil", "rating": "U", "release_year": 2012, "imdb_rating": 7.8, "trending": 82, "category": "Comedy"},
    {"title": "Velayudham",                  "description": "A village simpleton is mistaken for a vigilante superhero and must step up to fight a criminal mastermind threatening the city.", "poster_url": "https://image.tmdb.org/t/p/w500/pQxKjMvD9wFzYwM2XcBvGjRk.jpg", "duration_min": 160, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2011, "imdb_rating": 6.3, "trending": 76, "category": "Action"},
    {"title": "Kaavalan",                    "description": "A bodyguard falls in love with the girl he's protecting, but must hide his feelings when her father finds out.", "poster_url": "https://image.tmdb.org/t/p/w500/mNqFzYwM2XcBvGjRkP9QeFzYw.jpg", "duration_min": 149, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2011, "imdb_rating": 6.5, "trending": 75, "category": "Romantic"},

    # 2010–2007
    {"title": "Sura",                        "description": "A fearless fisherman takes on a corrupt minister trying to evict his village for a real-estate project along the coast.", "poster_url": "https://image.tmdb.org/t/p/w500/xBvGjRkP9QeFzYwM2XcNqKjMv.jpg", "duration_min": 156, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2010, "imdb_rating": 3.8, "trending": 68, "category": "Action"},
    {"title": "Vettaikaaran",                "description": "A college student who dreams of becoming a police officer takes on a powerful don involved in drug trafficking and murder.", "poster_url": "https://image.tmdb.org/t/p/w500/yQeFzYwM2XcNqKjMvD9wFzP9.jpg", "duration_min": 161, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2009, "imdb_rating": 5.7, "trending": 74, "category": "Action"},
    {"title": "Villu",                       "description": "A man seeks revenge against a powerful politician and his son responsible for his father's death.", "poster_url": "https://image.tmdb.org/t/p/w500/zM2XcNqKjMvD9wFzP9QeYwM2.jpg", "duration_min": 150, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2009, "imdb_rating": 4.7, "trending": 71, "category": "Action"},
    {"title": "Kuruvi",                      "description": "A carefree young man travels to Malaysia to rescue his friend's father from a ruthless diamond smuggler.", "poster_url": "https://image.tmdb.org/t/p/w500/cNqKjMvD9wFzP9QeYwM2XcNq.jpg", "duration_min": 170, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2008, "imdb_rating": 5.3, "trending": 73, "category": "Action"},
    {"title": "Azhagiya Tamil Magan",        "description": "A wealthy businessman with psychic abilities discovers an evil doppelgänger who tries to destroy his life.", "poster_url": "https://image.tmdb.org/t/p/w500/dKjMvD9wFzP9QeYwM2XcNqKj.jpg", "duration_min": 178, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2007, "imdb_rating": 5.8, "trending": 77, "category": "Action"},
    {"title": "Pokkiri",                     "description": "An undercover cop infiltrates the Chennai underworld to bring down a ruthless crime syndicate from within.", "poster_url": "https://image.tmdb.org/t/p/w500/eMvD9wFzP9QeYwM2XcNqKjMv.jpg", "duration_min": 161, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2007, "imdb_rating": 7.8, "trending": 89, "category": "Action"},

    # 2006–2004
    {"title": "Aadhi",                       "description": "A young man from a small town comes to Chennai to avenge his parents' murder, uncovering a massive real-estate mafia.", "poster_url": "https://image.tmdb.org/t/p/w500/fD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 135, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2006, "imdb_rating": 5.1, "trending": 70, "category": "Action"},
    {"title": "Sivakasi",                    "description": "A street-smart firecracker factory worker in Sivakasi returns home to reform his estranged family and expose his corrupt brother.", "poster_url": "https://image.tmdb.org/t/p/w500/gP9QeYwM2XcNqKjMvD9wFzP9.jpg", "duration_min": 162, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2005, "imdb_rating": 6.3, "trending": 76, "category": "Action"},
    {"title": "Sachien",                     "description": "A carefree college student and a rich girl fall in love despite their contrasting personalities and family opposition.", "poster_url": "https://image.tmdb.org/t/p/w500/hQeYwM2XcNqKjMvD9wFzP9Qe.jpg", "duration_min": 148, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2005, "imdb_rating": 6.7, "trending": 75, "category": "Romantic"},
    {"title": "Thirupaachi",                 "description": "A village blacksmith travels to Chennai to protect his sister, taking on the city's most feared gangsters.", "poster_url": "https://image.tmdb.org/t/p/w500/jD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 161, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2005, "imdb_rating": 6.5, "trending": 77, "category": "Action"},
    {"title": "Madhurey",                    "description": "A vegetable vendor in Madurai rises up against a powerful don who controls the city through fear and violence.", "poster_url": "https://image.tmdb.org/t/p/w500/kM2XcNqKjMvD9wFzP9QeYwM2.jpg", "duration_min": 160, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2004, "imdb_rating": 6.0, "trending": 72, "category": "Action"},
    {"title": "Ghilli",                      "description": "A state-level kabaddi player rescues a girl from a ruthless Madurai don and must fight to keep her safe. All-time blockbuster.", "poster_url": "https://image.tmdb.org/t/p/w500/lXcNqKjMvD9wFzP9QeYwM2Xc.jpg", "duration_min": 160, "genre": "Action", "language": "Tamil", "rating": "U", "release_year": 2004, "imdb_rating": 8.2, "trending": 95, "category": "Action"},

    # 2003–2000
    {"title": "Thirumalai",                  "description": "A bike mechanic in Chennai falls for a rich girl and takes on a powerful politician who opposes their love.", "poster_url": "https://image.tmdb.org/t/p/w500/mP9QeYwM2XcNqKjMvD9wFzP9.jpg", "duration_min": 158, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2003, "imdb_rating": 6.8, "trending": 74, "category": "Action"},
    {"title": "Vaseegara",                   "description": "A wealthy girl falls for a middle-class man, but misunderstandings and family opposition threaten their relationship.", "poster_url": "https://image.tmdb.org/t/p/w500/nFzP9QeYwM2XcNqKjMvD9wFz.jpg", "duration_min": 156, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2003, "imdb_rating": 6.2, "trending": 69, "category": "Romantic"},
    {"title": "Youth",                       "description": "A young man from a village moves to the city for work and falls in love, but faces obstacles from his family.", "poster_url": "https://image.tmdb.org/t/p/w500/oQeYwM2XcNqKjMvD9wFzP9Qe.jpg", "duration_min": 150, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2002, "imdb_rating": 5.1, "trending": 65, "category": "Romantic"},
    {"title": "Bagavathi",                   "description": "A tea-shop owner in a village single-handedly takes on a powerful politician and his son who exploit the poor.", "poster_url": "https://image.tmdb.org/t/p/w500/pXcNqKjMvD9wFzP9QeYwM2Xc.jpg", "duration_min": 165, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 2002, "imdb_rating": 6.1, "trending": 71, "category": "Action"},
    {"title": "Thamizhan",                   "description": "A young lawyer fights to make legal knowledge accessible to common people, taking on corporate lawyers and political power.", "poster_url": "https://image.tmdb.org/t/p/w500/qKjMvD9wFzP9QeYwM2XcNqKj.jpg", "duration_min": 163, "genre": "Drama", "language": "Tamil", "rating": "U", "release_year": 2002, "imdb_rating": 5.4, "trending": 67, "category": "Action"},
    {"title": "Shahjahan",                   "description": "A young man falls in love with two women and must navigate the complications of a love triangle.", "poster_url": "https://image.tmdb.org/t/p/w500/rMvD9wFzP9QeYwM2XcNqKjMv.jpg", "duration_min": 158, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2001, "imdb_rating": 5.2, "trending": 64, "category": "Romantic"},
    {"title": "Badri",                       "description": "A carefree young man's life changes when he must choose between two women who love him — one innocent, one bold.", "poster_url": "https://image.tmdb.org/t/p/w500/sD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 152, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2001, "imdb_rating": 6.0, "trending": 66, "category": "Romantic"},
    {"title": "Friends",                     "description": "Three childhood friends navigate love, loyalty, and family obligations as their lives take unexpected turns.", "poster_url": "https://image.tmdb.org/t/p/w500/tQeYwM2XcNqKjMvD9wFzP9Qe.jpg", "duration_min": 165, "genre": "Comedy", "language": "Tamil", "rating": "U", "release_year": 2001, "imdb_rating": 7.5, "trending": 73, "category": "Comedy"},
    {"title": "Priyamanavale",               "description": "A modern couple enters into a trial marriage for one year, testing whether love can survive real-world challenges.", "poster_url": "https://image.tmdb.org/t/p/w500/uKjMvD9wFzP9QeYwM2XcNqKj.jpg", "duration_min": 148, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2000, "imdb_rating": 7.0, "trending": 68, "category": "Romantic"},
    {"title": "Kannukkul Nilavu",            "description": "A man with memory loss searches for his identity and the woman he loved, unraveling a tragic mystery.", "poster_url": "https://image.tmdb.org/t/p/w500/vFzP9QeYwM2XcNqKjMvD9wFz.jpg", "duration_min": 155, "genre": "Thriller", "language": "Tamil", "rating": "UA", "release_year": 2000, "imdb_rating": 7.2, "trending": 67, "category": "Thriller"},
    {"title": "Kushi",                       "description": "Two childhood friends who grew up together in the same apartment complex navigate the ups and downs of their evolving relationship.", "poster_url": "https://image.tmdb.org/t/p/w500/wP9QeYwM2XcNqKjMvD9wFzP9.jpg", "duration_min": 170, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 2000, "imdb_rating": 7.9, "trending": 80, "category": "Romantic"},

    # 1999–1997
    {"title": "Minsara Kanna",               "description": "A wealthy but lonely young man hires a poor family to pretend to be his relatives, leading to heartwarming comedy.", "poster_url": "https://image.tmdb.org/t/p/w500/xM2XcNqKjMvD9wFzP9QeYwM2.jpg", "duration_min": 160, "genre": "Comedy", "language": "Tamil", "rating": "U", "release_year": 1999, "imdb_rating": 6.6, "trending": 63, "category": "Comedy"},
    {"title": "Thulladha Manamum Thullum",   "description": "A street musician's life changes when he accidentally blinds a young woman and dedicates his life to helping her.", "poster_url": "https://image.tmdb.org/t/p/w500/yXcNqKjMvD9wFzP9QeYwM2Xc.jpg", "duration_min": 165, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1999, "imdb_rating": 8.0, "trending": 81, "category": "Romantic"},
    {"title": "Endrendrum Kadhal",           "description": "A successful businessman falls for a traditional woman, but their different worldviews create conflicts in their relationship.", "poster_url": "https://image.tmdb.org/t/p/w500/zNqKjMvD9wFzP9QeYwM2XcNq.jpg", "duration_min": 150, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1999, "imdb_rating": 5.5, "trending": 60, "category": "Romantic"},
    {"title": "Nenjinile",                   "description": "A young man moves to Mumbai seeking a career and becomes entangled in the city's underworld while finding love.", "poster_url": "https://image.tmdb.org/t/p/w500/aKjMvD9wFzP9QeYwM2XcNqKj.jpg", "duration_min": 148, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 1999, "imdb_rating": 5.8, "trending": 61, "category": "Action"},
    {"title": "Priyamudan",                  "description": "An obsessive lover's possessiveness turns dangerous, leading to a gripping tale of passion and psychological turmoil.", "poster_url": "https://image.tmdb.org/t/p/w500/bD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 142, "genre": "Thriller", "language": "Tamil", "rating": "UA", "release_year": 1998, "imdb_rating": 6.9, "trending": 64, "category": "Thriller"},
    {"title": "Nilaave Vaa",                 "description": "A young software engineer falls in love with a traditional girl, but family honor and caste differences stand in their way.", "poster_url": "https://image.tmdb.org/t/p/w500/cD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 158, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1998, "imdb_rating": 5.6, "trending": 59, "category": "Romantic"},
    {"title": "Ninaithen Vandhai",           "description": "A man dreams of his future wife and sets out to find her, only to discover she already exists in real life.", "poster_url": "https://image.tmdb.org/t/p/w500/dQeYwM2XcNqKjMvD9wFzP9Qe.jpg", "duration_min": 155, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1998, "imdb_rating": 5.4, "trending": 58, "category": "Romantic"},
    {"title": "Love Today",                  "description": "Two young lovers face opposition from their families due to class differences in this romantic drama.", "poster_url": "https://image.tmdb.org/t/p/w500/eYwM2XcNqKjMvD9wFzP9QeYw.jpg", "duration_min": 148, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1997, "imdb_rating": 5.7, "trending": 57, "category": "Romantic"},
    {"title": "Nerrukku Ner",                "description": "Two friends turned bitter rivals fight over a woman they both love, leading to an intense emotional showdown.", "poster_url": "https://image.tmdb.org/t/p/w500/fM2XcNqKjMvD9wFzP9QeYwM2.jpg", "duration_min": 158, "genre": "Drama", "language": "Tamil", "rating": "U", "release_year": 1997, "imdb_rating": 6.4, "trending": 62, "category": "Drama"},
    {"title": "Once More",                   "description": "A happy-go-lucky young man discovers love and responsibility in this light-hearted romantic comedy.", "poster_url": "https://image.tmdb.org/t/p/w500/gXcNqKjMvD9wFzP9QeYwM2Xc.jpg", "duration_min": 145, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1997, "imdb_rating": 5.2, "trending": 55, "category": "Romantic"},

    # 1996–1994
    {"title": "Coimbatore Mappillai",        "description": "A village man from Coimbatore moves to the city and gets caught between two women who fall in love with him.", "poster_url": "https://image.tmdb.org/t/p/w500/hNqKjMvD9wFzP9QeYwM2XcNq.jpg", "duration_min": 143, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1996, "imdb_rating": 4.9, "trending": 52, "category": "Romantic"},
    {"title": "Selva",                       "description": "A college student falls in love with his professor's daughter while navigating the challenges of campus life.", "poster_url": "https://image.tmdb.org/t/p/w500/iMvD9wFzP9QeYwM2XcNqKjMv.jpg", "duration_min": 148, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1996, "imdb_rating": 4.8, "trending": 51, "category": "Romantic"},
    {"title": "Vasantha Vaasal",             "description": "A young man deals with love, family expectations, and village politics in this rural romantic drama.", "poster_url": "https://image.tmdb.org/t/p/w500/jQeYwM2XcNqKjMvD9wFzP9Qe.jpg", "duration_min": 145, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1996, "imdb_rating": 4.5, "trending": 49, "category": "Romantic"},
    {"title": "Maanbumigu Maanavan",         "description": "A college student fights against campus corruption and rowdyism while trying to complete his education.", "poster_url": "https://image.tmdb.org/t/p/w500/kD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 153, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 1996, "imdb_rating": 5.3, "trending": 53, "category": "Action"},
    {"title": "Chandralekha",                "description": "A twin brother and sister switch identities to solve a family crisis, leading to hilarious confusion.", "poster_url": "https://image.tmdb.org/t/p/w500/lFzP9QeYwM2XcNqKjMvD9wFz.jpg", "duration_min": 152, "genre": "Comedy", "language": "Tamil", "rating": "U", "release_year": 1995, "imdb_rating": 5.0, "trending": 50, "category": "Comedy"},
    {"title": "Vishnu",                      "description": "A wealthy man returns from abroad to reclaim his family business, facing challenges from a rival businessman.", "poster_url": "https://image.tmdb.org/t/p/w500/mP9QeYwM2XcNqKjMvD9wFzP9.jpg", "duration_min": 145, "genre": "Drama", "language": "Tamil", "rating": "U", "release_year": 1995, "imdb_rating": 4.8, "trending": 48, "category": "Drama"},
    {"title": "Rajavin Parvaiyile",          "description": "A story of friendship and love set against the backdrop of village life and class divides.", "poster_url": "https://image.tmdb.org/t/p/w500/nXcNqKjMvD9wFzP9QeYwM2Xc.jpg", "duration_min": 150, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1995, "imdb_rating": 5.0, "trending": 47, "category": "Romantic"},
    {"title": "Deva",                        "description": "A young man fights against injustice in his village, standing up to a tyrannical landlord who exploits the poor.", "poster_url": "https://image.tmdb.org/t/p/w500/oKjMvD9wFzP9QeYwM2XcNqKj.jpg", "duration_min": 148, "genre": "Action", "language": "Tamil", "rating": "UA", "release_year": 1995, "imdb_rating": 4.9, "trending": 46, "category": "Action"},
    {"title": "Rasigan",                     "description": "A young man's love story is complicated by his reputation as a troublemaker in his village.", "poster_url": "https://image.tmdb.org/t/p/w500/pQeYwM2XcNqKjMvD9wFzP9Qe.jpg", "duration_min": 147, "genre": "Romance", "language": "Tamil", "rating": "U", "release_year": 1994, "imdb_rating": 4.6, "trending": 44, "category": "Romantic"},
    {"title": "Sendhoorapandi",              "description": "Two brothers from a village find themselves on opposite sides of a bitter family feud over ancestral land.", "poster_url": "https://image.tmdb.org/t/p/w500/qMvD9wFzP9QeYwM2XcNqKjMv.jpg", "duration_min": 144, "genre": "Drama", "language": "Tamil", "rating": "U", "release_year": 1993, "imdb_rating": 4.8, "trending": 43, "category": "Drama"},
    {"title": "Naalaiya Theerpu",            "description": "Thalapathy Vijay's debut film — a college student stands up against a powerful family who wronged him and his mother.", "poster_url": "https://image.tmdb.org/t/p/w500/rD9wFzP9QeYwM2XcNqKjMvD9.jpg", "duration_min": 145, "genre": "Drama", "language": "Tamil", "rating": "UA", "release_year": 1992, "imdb_rating": 5.2, "trending": 42, "category": "Drama"},
]

# ──────────────────────────────────────────────
# Insert movies (skip if title already exists)
# ──────────────────────────────────────────────
existing_titles = {m[0] for m in db.query(Movie.title).all()}
inserted = 0
skipped = 0
inserted_movies = []

for m in vijay_movies:
    if m["title"] in existing_titles:
        skipped += 1
        continue
    movie = Movie(**m)
    db.add(movie)
    inserted_movies.append(movie)
    inserted += 1

db.flush()
print(f"Movies: {inserted} inserted, {skipped} skipped (already exist)")

# ──────────────────────────────────────────────
# Add showtimes for newly inserted movies
# ──────────────────────────────────────────────
theatres = db.query(Theatre).all()
screens = db.query(Screen).all()

if not theatres:
    print("WARNING: No theatres found. Run seed.py first to create theatres and screens.")
    db.commit()
    db.close()
    sys.exit(0)

base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
time_slots = [(10, 30), (14, 0), (18, 30), (22, 0)]

showtime_count = 0
for movie in inserted_movies:
    for day_offset in range(7):
        day = base_date + timedelta(days=day_offset)
        # Pick 2 different theatres per movie per day
        t1 = theatres[movie.id % len(theatres)]
        t2 = theatres[(movie.id + 5) % len(theatres)]

        for ti, theatre in enumerate([t1, t2]):
            # Pick 1-2 time slots per theatre
            slots = time_slots[day_offset % 2: day_offset % 2 + 2]
            if not slots:
                slots = [time_slots[0]]
            for slot in slots[:2]:
                start_time = day.replace(hour=slot[0], minute=slot[1])
                # Get a screen for this theatre
                theatre_screens = [s for s in screens if s.theatre_id == theatre.id]
                if not theatre_screens:
                    continue
                screen = theatre_screens[ti % len(theatre_screens)]

                # Check for time conflict on same screen
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

                db.add(Showtime(
                    movie_id=movie.id,
                    screen_id=screen.id,
                    start_time=start_time,
                    price=price,
                ))
                showtime_count += 1

db.commit()

print(f"Showtimes added: {showtime_count}")
print(f"Total Vijay movies in DB: {inserted + skipped}")
print("Done!")
db.close()
