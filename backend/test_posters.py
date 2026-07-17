import subprocess, sys

# All poster URLs from seed.py
posters = [
    ("Leo", "/pQFoHvH3f8FU87hGNY6Q7dfO88F.jpg"),
    ("Vikram", "/8WRKBcHXPBzrKvKxKmqFVKTQtt9.jpg"),
    ("Amaran", "/6UxhTRgAmue0wIJbpWmbGHGs9Ar.jpg"),
    ("Dragon", "/zxDDBrXiBPHCu5OpQjS5gS0gSJv.jpg"),
    ("Good Night", "/3J0xM7UvTBKVe4CvSyjFvJ8AzhO.jpg"),
    ("Parking", "/2kCcgY1EKWdzF9oVSMDsE5DqJEa.jpg"),
    ("Lubber Pandhu", "/3uGgoXdMRzDANYYqsq6KlfNud8D.jpg"),
    ("Raayan", "/z9CfCXYGPlBZLZkq3WENKn3xTBL.jpg"),
    ("Thug Life", "/3KzrLWNrnZUKYjrrGltE2XjGsCG.jpg"),
    ("Avengers: Endgame", "/or06FN3Dka5tukK1e9sl16pB3iy.jpg"),
    ("Interstellar", "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"),
    ("The Batman", "/74xTEgt7R36Fpooo50r9T25onhq.jpg"),
    ("Oppenheimer", "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"),
    ("Inception", "/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg"),
    ("John Wick: Chapter 4", "/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg"),
    ("The Conjuring", "/ejrD1XjwLMI47qP3xrVygKyPrLu.jpg"),
    ("Titanic", "/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg"),
    ("Mission: Impossible", "/NNxYVw5z5ffJKyBJzHNJRnDIu.jpg"),
]

for title, path in posters:
    url = f"https://image.tmdb.org/t/p/w500{path}"
    result = subprocess.run(
        ["curl", "-s", "-o", "nul", "-w", "%{http_code}", url],
        capture_output=True, text=True
    )
    code = result.stdout.strip()
    status = "OK" if code == "200" else f"FAIL ({code})"
    print(f"{status} | {title} | {path}")
