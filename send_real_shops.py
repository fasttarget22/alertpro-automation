#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import time

SENDER_EMAIL = "alertprocctv@gmail.com"
SENDER_PASSWORD = "ltvo whwc chok lyez"

print("\n" + "="*60)
print("Sending to 89 REAL Smoke Shops")
print("="*60 + "\n")

# Load scraped shops
with open("real_smoke_shops_scraped.csv", "r") as f:
    reader = csv.DictReader(f)
    contacts = list(reader)

EMAIL_SUBJECT = "Quick question — do your smoke shop have 24/7 camera monitoring? 👀"
EMAIL_BODY = """Hi {company},

I'm reaching out because most smoke shops have cameras but no one watching them at night.

We just launched AlertPro CCTV — real trained operators monitor cameras 24/7 for just $150/month (no setup fee, no contracts).

Perfect for smoke shops, vape shops, hookah lounges — we protect retail and detect theft in real-time.

Worth a 10-minute call to see if it makes sense for {company}?

Best,
Shahadat
AlertPro CCTV
+971 56 646 8525
https://alertpro.appabbottabad.com"""

sent_count = 0
failed_count = 0

for i, contact in enumerate(contacts, 1):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = contact["email"]
        msg["Subject"] = EMAIL_SUBJECT
        
        body = EMAIL_BODY.format(company=contact["company"])
        msg.attach(MIMEText(body, "plain"))
        
        server.send_message(msg)
        sent_count += 1
        print(f"[{i}] ✅ {contact['company']}")
        server.quit()
        time.sleep(0.5)
        
    except Exception as e:
        failed_count += 1
        print(f"[{i}] ❌ {contact['company']}")

print(f"\n" + "="*60)
print(f"✅ COMPLETE!")
print(f"   Sent: {sent_count}/89")
print(f"   Failed: {failed_count}")
print(f"="*60 + "\n")

