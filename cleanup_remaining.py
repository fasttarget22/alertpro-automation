#!/usr/bin/env python3
import imaplib

mail = imaplib.IMAP4_SSL("imap.gmail.com", timeout=30)
mail.login("alertprocctv@gmail.com", "ltvo whwc chok lyez")
mail.select("INBOX")

status, messages = mail.search(None, 'FROM "mailer-daemon"')
email_ids = messages[0].split()

print(f"Remaining bounces: {len(email_ids)}\n")

for i, email_id in enumerate(email_ids, 1):
    mail.store(email_id, '+FLAGS', '\\Deleted')
    if i % 50 == 0:
        print(f"[{i}] Deleted...")

mail.expunge()
mail.logout()
print(f"\n✅ All {len(email_ids)} remaining bounces deleted!\n")
