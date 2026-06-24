#!/usr/bin/env python3
from datetime import datetime

print("\n" + "="*60)
print("CHECK EMAIL SENDING STATUS")
print("="*60 + "\n")

current_time = datetime.utcnow()
print(f"Current UTC Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Expected Send Time: 2026-06-24 08:00:00 UTC")

if current_time.hour >= 8:
    print(f"\n✅ Time is past 8 AM UTC - Emails SHOULD have been sent")
    print(f"⏳ GitHub Actions may still be processing (takes 1-5 minutes)")
    print(f"\nTO VERIFY:")
    print(f"1. Go to: https://github.com/fasttarget22/alertpro-automation")
    print(f"2. Click 'Actions' tab")
    print(f"3. Look for 'Daily Smoke Shop Emails (Real)' workflow")
    print(f"4. Check if it ran at 8:00 AM UTC")
else:
    print(f"\n⏳ Waiting for 8:00 AM UTC")

print("\n" + "="*60 + "\n")
