import asyncio
import httpx

async def test_tmdb():
    async with httpx.AsyncClient() as client:
        # Test with Leo (2023 Tamil)
        r = await client.get("https://api.themoviedb.org/3/search/movie", params={
            "api_key": "2dca580c2a14b55200e784d157207b4d",
            "query": "Leo",
            "year": 2023,
        }, timeout=10)
        print("Status:", r.status_code)
        if r.status_code == 200:
            data = r.json()
            results = data.get("results", [])
            print("Results count:", len(results))
            for item in results[:3]:
                print(f"  - {item.get('title')} ({item.get('release_date')}) poster: {item.get('poster_path')}")
        else:
            print("Error body:", r.text[:500])

        # Also try Vikram
        r2 = await client.get("https://api.themoviedb.org/3/search/movie", params={
            "api_key": "2dca580c2a14b55200e784d157207b4d",
            "query": "Vikram",
            "year": 2022,
        }, timeout=10)
        print("\nVikram search:")
        print("Status:", r2.status_code)
        if r2.status_code == 200:
            data = r2.json()
            for item in data.get("results", [])[:2]:
                print(f"  - {item.get('title')} ({item.get('release_date')}) poster: {item.get('poster_path')}")

        # Try English movie
        r3 = await client.get("https://api.themoviedb.org/3/search/movie", params={
            "api_key": "2dca580c2a14b55200e784d157207b4d",
            "query": "Inception",
            "year": 2010,
        }, timeout=10)
        print("\nInception search:")
        print("Status:", r3.status_code)
        if r3.status_code == 200:
            for item in r3.json().get("results", [])[:2]:
                print(f"  - {item.get('title')} ({item.get('release_date')}) poster: {item.get('poster_path')}")

        # Test downloading an image
        test_path = "/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg"
        r4 = await client.get(f"https://image.tmdb.org/t/p/w500{test_path}", timeout=10)
        print(f"\nImage download ({test_path}): Status {r4.status_code}, Size {len(r4.content)} bytes")

asyncio.run(test_tmdb())
