#!/usr/bin/env python3
import imaplib

print("Cleaning up bounces...\n")

mail = imaplib.IMAP4_SSL("imap.gmail.com", timeout=30)
mail.login("alertprocctv@gmail.com", "ltvo whwc chok lyez")
mail.select("INBOX")

# Search only for mailer-daemon (fastest method)
status, messages = mail.search(None, 'FROM "mailer-daemon"')
email_ids = messages[0].split()

print(f"Found: {len(email_ids)} bounces\n")

for i, email_id in enumerate(email_ids[:50], 1):  # Delete first 50
    mail.store(email_id, '+FLAGS', '\\Deleted')
    print(f"[{i}] Deleted")

mail.expunge()
mail.logout()
print(f"\n✅ Deleted {len(email_ids[:50])} bounces!")
