import json
import time
from google_play_scraper import search, app, reviews, Sort


# searching for mental health and wellness ai applications (with 27 different querys)
SEARCH_QUERIES = [
    "mental health AI",
    "AI therapy chatbot",
    "AI counseling app",
    "mental health chatbot",
    "AI emotional support",
    "anxiety relief app",
    "depression support app",
    "stress management app",
    "PTSD mental health app",
    "OCD therapy app",
    "bipolar disorder support app",
    "panic attack relief app",
    "wellness AI app",
    "meditation mindfulness AI",
    "mindfulness stress relief",
    "sleep anxiety app",
    "breathing relaxation app",
    "mood tracker mental health",
    "anxiety therapy AI",
    "CBT cognitive behavioral therapy app",
    "online therapy app",
    "self help therapy app",
    "psychotherapy mental wellness",
    "mental wellness self care",
    "emotional wellbeing app",
    "positive thinking mental health",
    "burnout stress recovery app",
]

print("Searching for mental health & wellness AI apps...")

app_ids_seen = set()
search_results = []

for query in SEARCH_QUERIES:
    try:
        results = search(query, lang="en", country="us", n_hits=15)
        for r in results:
            if r["appId"] not in app_ids_seen:
                app_ids_seen.add(r["appId"])
                search_results.append(r)
        print(f"✓ Query '{query}': {len(results)} results")
    except Exception as e:
        print(f"✗ Query '{query}' failed: {e}")
    time.sleep(1)

print(f"{len(search_results)} unique apps found across all queries")

# fetching full app details for each app
print("\nFetching full app details...")

apps_data = []
for r in search_results:
    try:
        details = app(r["appId"], lang="en", country="us")
        apps_data.append(details)
        print(f"✓ {details['title']}")
        time.sleep(0.5)
    except Exception as e:
        print(f"✗ Failed for {r['appId']}: {e}")

print(f"Fetched details for {len(apps_data)} apps")

# fetching reviws for each app 
print("\nFetching user reviews (Most Relevant + Newest + Rating)...")

SORT_MODES = [
    (Sort.MOST_RELEVANT, "Most Relevant"),
    (Sort.NEWEST,        "Newest"),
    (Sort.RATING,        "Rating"),
]

reviews_data = {}
for a in apps_data:
    aid = a["appId"]
    seen_review_ids = set()
    merged = []

    for sort_mode, sort_label in SORT_MODES:
        try:
            result, _ = reviews(
                aid,
                lang="en",
                country="us",
                sort=sort_mode,
                count=200,
            )
            new_count = 0
            for r in result:
                if r["reviewId"] not in seen_review_ids:
                    seen_review_ids.add(r["reviewId"])
                    merged.append(r)
                    new_count += 1
            print(f"[{sort_label}] +{new_count} new reviews")
            time.sleep(0.8)
        except Exception as e:
            print(f"[{sort_label}] failed: {e}")

    reviews_data[aid] = merged
    print(f"✓ {a['title']}: {len(merged)} total unique reviews\n")

#combining and saving to JSON
output = {
    "metadata": {
        "source": "Google Play Store via google-play-scraper",
        "search_queries": SEARCH_QUERIES,
        "total_apps": len(apps_data),
        "total_reviews": sum(len(v) for v in reviews_data.values()),
    },
    "apps": apps_data,
    "reviews": reviews_data,
}

output_path = "mental_health_apps.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2, default=str)

print(f"\nDone ! Data saved to: {output_path}")
print(f"Apps collected   : {output['metadata']['total_apps']}")
print(f"Reviews collected: {output['metadata']['total_reviews']}")