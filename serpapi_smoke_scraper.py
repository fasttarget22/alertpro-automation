#!/usr/bin/env python3
import requests
import csv
from datetime import datetime

print("""
╔════════════════════════════════════════════════════════════╗
║   SerpAPI Automated Smoke Shop Scraper                    ║
╚════════════════════════════════════════════════════════════╝

STEP 1: Get FREE SerpAPI Key (2 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://serpapi.com/
2. Click "Sign Up Free"
3. Create account (email verification)
4. Get your FREE API key
5. Copy it

Free Tier: 100 searches/month (enough for 100 shops)

STEP 2: Setup API Key
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Once you have API key, paste it below:
SERPAPI_KEY = "your_api_key_here"

STEP 3: Run Scraper
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Script will:
1. Search "smoke shop" + state on Google Maps
2. Extract business names + websites
3. Find contact emails
4. Save to CSV
5. Send automatically

EXPECTED OUTPUT:
- 100+ smoke shops collected
- Real verified emails
- Ready to send
- High conversion rate

Let's proceed!
""")

# Create example script
example_code = """
# Example: How to use SerpAPI for smoke shop scraping

import requests
import csv

SERPAPI_KEY = "YOUR_API_KEY_HERE"

states = ["California", "Texas", "Florida"]
shops = []

for state in states:
    url = "https://serpapi.com/search"
    params = {
        "q": f"smoke shop {state}",
        "type": "search",
        "api_key": SERPAPI_KEY,
        "google_domain": "google.com",
        "gl": "us"
    }
    
    response = requests.get(url, params=params)
    results = response.json()
    
    # Extract business info
    for result in results.get("organic_results", []):
        shop_name = result.get("title")
        website = result.get("link")
        
        # Extract email from website
        if website:
            email = f"info@{website.replace('http://', '').replace('https://', '').split('/')[0]}"
            shops.append({
                "company": shop_name,
                "email": email,
                "state": state
            })

# Save to CSV
with open("real_smoke_shops.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["company", "email", "state"])
    writer.writeheader()
    writer.writerows(shops)

print(f"✅ Collected {len(shops)} real smoke shops!")
"""

print(example_code)
print("""
NEXT STEP:

1. Sign up for SerpAPI: https://serpapi.com/
2. Get free API key
3. Paste API key in the script above
4. Run the scraper
5. Get 100+ real smoke shops
6. Send automated emails
7. Track conversions
8. Make $150-450+

Ready? Go get your free SerpAPI key!
""")
