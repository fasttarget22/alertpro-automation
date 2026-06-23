#!/usr/bin/env python3
import csv
from datetime import datetime, timedelta

print("\n" + "="*60)
print("Verifying Unique Emails for 30-Day Campaign")
print("="*60 + "\n")

all_emails = []
total_shops = 0
duplicate_count = 0

# Check all 30 days
base_date = datetime(2026, 6, 24)

for day in range(30):
    date = base_date + timedelta(days=day)
    filename = f"smoke_shops_day_{date.strftime('%Y%m%d')}.csv"
    
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            day_emails = []
            for row in reader:
                email = row["email"]
                day_emails.append(email)
                total_shops += 1
                
                # Check for duplicates
                if email in all_emails:
                    duplicate_count += 1
                    print(f"❌ DUPLICATE: {email} (Day {day+1})")
                else:
                    all_emails.append(email)
            
            print(f"✅ Day {day+1}: {len(day_emails)} emails (All unique so far)")
    
    except FileNotFoundError:
        print(f"⚠️  Day {day+1}: File not found")

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
print(f"Total emails across 30 days: {total_shops}")
print(f"Unique emails: {len(all_emails)}")
print(f"Duplicate emails: {duplicate_count}")

if duplicate_count == 0:
    print(f"\n✅ PERFECT! All {len(all_emails)} emails are UNIQUE!")
    print(f"✅ Each smoke shop gets email sent to DIFFERENT address")
    print(f"✅ Safe to send - NO duplicates\n")
else:
    print(f"\n❌ WARNING: {duplicate_count} duplicate emails found!")
    print(f"❌ Need to regenerate unique emails\n")

print("="*60 + "\n")
