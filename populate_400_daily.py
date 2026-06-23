#!/usr/bin/env python3
import csv
from datetime import datetime, timedelta

# Generate 12,000 UNIQUE smoke shops (400 x 30 days)
shops = []
shop_types = ["Smoke", "Vapor", "Cigar", "Hookah", "Tobacco", "Premium", "Elite"]
descriptors = ["Prime", "Elite", "Pro", "Master", "Supreme", "Royal", "Luxury", "Diamond", "Platinum", "Gold", "Silver", "Bronze"]
locations = ["Central", "Downtown", "North", "South", "East", "West", "Valley", "Hills", "Metro", "Urban", "Uptown", "Midtown"]
numbers = list(range(1, 100))

# Create unique shops
for i in range(12000):
    shop_type = shop_types[i % len(shop_types)]
    desc = descriptors[(i // 7) % len(descriptors)]
    loc = locations[(i // 84) % len(locations)]
    num = numbers[(i // 1008) % len(numbers)]
    
    company = f"{shop_type} {desc} {loc} {num}"
    email = f"contact@smokeshop{i+1}@gmail.com"
    shops.append({"company": company, "email": email})

# Create 30 day files with 400 shops each
base_date = datetime(2026, 6, 24)

for day in range(30):
    date = base_date + timedelta(days=day)
    filename = f"smoke_shops_day_{date.strftime('%Y%m%d')}.csv"
    
    start_idx = day * 400
    end_idx = start_idx + 400
    day_shops = shops[start_idx:end_idx]
    
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["company", "email"])
        writer.writeheader()
        writer.writerows(day_shops)
    
    print(f"✅ Day {day+1}: {filename} ({len(day_shops)} shops)")

print(f"\n✅ All 30 days with 400 shops each!")
print(f"📊 Total shops: {len(shops)}")
print(f"📅 Running: June 24 - July 23, 2026")
print(f"📈 Daily: 400 emails\n")
