#!/usr/bin/env python3
import csv
from datetime import datetime

print("""
╔═══════════════════════════════════════════════════════════════╗
║  AlertPro CCTV — Google Sheets Auto-Creator (Simplified)    ║
╚═══════════════════════════════════════════════════════════════╝
""")

# Create CSV that can be imported to Google Sheets
tracking_data = []

# Add headers
headers = ["Date Sent", "Company", "Email", "State", "Email Opened", "Reply", "Phone Call", "Converted", "Notes"]
tracking_data.append(headers)

# Add sample rows for first 10 days (4000 emails)
from datetime import datetime, timedelta

base_date = datetime(2026, 6, 24)
sample_companies = [
    ("Smoke Shop - California Prime", "contact@cali1@gmail.com", "California"),
    ("Vapor Lounge - Texas Elite", "contact@texas1@gmail.com", "Texas"),
    ("Cigar Bar - New York Pro", "contact@ny1@gmail.com", "New York"),
    ("Hookah Lounge - Florida Master", "contact@florida1@gmail.com", "Florida"),
    ("Tobacco Store - Illinois Supreme", "contact@illinois1@gmail.com", "Illinois"),
]

row_num = 1
for day in range(10):
    date = base_date + timedelta(days=day)
    date_str = date.strftime("%Y-%m-%d")
    
    # Add 5 sample companies per day (in real scenario: 400)
    for company, email, state in sample_companies:
        row_num += 1
        tracking_data.append([
            date_str,           # Date Sent
            f"{company} #{row_num}",  # Company
            email,              # Email
            state,              # State
            "No",               # Email Opened (auto-fill later)
            "No",               # Reply
            "No",               # Phone Call
            "No",               # Converted
            ""                  # Notes
        ])

# Save as CSV for Google Sheets import
csv_filename = "AlertPro_Email_Tracking.csv"
with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(tracking_data)

print(f"\n✅ Created: {csv_filename}")
print(f"📊 Rows: {len(tracking_data)} (including header)")
print(f"📈 Sample data: First 10 days × 5 companies")
print(f"\nNow copy to Google Sheets:")
print(f"1. Go to: https://sheets.google.com/")
print(f"2. Click 'Blank spreadsheet'")
print(f"3. File → Import → Upload")
print(f"4. Select: {csv_filename}")
print(f"5. Click 'Import data'")
print(f"\nDone! Your tracking sheet is ready.\n")

# Also create formulas file
formulas_file = "Google_Sheets_Formulas.txt"
formulas_content = """
GOOGLE SHEETS SETUP INSTRUCTIONS
==================================

COLUMN FORMULAS (Add these to your sheet):

Column E - Email Opened (Auto-detect if reply or call):
=IF(OR(F2="Yes",G2="Yes"),"Yes","No")

Column H - Converted (Auto-detect if reply AND call):
=IF(AND(F2="Yes",G2="Yes"),"Yes","No")

SUMMARY SECTION (Add below your data):

Row below data + 2:
Total Emails: =COUNTA(B:B)-1
Total Opened: =COUNTIF(E:E,"Yes")
Total Replies: =COUNTIF(F:F,"Yes")
Total Calls: =COUNTIF(G:G,"Yes")
Total Converted: =COUNTIF(H:H,"Yes")
Conversion Rate: =COUNTIF(H:H,"Yes")/COUNTA(B:B)*100&"%"

DAILY WORKFLOW:

Morning (8 AM):
✅ 400 smoke shop emails sent automatically

Throughout Day:
✅ Gmail: Check for replies → Mark "Yes" in column F
✅ WhatsApp: Check messages → Mark "Yes" in column E
✅ Phone: Answer calls → Mark "Yes" in column G
✅ Sheet: Update tracking in real-time

Evening:
✅ Review metrics (Total Opened, Replies, Conversions)
✅ Plan next day follow-ups

EXPECTED DAILY RESULTS:
- 400 emails sent
- 80-120 opens (20-30%)
- 8-20 replies (2-5%)
- 2-6 conversions (20-30%)
- Revenue: $300-900/day

MONTHLY GOAL (30 days):
- 12,000 emails
- 2,400-3,600 opens
- 240-600 replies
- 48-180 conversions
- $7,200-27,000 revenue
"""

with open(formulas_file, "w") as f:
    f.write(formulas_content)

print(f"✅ Created: {formulas_file}")
print(f"📋 Contains all formulas and setup instructions\n")
