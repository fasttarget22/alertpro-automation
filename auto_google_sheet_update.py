#!/usr/bin/env python3
import csv
from datetime import datetime, timedelta

print("""
╔═════════════════════════════════════════════════════════════╗
║  Automated Google Sheet Tracking System                    ║
╚═════════════════════════════════════════════════════════════╝

SOLUTION: Auto-generate daily tracking CSV

HOW IT WORKS:
1. Each day at 8 AM → 400 emails sent
2. Script creates daily tracking file
3. You upload to Google Sheet
4. Formulas auto-calculate results

SETUP:
""")

# Create daily tracking template
base_date = datetime(2026, 6, 24)

for day in range(1, 31):
    date = base_date + timedelta(days=day-1)
    date_str = date.strftime("%Y-%m-%d")
    filename = f"tracking_day{day}_{date_str}.csv"
    
    with open(filename, "w", newline="") as f:
        f.write("Date Sent,Company,Email,State,Email Opened,Reply,Phone Call,Converted,Notes\n")
        
        # Add sample rows (you'll fill in replies later)
        for i in range(1, 11):  # 10 sample rows per day
            f.write(f"{date_str},Smoke Shop {i},{date_str}-shop{i}@gmail.com,CA,No,No,No,No,\n")
    
    print(f"✅ Day {day}: Created {filename}")

print(f"""
✅ Created tracking files for all 30 days!

GOOGLE SHEET FORMULAS - ADD THESE:

Row 2 (Auto-detect Email Opened):
E2: =IF(OR(F2="Yes",G2="Yes"),"Yes","No")

Row 2 (Auto-detect Converted):
H2: =IF(AND(F2="Yes",G2="Yes"),"Yes","No")

SUMMARY SECTION (Add at bottom):

A32: DAILY SUMMARY
A33: Total Sent
B33: =COUNTA(B2:B31)

A34: Total Opened
B34: =COUNTIF(E2:E31,"Yes")

A35: Total Replies
B35: =COUNTIF(F2:F31,"Yes")

A36: Total Calls
B36: =COUNTIF(G2:G31,"Yes")

A37: Total Converted
B37: =COUNTIF(H2:H31,"Yes")

A38: Conversion Rate
B38: =IF(B33=0,0,B37/B33*100)&"%"

DAILY WORKFLOW:

Morning (8 AM):
✅ 400 emails sent automatically
✅ tracking_day1_2026-06-24.csv created

Throughout Day:
✅ Check Gmail for replies
✅ Add company name to sheet
✅ Mark "Yes" in Reply column
✅ Formulas auto-calculate

Evening:
✅ Review metrics
✅ Plan next day

Ready? Setup formulas in your sheet now!
""")
