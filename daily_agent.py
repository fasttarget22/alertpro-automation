import requests, csv, smtplib, imaplib, time, os, re, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"
SERPAPI_KEY = "8b54bc1080500112c7eff67d46808578c04250990a37dbd71ff0bff7dd80cb18"
SENT_FILE = "data/sent_log.csv"
TARGET = 90

STATES = ["California","Texas","Florida","New York","Illinois","Pennsylvania","Ohio","Georgia","North Carolina","Colorado","Arizona","Nevada","Michigan","Washington","Virginia","Tennessee","Indiana","Missouri","Maryland","Wisconsin"]
SUBJECTS = ["Quick question - do your smoke shop have 24/7 camera monitoring?","Are your cameras actually being watched at night?","Stop theft before it happens - $150/month"]
BODY = """Hi {company},

Most smoke shops have cameras but no one watching at night.

AlertPro CCTV - real operators monitor 24/7 for $150/month. No setup, no contracts.

- Live 24/7 monitoring
- Alerts within 60 seconds
- 60% cheaper than security guards

Worth a 10-minute call?

Shahadat
AlertPro CCTV
+971 56 646 8525
https://alertpro.appabbottabad.com"""

def load_sent():
    sent = set()
    os.makedirs("data", exist_ok=True)
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            for row in csv.DictReader(f):
                sent.add(row["email"].lower())
    print(f"Already sent: {len(sent)} skipping")
    return sent

def save_sent(c, e, s, st):
    new = not os.path.exists(SENT_FILE)
    with open(SENT_FILE, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date","company","email","state","status"])
        if new: w.writeheader()
        w.writerow({"date":datetime.now().strftime("%Y-%m-%d"),"company":c,"email":e,"state":s,"status":st})

def extract_emails(text):
    skip = ["example","sentry","wixpress","godaddy","amazonaws","fountmedia","bloyal","facebook","instagram","yelp","google","indeed","shopify","squarespace","wordpress"]
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return list(set(e.lower() for e in emails if not any(s in e.lower() for s in skip)))

def find_leads(state, sent):
    print(f"Searching {state}...")
    leads = []
    for q in [f"smoke shop {state} email", f"vape shop {state} contact"]:
        if len(leads) >= 5: break
        try:
            r = requests.get("https://serpapi.com/search", params={"q":q,"api_key":SERPAPI_KEY,"engine":"google"}, timeout=15)
            for res in r.json().get("organic_results", [])[:5]:
                for email in extract_emails(res.get("snippet","")+res.get("title",""))[:1]:
                    if email not in sent and email not in [l["email"] for l in leads]:
                        leads.append({"company":res.get("title","Shop")[:50],"email":email,"state":state})
        except: pass
        time.sleep(1)
    print(f"  Found {len(leads)}")
    return leads

def send_email(company, email):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        s.starttls()
        s.login(GMAIL_USER, GMAIL_PASSWORD)
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = email
        msg["Subject"] = random.choice(SUBJECTS)
        msg.attach(MIMEText(BODY.format(company=company), "plain"))
        s.send_message(msg)
        s.quit()
        return True
    except: return False

def clean_bounces():
    try:
        m = imaplib.IMAP4_SSL("imap.gmail.com", timeout=30)
        m.login(GMAIL_USER, GMAIL_PASSWORD)
        m.select("INBOX")
        total = 0
        for kw in ['FROM "mailer-daemon"','FROM "postmaster"','FROM "Mail Delivery"']:
            _, msgs = m.search(None, kw)
            for i in msgs[0].split():
                m.store(i, "+FLAGS", "\\Deleted")
                total += 1
        m.expunge()
        m.logout()
        print(f"Cleaned {total} bounces")
    except: pass

def main():
    print(f"AlertPro Agent - {datetime.now().strftime('%Y-%m-%d')}")
    sent = load_sent()
    leads = []
    random.shuffle(STATES)
    for state in STATES:
        if len(leads) >= TARGET: break
        leads.extend(find_leads(state, sent))
    sent_count = 0
    for i, lead in enumerate(leads[:TARGET], 1):
        if send_email(lead["company"], lead["email"]):
            sent_count += 1
            save_sent(lead["company"], lead["email"], lead["state"], "sent")
            print(f"[{i}] OK: {lead['company'][:30]}")
        else:
            save_sent(lead["company"], lead["email"], lead["state"], "failed")
        time.sleep(2)
    print(f"Sent: {sent_count}")
    clean_bounces()
    print("DONE!")

if __name__ == "__main__":
    main()
