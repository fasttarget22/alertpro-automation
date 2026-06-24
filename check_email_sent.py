#!/usr/bin/env python3
import imaplib
from datetime import datetime

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"

print("\n" + "="*60)
print("CHECK IF EMAILS WERE SENT")
print("="*60 + "\n")

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com", timeout=10)
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    
    # Check sent folder
    mail.select("[Gmail]/Sent Mail")
    status, messages = mail.search(None, 'ALL')
    total_sent = len(messages[0].split())
    
    # Check today's sent
    today = datetime.utcnow().strftime("%d-Jun-%Y")
    status, today_msgs = mail.search(None, f'SINCE "{today}"')
    today_sent = len(today_msgs[0].split()) if today_msgs[0] else 0
    
    print(f"✅ Connected to Gmail")
    print(f"📧 Total emails ever sent: {total_sent}")
    print(f"📧 Emails sent TODAY (June 24): {today_sent}")
    
    if today_sent >= 400:
        print(f"\n🎉 SUCCESS! 400+ emails sent today!")
        print(f"✅ Campaign is LIVE!")
    elif today_sent > 0:
        print(f"\n⏳ {today_sent} emails sent so far")
        print(f"⏳ Still processing... GitHub Actions may be running")
    else:
        print(f"\n⏳ No emails sent yet")
        print(f"⏳ GitHub Actions may still be processing")
        print(f"⏳ Check again in 2-3 minutes")
    
    mail.logout()
    
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "="*60 + "\n")
