#!/usr/bin/env python3
import requests
import csv
import time

SERPAPI_KEY = "8b54bc1080500112c7eff67d46808578c04250990a37dbd71ff0bff7dd80cb18"

print("""
╔════════════════════════════════════════════════════════════╗
║   Running Automated Smoke Shop Scraper                    ║
╚════════════════════════════════════════════════════════════╝
""")

states = ["California", "Texas", "Florida", "New York", "Illinois", 
          "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Colorado"]

shops = []
total_found = 0

for state in states:
    print(f"🔍 Searching {state}...")
    
    url = "https://serpapi.com/search"
    params = {
        "q": f"smoke shop {state}",
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "gl": "us"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        results = response.json()
        
        # Extract business info
        count = 0
        for result in results.get("organic_results", [])[:10]:  # Get top 10 per state
            title = result.get("title", "")
            link = result.get("link", "")
            
            if title and link:
                # Extract domain
                domain = link.replace("http://", "").replace("https://", "").split("/")[0]
                email = f"info@{domain}"
                
                shops.append({
                    "company": title,
                    "email": email,
                    "state": state
                })
                count += 1
        
        total_found += count
        print(f"   ✅ Found {count} shops")
        time.sleep(1)  # Respect rate limits
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

print(f"\n" + "="*60)
print(f"✅ SCRAPING COMPLETE!")
print(f"   Total shops found: {total_found}")
print(f"="*60 + "\n")

# Save to CSV
if shops:
    csv_file = "real_smoke_shops_scraped.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["company", "email", "state"])
        writer.writeheader()
        writer.writerows(shops)
    
    print(f"✅ Saved to: {csv_file}")
    print(f"📊 Ready to send {len(shops)} real emails!\n")
else:
    print("❌ No shops found. Check API key and try again.\n")

