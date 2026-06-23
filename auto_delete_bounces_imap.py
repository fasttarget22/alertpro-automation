#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"

print("""
╔═══════════════════════════════════════════════════════════╗
║  Auto-Delete Bounced Emails from Gmail                  ║
╚═══════════════════════════════════════════════════════════╝
""")

# Bounce keywords
BOUNCE_KEYWORDS = [
    "Address not found",
    "Delivery has failed",
    "Undeliverable",
    "Invalid recipient",
    "User doesn't exist",
    "No such user",
    "Mail delivery failed",
    "550 5.1.2",
    "550 5.7.1",
    "Postmaster"
]

try:
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    print("✅ Connected to Gmail IMAP")
    
    # Select inbox
    mail.select("INBOX")
    print("✅ Searching for bounced emails...")
    
    # Search for emails
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    
    deleted_count = 0
    checked_count = 0
    
    # Check each email
    for email_id in email_ids[-100:]:  # Check last 100 emails
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = msg.get("Subject", "")
        from_addr = msg.get("From", "")
        
        checked_count += 1
        
        # Check if bounce
        is_bounce = False
        for keyword in BOUNCE_KEYWORDS:
            if keyword.lower() in subject.lower() or keyword.lower() in from_addr.lower():
                is_bounce = True
                break
        
        # Delete if bounce
        if is_bounce:
            mail.store(email_id, '+FLAGS', '\\Deleted')
            deleted_count += 1
            print(f"🗑️  Deleted: {subject[:50]}")
    
    # Permanently delete
    mail.expunge()
    mail.close()
    mail.logout()
    
    print(f"\n✅ COMPLETE!")
    print(f"   Checked: {checked_count} emails")
    print(f"   Deleted: {deleted_count} bounces")
    print(f"   Inbox: CLEAN\n")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print(f"   Make sure IMAP is enabled in Gmail settings")
    print(f"   Go to: https://myaccount.google.com/security\n")
