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

I noticed most smoke shops have cameras but nobody watching them at night — leaving them vulnerable to theft and break-ins.

We offer AlertPro CCTV monitoring:
✅ Real trained operators watching 24/7
✅ Instant alerts within 60 seconds
✅ Full incident documentation + video evidence
✅ Only $150/month (no setup fee, no contracts)
✅ 60% cheaper than a security guard

We work specifically with smoke shops, vape shops, and tobacco retailers across the USA.

Would you be open to a quick 10-minute call this week to see if it's a good fit for {company}?

Best regards,
Shahadat
AlertPro CCTV Eagle Eyes
📞 +971 56 646 8525
🌐 https://alertpro.appabbottabad.com
💬 WhatsApp: https://wa.me/971566468525"""

# Domains to completely skip
SKIP_DOMAINS = [
    "yelp.com","google.com","facebook.com","instagram.com","twitter.com",
    "linkedin.com","yellowpages.com","tripadvisor.com","foursquare.com",
    "wix.com","squarespace.com","wordpress.com","shopify.com","godaddy.com",
    "amazonaws.com","sentry.io","fountmedia.com","bloyal.com","indeed.com",
    "ziprecruiter.com","glassdoor.com","bbb.org","thumbtack.com","groupon.com",
    "angi.com","houzz.com","nextdoor.com","patch.com","citysearch.com",
    "mapquest.com","whitepages.com","spokeo.com","yellowbook.com",
    "superpages.com","manta.com","chamberofcommerce.com","dandb.com",
    "bizapedia.com","corporationwiki.com","opencorporates.com",
    "merchantcircle.com","hotfrog.com","cylex.us","n49.com",
    "2findlocal.com","local.com","ezlocal.com","brownbook.net",
    "tupalo.com","opendi.us","storeboard.com","fyple.com"
]

# Good email prefixes (prioritize these)
GOOD_PREFIXES = ["info","contact","hello","owner","manager","sales",
                 "admin","support","shop","store","business"]

def is_valid_email(email):
    email = email.strip().lower().rstrip(".")
    if not email: return False
    if "www." in email: return False
    if email.count("@") != 1: return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email): return False
    domain = email.split("@")[1].lower()
    if domain.startswith("www."): return False
    if any(s in domain for s in SKIP_DOMAINS): return False
    # Skip if domain has no dot or too short
    if len(domain) < 5: return False
    # Skip obvious non-business emails
    bad_prefixes = ["noreply","no-reply","donotreply","bounce",
                   "mailer","daemon","postmaster","abuse","spam"]
    prefix = email.split("@")[0].lower()
    if any(b in prefix for b in bad_prefixes): return False
    return True

def score_email(email):
    """Score email quality - higher is better"""
    prefix = email.split("@")[0].lower()
    domain = email.split("@")[1].lower()
    score = 0
    # Gmail/Yahoo are often real business emails
    if "gmail.com" in domain: score += 3
    if "yahoo.com" in domain: score += 2
    # Good prefixes
    if any(p == prefix for p in GOOD_PREFIXES): score += 5
    if any(p in prefix for p in GOOD_PREFIXES): score += 2
    # Smoke shop keywords in domain
    smoke_keywords = ["smoke","vape","vapor","cigar","tobacco","hookah","head","hemp"]
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
            "company": c,
            "email": e,
            "state": s,
            "status": st
        })

def extract_emails(text):
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    valid = []
    for e in emails:
        e = e.lower().strip().rstrip(".")
        if is_valid_email(e):
            valid.append(e)
    # Sort by score (best first)
    valid.sort(key=score_email, reverse=True)
    return list(dict.fromkeys(valid))  # Remove duplicates

def crawl_website(url):
    """Crawl website to find contact email"""
    emails = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Check main page
        emails.extend(extract_emails(resp.text))
        
        # Look for contact page link
        contact_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if any(k in href for k in ["contact","about","reach","email"]):
                if href.startswith("http"):
                    contact_links.append(href)
                elif href.startswith("/"):
                    base = "/".join(url.split("/")[:3])
                    contact_links.append(base + href)
        
        # Crawl contact page
        for contact_url in contact_links[:2]:
            try:
                resp2 = requests.get(contact_url, headers=headers, timeout=5)
                emails.extend(extract_emails(resp2.text))
            except: pass
            
    except: pass
    
    # Sort by score and return best
    emails.sort(key=score_email, reverse=True)
    return list(dict.fromkeys(emails))

def find_leads(state, sent):
    print(f"\n🔍 Searching {state}...")
    leads = []
    
    queries = [
        f"smoke shop {state} contact email site:.com",
        f"vape shop {state} email address contact",
        f"tobacco store {state} owner email",
        f'"smoke shop" "{state}" email contact',
    ]
    
    for q in queries:
        if len(leads) >= 6: break
        try:
            r = requests.get("https://serpapi.com/search",
                params={
                    "q": q,
                    "api_key": SERPAPI_KEY,
                    "engine": "google",
                    "num": 10,
                    "gl": "us"
                }, timeout=15)
            
            results = r.json().get("organic_results", [])
            
            for res in results[:8]:
                if len(leads) >= 6: break
                title = res.get("title", "Unknown Shop")
                link = res.get("link", "")
                snippet = res.get("snippet", "")
                
                # Skip directory sites
                if any(s in link.lower() for s in SKIP_DOMAINS):
                    continue
                
                # Try to get email from snippet first (faster)
                emails = extract_emails(snippet + " " + title)
                
                # If no email in snippet, crawl the website
                if not emails and link and "http" in link:
                    print(f"  🌐 Crawling: {link[:50]}...")
                    emails = crawl_website(link)
                
                # Add best email
                for email in emails[:1]:
                    email = email.strip().rstrip(".")
                    if email not in sent and email not in [l["email"] for l in leads]:
                        # Clean up title
                        clean_title = re.sub(r'\s*[-|]\s*.*$', '', title).strip()
                        if len(clean_title) < 3:
                            clean_title = title[:50]
                        
                        leads.append({
                            "company": clean_title[:50],
                            "email": email,
                            "state": state,
                            "score": score_email(email)
                        })
                        print(f"  ✅ {clean_title[:30]} → {email} (score:{score_email(email)})")
                        break
                        
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}")
        
        time.sleep(1.5)
    
    print(f"  📊 Found {len(leads)} valid leads in {state}")
    return leads

def send_email(company, email):
    try:
        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        s.starttls()
        s.login(GMAIL_USER, GMAIL_PASSWORD)
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Shahadat - AlertPro CCTV <{GMAIL_USER}>"
        msg["To"] = email
        msg["Subject"] = random.choice(SUBJECTS)
        msg["Reply-To"] = GMAIL_USER
        body = BODY.format(company=company)
        msg.attach(MIMEText(body, "plain"))
        s.send_message(msg)
        s.quit()
        return True
    except Exception as e:
        print(f"  Send error: {str(e)[:50]}")
        return False

def clean_bounces():
    try:
        m = imaplib.IMAP4_SSL("imap.gmail.com", timeout=30)
        m.login(GMAIL_USER, GMAIL_PASSWORD)
        m.select("INBOX")
        total = 0
        for kw in [
            'FROM "mailer-daemon"',
            'FROM "postmaster"',
            'FROM "Mail Delivery"',
            'FROM "Mail Delivery Subsystem"',
            'SUBJECT "Delivery incomplete"',
            'SUBJECT "Undeliverable"',
            'SUBJECT "Delivery Status Notification"',
            'SUBJECT "Mail delivery failed"'
        ]:
            try:
                _, msgs = m.search(None, kw)
                for i in msgs[0].split():
                    m.store(i, "+FLAGS", "\\Deleted")
                    total += 1
            except: pass
        m.expunge()
        m.logout()
        print(f"🗑️  Cleaned {total} bounces")
    except Exception as e:
        print(f"Bounce cleanup error: {str(e)[:50]}")

def main():
    print("=" * 60)
    print(f"AlertPro CCTV Agent - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    sent = load_sent()
    leads = []
    states = STATES.copy()
    random.shuffle(states)
    
    for state in states:
        if len(leads) >= TARGET: break
        new_leads = find_leads(state, sent)
        leads.extend(new_leads)
    
    # Sort leads by email score (best first)
    leads.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    print(f"\n{'='*60}")
    print(f"Total valid leads found: {len(leads)}")
    print(f"Sending to top {min(TARGET, len(leads))} leads...")
    print(f"{'='*60}\n")
    
    sent_count = 0
    failed_count = 0
    
    for i, lead in enumerate(leads[:TARGET], 1):
        email = lead["email"].strip().rstrip(".")
        company = lead["company"]
        
        if send_email(company, email):
            sent_count += 1
            save_sent(company, email, lead["state"], "sent")
            print(f"[{i}] ✅ {company[:30]} → {email}")
        else:
            failed_count += 1
            save_sent(company, email, lead["state"], "failed")
            print(f"[{i}] ❌ Failed: {email}")
        
        time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"✅ Sent: {sent_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"{'='*60}")
    
    print("\nCleaning bounces...")
    clean_bounces()
    print("\n🎉 DONE!")

if __name__ == "__main__":
    main()
