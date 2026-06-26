import requests, csv, smtplib, imaplib, time, os, re, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bs4 import BeautifulSoup

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"
SERPAPI_KEY = "8b54bc1080500112c7eff67d46808578c04250990a37dbd71ff0bff7dd80cb18"
SENT_FILE = "data/sent_log.csv"
TARGET = 90

STATES = [
    "California","Texas","Florida","New York","Illinois",
    "Pennsylvania","Ohio","Georgia","North Carolina","Colorado",
    "Arizona","Nevada","Michigan","Washington","Virginia",
    "Tennessee","Indiana","Missouri","Maryland","Wisconsin",
    "Minnesota","Oregon","Oklahoma","Kentucky","Louisiana",
    "Alabama","South Carolina","Utah","Iowa","Arkansas"
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

# Complete skip list
SKIP_DOMAINS = [
    # Directories
    "yelp.com","google.com","facebook.com","instagram.com","twitter.com",
    "linkedin.com","yellowpages.com","tripadvisor.com","foursquare.com",
    "wix.com","squarespace.com","wordpress.com","shopify.com","godaddy.com",
    "amazonaws.com","sentry.io","fountmedia.com","bloyal.com","indeed.com",
    "ziprecruiter.com","glassdoor.com","bbb.org","thumbtack.com","groupon.com",
    "angi.com","houzz.com","nextdoor.com","patch.com","citysearch.com",
    "mapquest.com","whitepages.com","spokeo.com","yellowbook.com",
    "superpages.com","manta.com","chamberofcommerce.com","dandb.com",
    "bizapedia.com","opencorporates.com","merchantcircle.com","hotfrog.com",
    "2findlocal.com","local.com","ezlocal.com","brownbook.net",
    # News sites
    "abc.com","nbc.com","cbs.com","cnn.com","fox.com","tmj4.com",
    "wjhl.com","wkrn.com","wbaltv.com","abc7ny.com","wtaj.com",
    "arkansasonline.com","myarklamiss.com","dcnewsnow.com",
    # Government
    "fcc.gov","epa.gov","fda.gov","cdc.gov","hhs.gov","irs.gov",
    "state.mn.us","state.tn.gov","maryland.gov","ohio.gov","pa.gov",
    "in.gov","wa.gov","lcb.wa.gov","atc.in.gov","dfa.arkansas.gov",
    "adh.tpcp","lung.org","phmc.org","dcwp.nyc.gov",
    # Data companies
    "datacaptive.com","zoominfo.com","leadiq.com","rentechdigital.com",
    "neverbounce.com","datanyze.com","openmart.com","ambientech.org",
    # Fake/placeholder
    "domain.com","yoursite.com","example.com","test.com",
    "sentry-next.wixpress.com","wixpress.com",
    # Vaping generic (sent too many times)
    "vaping.com","provape.com",
    # Press/media
    "pointrobertspress.com","thenorthernlight.com","messagemedia.co",
    # Stoops NYC (not a smoke shop)
    "stoopsnyc.com",
]

GOOD_PREFIXES = ["info","contact","hello","owner","manager","sales",
                 "admin","support","shop","store","business","hello"]

def is_valid_email(email):
    email = email.strip().lower().rstrip(".")
    if not email: return False
    if "www." in email: return False
    if email.count("@") != 1: return False
    # Block fake placeholder emails
    fake = ["user@domain","name@your","test@test","example@",
            "noreply","no-reply","donotreply","bounce","mailer",
            "daemon","postmaster","abuse","spam","sentry-next",
            "wixpress","605a7bae"]
    if any(f in email for f in fake): return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email): return False
    domain = email.split("@")[1].lower()
    if domain.startswith("www."): return False
    # Block government emails
    if ".gov" in domain: return False
    if ".gov." in domain: return False
    if any(s in domain for s in SKIP_DOMAINS): return False
    if len(domain) < 5: return False
    return True

def score_email(email):
    prefix = email.split("@")[0].lower()
    domain = email.split("@")[1].lower()
    score = 0
    if "gmail.com" in domain: score += 3
    if "yahoo.com" in domain: score += 2
    if "hotmail.com" in domain or "aol.com" in domain: score += 1
    if any(p == prefix for p in GOOD_PREFIXES): score += 5
    if any(p in prefix for p in GOOD_PREFIXES): score += 2
    smoke_keywords = ["smoke","vape","vapor","cigar","tobacco","hookah","hemp","cloud","canna"]
    if any(k in domain for k in smoke_keywords): score += 10
    if any(k in prefix for k in smoke_keywords): score += 5
    return score

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
        w.writerow({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "company": c, "email": e,
            "state": s, "status": st
        })

def extract_emails(text):
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    valid = []
    for e in emails:
        e = e.lower().strip().rstrip(".")
        if is_valid_email(e) and e not in valid:
            valid.append(e)
    valid.sort(key=score_email, reverse=True)
    return valid

def crawl_website(url):
    emails = []
    try:
        if any(s in url for s in SKIP_DOMAINS): return []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(resp.text, "html.parser")
        emails.extend(extract_emails(resp.text))
        # Look for contact page
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if any(k in href for k in ["contact","about","reach"]):
                if href.startswith("http"):
                    contact_url = href
                elif href.startswith("/"):
                    base = "/".join(url.split("/")[:3])
                    contact_url = base + href
                else: continue
                try:
                    r2 = requests.get(contact_url, headers=headers, timeout=5)
                    emails.extend(extract_emails(r2.text))
                except: pass
                break
    except: pass
    emails.sort(key=score_email, reverse=True)
    return list(dict.fromkeys(emails))

def find_leads(state, sent, global_sent_session):
    print(f"\n Searching {state}...")
    leads = []
    queries = [
        f"smoke shop {state} contact email",
        f"vape shop {state} email address",
        f"tobacco store {state} owner email",
    ]
    for q in queries:
        if len(leads) >= 5: break
        try:
            r = requests.get("https://serpapi.com/search",
                params={"q":q,"api_key":SERPAPI_KEY,"engine":"google","num":10,"gl":"us"},
                timeout=15)
            results = r.json().get("organic_results", [])
            for res in results[:8]:
                if len(leads) >= 5: break
                title = res.get("title","Unknown")
                link = res.get("link","")
                snippet = res.get("snippet","")
                # Skip directory/news sites
                if any(s in link.lower() for s in SKIP_DOMAINS): continue
                if ".gov" in link.lower(): continue
                emails = extract_emails(snippet + " " + title)
                if not emails and link and "http" in link:
                    emails = crawl_website(link)
                for email in emails[:1]:
                    email = email.strip().rstrip(".")
                    if (email not in sent and
                        email not in global_sent_session and
                        email not in [l["email"] for l in leads]):
                        clean_title = re.sub(r'\s*[-|]\s*.*$','',title).strip()[:50]
                        leads.append({
                            "company": clean_title or "Smoke Shop",
                            "email": email,
                            "state": state,
                            "score": score_email(email)
                        })
                        global_sent_session.add(email)
                        print(f"  OK {clean_title[:25]} -> {email}")
                        break
        except Exception as e:
            print(f"  Error: {str(e)[:40]}")
        time.sleep(1.5)
    print(f"  Found {len(leads)} leads")
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
        for kw in ['FROM "mailer-daemon"','FROM "postmaster"',
                   'FROM "Mail Delivery"','FROM "Mail Delivery Subsystem"',
                   'SUBJECT "Delivery incomplete"','SUBJECT "Undeliverable"',
                   'SUBJECT "Delivery Status"','SUBJECT "Mail delivery failed"']:
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
    print(f"AlertPro CCTV Agent - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    sent = load_sent()
    global_sent_session = set()
    leads = []
    states = STATES.copy()
    random.shuffle(states)
    for state in states:
        if len(leads) >= TARGET: break
        leads.extend(find_leads(state, sent, global_sent_session))
    leads.sort(key=lambda x: x.get("score",0), reverse=True)
    print(f"\nTotal leads: {len(leads)}")
    print(f"Sending top {min(TARGET,len(leads))}...")
    sent_count = 0
    for i, lead in enumerate(leads[:TARGET], 1):
        email = lead["email"].strip().rstrip(".")
        if send_email(lead["company"], email):
            sent_count += 1
            save_sent(lead["company"], email, lead["state"], "sent")
            print(f"[{i}] OK: {lead['company'][:25]} -> {email}")
        else:
            save_sent(lead["company"], email, lead["state"], "failed")
            print(f"[{i}] FAIL: {email}")
        time.sleep(2)
    print(f"\nSent: {sent_count}")
    clean_bounces()
    print("DONE!")

if __name__ == "__main__":
    main()
