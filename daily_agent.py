import csv, smtplib, imaplib, time, os, re, random, socket
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bs4 import BeautifulSoup

GMAIL_USER = "alertprocctv@gmail.com"
GMAIL_PASSWORD = "ltvo whwc chok lyez"
SENT_FILE = "data/sent_log.csv"
TARGET = 20

# Generate 700+ potential smoke shop domains
def generate_sites():
    cities = [
        "houston","dallas","austin","sanantonio","fortworth","elpaso",
        "losangeles","sandiego","fresno","sacramento","longbeach","oakland",
        "jacksonville","miami","tampa","orlando","fortlauderdale","gainesville",
        "newyork","brooklyn","buffalo","rochester","syracuse","albany",
        "chicago","rockford","joliet","naperville","springfield","peoria",
        "columbus","cleveland","cincinnati","toledo","akron","dayton",
        "atlanta","savannah","macon","athens","roswell","marietta",
        "charlotte","raleigh","greensboro","durham","fayetteville","asheville",
        "detroit","grandrapids","lansing","flint","annarbor","kalamazoo",
        "phoenix","tucson","mesa","chandler","scottsdale","tempe","glendale",
        "philadelphia","pittsburgh","allentown","erie","scranton","reading",
        "seattle","spokane","tacoma","bellevue","everett","renton",
        "denver","colorado","aurora","fortcollins","lakewood","pueblo",
        "nashville","memphis","knoxville","chattanooga","clarksville","jackson",
        "indianapolis","fortwayne","evansville","southbend","bloomington",
        "kansascity","stlouis","springfield","columbia","independence",
        "baltimore","columbia","rockville","bethesda","frederick","annapolis",
        "boston","worcester","cambridge","lowell","brockton","springfield",
        "lasvegas","henderson","reno","sparks","northlasvegas",
        "portland","eugene","salem","gresham","hillsboro","beaverton",
        "louisville","lexington","bowling","owensboro","covington",
        "neworleans","batonrouge","shreveport","lafayette","lakecharles",
        "birmingham","montgomery","huntsville","mobile","tuscaloosa",
        "richmond","norfolk","chesapeake","virginia","newport","alexandria",
        "milwaukee","madison","greenbay","kenosha","racine","appleton",
        "minneapolis","stpaul","rochester","duluth","bloomington","brooklyn",
        "omaha","lincoln","bellevue","grandisland","kearney",
        "tulsa","oklahomacity","norman","broken","lawton","edmond",
        "albuquerque","lascruces","rio","santa","roswell","farmington",
        "wichita","overland","kansascity","topeka","olathe","manhattan",
        "columbia","charleston","north","greenville","rockhill","summerville",
        "saltlake","westvalley","provo","westjordan","orem","sandy",
        "hartford","bridgeport","newhaven","stamford","waterbury","norwalk",
        "providence","cranston","warwick","pawtucket","eastprovidence",
        "jackson","gulfport","southaven","hattiesburg","biloxi","olive",
        "littlerock","fortsmith","fayetteville","springdale","jonesboro",
        "desmoines","cedar","davenport","sioux","iowa","waterloo",
        "sioux","rapid","aberdeen","brookings","watertown","mitchell",
        "fargo","bismarck","grandforcs","minot","westernfargo","mandan",
        "billings","missoula","greatfalls","bozeman","butte","helena",
        "cheyenne","casper","laramie","gillette","rock","sheridan",
        "boise","meridian","nampa","idaho","pocatello","caldwell",
        "anchorage","juneau","fairbanks","sitka","ketchikan","wasilla",
        "honolulu","pearl","hilo","kailua","kaneohe","waipahu",
        "burlington","south","rutland","barre","montpelier","winooski",
        "portland","lewiston","bangor","south","auburn","biddeford",
        "manchester","nashua","concord","derry","rochester","dover",
        "providence","cranston","warwick","pawtucket","woonsocket"
    ]
    
    smoke_words = ["smoke","vape","vapor","tobacco","cigar","hookah"]
    sites = []
    
    for city in cities:
        city = city.lower().replace(" ","")
        for word in smoke_words:
            sites.append(f"https://www.{city}{word}shop.com")
            sites.append(f"https://www.{city}{word}.com")
            sites.append(f"https://www.{word}shop{city}.com")
    
    # Add known real sites
    known_real = [
        "https://tootersvapeshop.com",
        "https://www.elevatesmokeshops.com",
        "https://www.unclestussmokeandvape.com",
        "https://risesmokeshop.com",
        "https://www.cloud9smokeco.com",
        "https://www.smokesupply.com",
        "https://www.o2vape.com",
        "https://www.smokeymoes.com",
        "https://www.flawlessvapeshop.com",
        "https://www.indyecigs.com",
        "https://www.317vapers.com",
        "https://www.rockymountainsmoke.com",
        "https://www.smokelessmn.com",
        "https://www.vapeosmoketn.com",
        "https://www.area51smokenvape.com",
        "https://www.centralvapesupply.com",
        "https://www.chicitysmokeshop.com",
        "https://www.altsmoke.com",
        "https://www.washsmoke.com",
        "https://www.highergradestore.com",
        "https://www.houseofpipes.com",
        "https://www.famous-smoke.com",
        "https://www.sweetfiretobacco.com",
        "https://www.buddhaglassmn.com",
        "https://www.royaltobacco.com",
        "https://www.thevaporemporiummd.com",
        "https://www.joostvapor.com",
        "https://www.smokerolla.com",
        "https://www.redstarvapor.com",
        "https://www.101smokeshop.com",
        "https://www.ebcreate.store",
        "https://www.cravesmokeshopmi.com",
        "https://www.thetobaccoshoppeinc.com",
        "https://www.extonsmokeshop.com",
        "https://www.thehabitsmokeshop.com",
        "https://www.blackcloudsvape.com",
        "https://www.vypevapor.com",
        "https://www.drippersvapeshop.com",
        "https://www.vibecitysmokeshop.com",
        "https://www.shopfarragut.com",
        "https://www.thevapeshop.com",
        "https://www.highergrade.com",
        "https://www.islandvapeshop.com",
        "https://www.holysmokeandvape.com",
        "https://www.allin1smokeshop.com",
        "https://www.elitevapeandsmoke.com",
        "https://www.pipesandtobaccosmokeshop.com",
        "https://www.ecigsinternational.com",
        "https://www.madisonupinsmoke.com",
        "https://www.tundrasmokeshopgreenbayreviews.com",
        "https://www.topdogzvapeshop.com",
    ]
    
    return list(set(sites + known_real))

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
    "linkedin.com","yellowpages.com","tripadvisor.com","godaddy.com",
    "amazonaws.com","sentry.io","indeed.com","domain.com","yoursite.com",
    "example.com","test.com","wixpress.com","lung.org","healthline.com",
    "webmd.com","reddit.com","youtube.com","amazon.com","walmart.com"
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
    fake = ["noreply","no-reply","donotreply","bounce","mailer",
            "daemon","postmaster","abuse","spam","wixpress",
            "sentry","yoursite","@domain.","placeholder","example"]
    if any(f in email for f in fake): return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email): return False
    domain = email.split("@")[1].lower()
    if domain.startswith("www."): return False
    if ".gov" in domain: return False
    if ".edu" in domain: return False
    if any(s in domain for s in SKIP_DOMAINS): return False
    return True

def score_email(email):
    prefix = email.split("@")[0].lower()
    domain = email.split("@")[1].lower()
    score = 0
    if "gmail.com" in domain: score += 3
    if "yahoo.com" in domain: score += 2
    if "hotmail.com" in domain: score += 1
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
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        emails = extract_emails(resp.text)
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
    print(f"Target: {TARGET} REAL verified emails")
    print("="*60)
    
    sent = load_sent()
    session_sent = set()
    leads = []
    
    # Generate and shuffle all potential sites
    all_sites = generate_sites()
    random.shuffle(all_sites)
    print(f"Total potential sites: {len(all_sites)}")
    
    checked = 0
    for url in all_sites:
        if len(leads) >= TARGET: break
        if checked > 200: break  # Don't check too many
        
        try:
            domain = url.split("/")[2].replace("www.","").lower()
        except:
            continue
        
        checked += 1
        
        # Quick DNS check
        if not domain_exists(domain):
            continue
        
        print(f"Found domain: {domain}")
        email = get_email_from_website(url)
        
        if not email:
            continue
        if email in sent or email in session_sent:
            print(f"  Skip duplicate: {email}")
            continue
        
        company = domain.split(".")[0].replace("-"," ").title()
        leads.append({
            "company": company[:50],
            "email": email,
            "state": "USA",
            "score": score_email(email)
        })
        session_sent.add(email)
        print(f"  REAL: {company} -> {email}")
        time.sleep(1)
    
    print(f"\nFound {len(leads)} real leads from {checked} checked")
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
    
    print(f"\nSent: {sent_count} real verified emails")
    clean_bounces()
    print("DONE!")

if __name__ == "__main__":
    main()
