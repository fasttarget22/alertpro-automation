#!/usr/bin/env python3

print("""
╔════════════════════════════════════════════════════════════╗
║   AlertPro CCTV — Google Sheet Auto-Setup                 ║
╚════════════════════════════════════════════════════════════╝

Your Google Sheet URL:
https://docs.google.com/spreadsheets/d/16rIb_sPhHWcQZWxMlt4XuY5nVeGOdjZXFzms4n_tHwY/edit

MANUAL SETUP (5 minutes):

ROW 1 - HEADERS:
A1: Date Sent
B1: Company
C1: Email
D1: State
E1: Email Opened
F1: Reply
G1: Phone Call
H1: Converted
I1: Notes

ROW 2+ - FORMULAS:
E2: =IF(OR(F2="Yes",G2="Yes"),"Yes","No")
H2: =IF(AND(F2="Yes",G2="Yes"),"Yes","No")

BOTTOM - SUMMARY (After all data):
A25: SUMMARY
A26: Total Emails
B26: =COUNTA(B:B)-1
A27: Total Opened
B27: =COUNTIF(E:E,"Yes")
A28: Total Replies
B28: =COUNTIF(F:F,"Yes")
A29: Total Calls
B29: =COUNTIF(G:G,"Yes")
A30: Total Converted
B30: =COUNTIF(H:H,"Yes")
A31: Conversion Rate
B31: =B30/B26*100&"%"

DAILY WORKFLOW:

1. Check Gmail for replies
2. Open Google Sheet
3. Add company name + mark "Yes" in Reply
4. Sheet auto-calculates totals
5. Done!

EXPECTED FIRST WEEK:

Day 1: 400 emails sent
Day 2: 80-120 opens
Day 3: 8-20 replies (start adding to sheet)
Day 4-7: More replies, track conversions

Ready? Open your sheet and add headers now!
""")
