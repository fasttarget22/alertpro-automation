#!/usr/bin/env python3
import imaplib
import email
from datetime import datetime

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"

print("""
╔═════════════════════════════════════════════════════════════╗
║  Daily Inbox Cleanup - Remove All Bounces                 ║
╚═════════════════════════════════════════════════════════════╝
""")

BOUNCE_SENDERS = [
    "mailer-daemon",
    "postmaster",
    "Mail Delivery",
    "Undeliverable"
]

try:
    print("🔌 Connecting...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    print("✅ Connected to Gmail\n")
    
    mail.select("INBOX")
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    
    if not email_ids:
        print("✅ Inbox is empty")
        mail.logout()
        exit()
    
    print(f"📊 Scanning {len(email_ids)} emails...\n")
    
    deleted = 0
    for email_id in email_ids:
        try:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject = str(msg.get("Subject", "")).lower()
            from_addr = str(msg.get("From", "")).lower()
            
            # Check for bounces
            is_bounce = any(keyword.lower() in subject or keyword.lower() in from_addr 
                          for keyword in BOUNCE_SENDERS)
            
            if is_bounce:
                mail.store(email_id, '+FLAGS', '\\Deleted')
                deleted += 1
                print(f"🗑️  Deleted bounce #{deleted}")
        except:
            pass
    
    mail.expunge()
    mail.close()
    mail.logout()
    
    print(f"\n✅ CLEANUP COMPLETE!")
    print(f"   Deleted: {deleted} bounce emails")
    print(f"   Inbox: CLEAN\n")
    
except Exception as e:
    print(f"❌ Error: {e}\n")
