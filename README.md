# Lab 1 – Extracting Data using the Google Play Store API

I used the google-play-scraper Python library to extract data on mental health & wellness AI applications from the Google Play Store, along with their user reviews, and stored everything in a JSON file.

## Applications search
I ran 27 search queries to find as many relevant apps as possible, and each query fetched up to 15 results with duplicates automatically removed.

## Reviews collection
For each app, I fetched reviews using all 3 available sort modes:
- Most Relevant
- Newest
- Rating

Each mode returned up to 200 reviews, and duplicates were removed using the unique reviewId. This gave a much richer and less biased dataset compared to using a single sort mode.

## Output
I extracted data from 179 applications with 38201 reviews collected. Everything was saved to mental_health_apps.json with the following structure:
- metadata : source, queries used, total apps and reviews count
- apps : full app details (title, developer, rating, installs, description…)
- reviews : for each app (reviewer name, comment text, score, date, thumbs up, developer reply…)

Note : I tried to upload the JSON file but since it exceeds GitHub's size limit for direct upload, I only uploaded a preview of its structure and content.
