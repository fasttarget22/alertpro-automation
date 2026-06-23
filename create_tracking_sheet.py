#!/usr/bin/env python3

print("""
╔════════════════════════════════════════════════════════════════╗
║   AlertPro CCTV — Google Sheets Email Tracking Template      ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: Go to Google Sheets
URL: https://sheets.google.com/

STEP 2: Click "Blank spreadsheet"

STEP 3: Create columns (A-H):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Date Sent | Company | Email | State | Email Opened | Reply | Phone Call | Converted |

STEP 4: Add sample data rows:

Row 1 (Headers):
A1: Date Sent
B1: Company
C1: Email
D1: State
E1: Email Opened
F1: Reply
G1: Phone Call
H1: Converted

Row 2 (Sample):
A2: 2026-06-24
B2: Smoke Shop - California Prime
C2: contact@california1@gmail.com
D2: California
E2: No
F2: No
G2: No
H2: No

STEP 5: Set up tracking formulas:

In column E (Email Opened):
- Mark "Yes" when you see a reply or phone call
- Auto-populate based on other columns

In column H (Converted):
- Mark "Yes" when they commit to service
- Use formula: =IF(AND(F2="Yes", G2="Yes"), "Yes", "No")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 6: Share with yourself
- File → Share
- Add your email
- Get link to access anywhere

STEP 7: Update daily
- Add new rows for each day's 400 emails
- Mark "Yes" when they reply or call
- Track conversions in column H

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXPECTED TRACKING:

Day 1 (June 24): 400 emails sent
  → Day 3-5: Replies start coming in
  → Mark "Yes" in columns E, F, G as they respond
  → Day 7: Send Email 2 to non-responders
  → Day 15+: Close deals (mark H as "Yes")

FORMULAS TO USE:

Total Opened: =COUNTIF(E:E,"Yes")
Total Replies: =COUNTIF(F:F,"Yes")
Total Calls: =COUNTIF(G:G,"Yes")
Total Converted: =COUNTIF(H:H,"Yes")
Conversion Rate: =COUNTIF(H:H,"Yes")/COUNTA(B:B)*100&"%"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DAILY WORKFLOW:

Morning (8 AM):
  ✅ 400 emails sent automatically

Throughout day:
  ✅ Check Gmail for replies
  ✅ Add company name to tracking sheet
  ✅ Mark "Yes" in Email Opened column
  ✅ Log phone calls
  ✅ Track which ones convert

Evening:
  ✅ Review metrics
  ✅ Plan follow-ups

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready? Create your Google Sheet now!
""")
