#!/usr/bin/env python3
import imaplib
import email

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"

print("""
╔═══════════════════════════════════════════════════════════╗
║  Auto-Delete Bounced Emails - Move to Trash              ║
╚═══════════════════════════════════════════════════════════╝
""")

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
    "Postmaster",
    "Returned mail"
]

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    print("✅ Connected to Gmail")
    
    mail.select("INBOX")
    print("✅ Searching for bounces in INBOX...")
    
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    
    deleted_count = 0
    
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = msg.get("Subject", "")
        from_addr = msg.get("From", "")
        
        is_bounce = False
        for keyword in BOUNCE_KEYWORDS:
            if keyword.lower() in subject.lower() or keyword.lower() in from_addr.lower():
                is_bounce = True
                break
        
        if is_bounce:
            # Move to Trash (Gmail label: [Gmail]/Trash)
            mail.copy(email_id, '[Gmail]/Trash')
            mail.store(email_id, '+FLAGS', '\\Deleted')
            deleted_count += 1
            print(f"🗑️  Moved to Trash: {subject[:50]}")
    
    mail.expunge()
    mail.close()
    mail.logout()
    
    print(f"\n✅ COMPLETE!")
    print(f"   Deleted: {deleted_count} bounce emails")
    print(f"   Status: All moved to Trash\n")
    
except Exception as e:
    print(f"❌ Error: {str(e)}\n")
