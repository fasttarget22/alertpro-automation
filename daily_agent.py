import csv, smtplib, imaplib, time, os, re, random, socket
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bs4 import BeautifulSoup
from googlesearch import search

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"
SENT_FILE = "data/sent_log.csv"
TARGET = 20

CITIES = [
    "Los Angeles CA","Houston TX","Miami FL","Chicago IL",
    "Phoenix AZ","Philadelphia PA","Dallas TX","San Diego CA",
    "Jacksonville FL","Austin TX","Columbus OH","Charlotte NC",
    "Denver CO","Nashville TN","Las Vegas NV","Portland OR",
    "Memphis TN","Louisville KY","Baltimore MD","Milwaukee WI",
    "Atlanta GA","Detroit MI","Seattle WA","Boston MA",
    "New Orleans LA","Cleveland OH","Tampa FL","Orlando FL",
    "Kansas City MO","Raleigh NC","Pittsburgh PA","Cincinnati OH"
]

SUBJECTS = [
    "Quick question about your smoke shop security",
    "Are your cameras actually being watched at night?",
    "Stop theft before it happens - $150/month",
    "24/7 camera monitoring for smoke shops",
    "Protect your smoke shop from theft tonight"
]

BODY = """Hi {company},

I noticed most smoke shops have cameras but nobody watching them at night.

We offer AlertPro CCTV monitoring:
- Real trained operators watching 24/7
- Instant alerts within 60 seconds
- Full incident documentation
- Only $150/month (no setup fee, no contracts)
- 60% cheaper than a security guard

Would you be open to a quick 10-minute call?

Best regards,
Shahadat
AlertPro CCTV Eagle Eyes
+971 56 646 8525
https://alertpro.appabbottabad.com
WhatsApp: https://wa.me/971566468525"""

SKIP_DOMAINS = [
    "yelp.com","google.com","facebook.com","instagram.com","twitter.com",
    "linkedin.com","yellowpages.com","tripadvisor.com","foursquare.com",
    "wix.com","squarespace.com","wordpress.com","shopify.com","godaddy.com",
    "amazonaws.com","sentry.io","indeed.com","ziprecruiter.com","bbb.org",
    "thumbtack.com","groupon.com","angi.com","mapquest.com","whitepages.com",
    "superpages.com","manta.com","zoominfo.com","leadiq.com","datanyze.com",
    "datacaptive.com","openmart.com","rentechdigital.com","neverbounce.com",
    "abc.com","nbc.com","cbs.com","cnn.com","fox.com","tmj4.com",
    "domain.com","yoursite.com","example.com","test.com","vaping.com",
    "wixpress.com","provape.com","lung.org","phmc.org",
    "healthline.com","webmd.com","reddit.com","pinterest.com","youtube.com",
    "amazon.com","ebay.com","walmart.com","target.com","wikihow.com"
]

def domain_exists(domain):
    try:
        socket.getaddrinfo(domain, None, socket.AF_INET)
        return True
    except:
        return False

def is_valid_email(email):
    email = email.strip().lower().rstrip(".")
    if not email: return False
    if "www." in email: return False
    if email.count("@") != 1: return False
    fake = ["user@domain","name@your","test@test","example@",
            "noreply","no-reply","donotreply","bounce","mailer",
            "daemon","postmaster","abuse","spam","wixpress",
            "sentry","yoursite","@domain.","placeholder"]
    if any(f in email for f in fake): return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email): return False
    domain = email.split("@")[1].lower()
    if domain.startswith("www."): return False
    if ".gov" in domain: return False
    if ".edu" in domain: return False
    if any(s in domain for s in SKIP_DOMAINS): return False
    if len(domain) < 5: return False
    return True

def score_email(email):
    prefix = email.split("@")[0].lower()
    domain = email.split("@")[1].lower()
    score = 0
    if "gmail.com" in domain: score += 3
    if "yahoo.com" in domain: score += 2
    if "hotmail.com" in domain: score += 1
    if "aol.com" in domain: score += 1
    good = ["info","contact","hello","owner","manager","sales","admin","support"]
    if any(p == prefix for p in good): score += 5
    if any(p in prefix for p in good): score += 2
    smoke = ["smoke","vape","vapor","cigar","tobacco","hookah","hemp","cloud","puff","pipe"]
    if any(k in domain for k in smoke): score += 10
    if any(k in prefix for k in smoke): score += 5
    return score

def extract_emails(text):
    found = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    valid = []
    for e in found:
        e = e.lower().strip().rstrip(".")
        if is_valid_email(e) and e not in valid:
            valid.append(e)
    valid.sort(key=score_email, reverse=True)
    return valid

def get_email_from_website(url):
    try:
        if any(s in url.lower() for s in SKIP_DOMAINS): return None
        if ".gov" in url or ".edu" in url: return None
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        emails = extract_emails(resp.text)
        # Find contact page
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if any(k in href for k in ["contact","about"]):
                if href.startswith("http"):
                    cu = href
                elif href.startswith("/"):
                    cu = "/".join(url.split("/")[:3]) + href
                else: continue
                try:
                    r2 = requests.get(cu, headers=headers, timeout=6)
                    emails.extend(extract_emails(r2.text))
                except: pass
                break
        # Return best scored email
        emails.sort(key=score_email, reverse=True)
        for e in emails:
            if score_email(e) >= 2:
                return e
        return None
    except:
        return None

def load_sent():
    sent = set()
    os.makedirs("data", exist_ok=True)
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            for row in csv.DictReader(f):
                sent.add(row["email"].lower().strip())
    print(f"Already sent: {len(sent)} (skipping)")
    return sent

def save_sent(c, e, s, st):
    new = not os.path.exists(SENT_FILE)
    with open(SENT_FILE, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date","company","email","state","status"])
        if new: w.writeheader()
        w.writerow({"date":datetime.now().strftime("%Y-%m-%d"),
                    "company":c,"email":e,"state":s,"status":st})

def find_real_leads(city, sent, session_sent):
    print(f"\nSearching {city}...")
    leads = []
    try:
        urls = list(search(f"smoke shop {city}", num_results=10, lang="en"))
        for url in urls:
            if len(leads) >= 2: break
            if any(s in url.lower() for s in SKIP_DOMAINS): continue
            if ".gov" in url or ".edu" in url: continue
            domain = url.split("/")[2].replace("www.","").lower()
            # DNS check
            if not domain_exists(domain):
                print(f"  SKIP (no DNS): {domain}")
                continue
            # Get email
            email = get_email_from_website(url)
            if not email:
                print(f"  SKIP (no email): {domain}")
                continue
            if email in sent or email in session_sent:
                print(f"  SKIP (duplicate): {email}")
                continue
            company = domain.split(".")[0].replace("-"," ").title()
            leads.append({
                "company": company[:50],
                "email": email,
                "state": city.split()[-1],
                "score": score_email(email)
            })
            session_sent.add(email)
            print(f"  REAL: {company} -> {email} (score:{score_email(email)})")
        time.sleep(3)
    except Exception as e:
        print(f"  Error: {str(e)[:50]}")
        time.sleep(5)
    return leads

def send_email(company, email):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        s.starttls()
        s.login(GMAIL_USER, GMAIL_PASSWORD)
        msg = MIMEMultipart()
        msg["From"] = f"Shahadat - AlertPro CCTV <{GMAIL_USER}>"
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
        for kw in [
            'FROM "mailer-daemon"','FROM "Mail Delivery Subsystem"',
            'FROM "postmaster"','SUBJECT "Delivery Status Notification"',
            'SUBJECT "Delivery incomplete"','SUBJECT "Message not delivered"',
            'SUBJECT "Undeliverable"','SUBJECT "Failure Notice"'
        ]:
            try:
                _, msgs = m.search(None, kw)
                for i in msgs[0].split():
                    m.store(i, "+FLAGS", "\\Deleted")
                    total += 1
            except: pass
        m.expunge()
        m.logout()
        print(f"Cleaned {total} bounces")
    except: pass

def main():
    print("="*60)
    print(f"AlertPro Agent - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Target: {TARGET} REAL verified emails only")
    print("="*60)
    sent = load_sent()
    session_sent = set()
    leads = []
    cities = CITIES.copy()
    random.shuffle(cities)
    for city in cities:
        if len(leads) >= TARGET: break
        leads.extend(find_real_leads(city, sent, session_sent))
    leads.sort(key=lambda x: x.get("score",0), reverse=True)
    print(f"\nFound {len(leads)} real verified leads")
    sent_count = 0
    for i, lead in enumerate(leads[:TARGET], 1):
        email = lead["email"].strip().rstrip(".")
        if send_email(lead["company"], email):
            sent_count += 1
            save_sent(lead["company"], email, lead["state"], "sent")
            print(f"[{i}] SENT: {lead['company'][:30]} -> {email}")
        else:
            save_sent(lead["company"], email, lead["state"], "failed")
            print(f"[{i}] FAIL: {email}")
        time.sleep(2)
    print(f"\nSent: {sent_count} real emails today")
    clean_bounces()
    print("DONE!")

if __name__ == "__main__":
    main()
