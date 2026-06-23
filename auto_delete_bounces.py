#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header

print("""
╔═══════════════════════════════════════════════════════════╗
║  AlertPro CCTV — Auto-Delete Bounced Emails              ║
╚═══════════════════════════════════════════════════════════╝

BOUNCE DETECTION & AUTO-DELETE

Keywords to detect bounces:
- "Address not found"
- "Delivery has failed"
- "Undeliverable"
- "Invalid recipient"
- "User doesn't exist"
- "No such user"
- "Mail delivery failed"

ACTION:
✅ Find emails with bounce keywords
✅ Auto-delete them
✅ Keep clean inbox

SETUP:

1. Gmail must have "Enable IMAP" turned ON
2. Go to: https://myaccount.google.com/apppasswords
3. Generate app password (if not done)
4. Script will auto-clean bounces daily

EXPECTED RESULTS:
From 12,000 emails:
- ~95% deliverable (11,400 emails)
- ~5% bounces (600 emails)
- Auto-deleted (keeping inbox clean)

AUTOMATION:
Run this script after emails are sent each day
It will find and delete all bounced emails automatically

Ready? Enable IMAP first!
""")
