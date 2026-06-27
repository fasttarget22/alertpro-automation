#!/usr/bin/env python3

# Test the email validator
import re

def is_valid_email(email):
    # Remove emails with www. in domain
    if "www." in email:
        return False
    # Remove emails ending with dot
    if email.endswith("."):
        return False
    # Remove Yelp and directory sites
    skip_domains = [
        "yelp.com", "google.com", "facebook.com", "instagram.com",
        "twitter.com", "linkedin.com", "yellowpages.com", "mapquest.com",
        "tripadvisor.com", "foursquare.com", "wix.com", "squarespace.com",
        "wordpress.com", "shopify.com", "godaddy.com", "amazonaws.com",
        "sentry.io", "fountmedia.com", "bloyal.com", "indeed.com",
        "ziprecruiter.com", "glassdoor.com", "bbb.org", "thumbtack.com",
        "angi.com", "houzz.com", "nextdoor.com", "patch.com",
        "groupon.com", "yelp.com", "citysearch.com"
    ]
    domain = email.split("@")[1].lower()
    if any(s in domain for s in skip_domains):
        return False
    # Must have valid format
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False
    # Domain must not start with www
    if domain.startswith("www."):
        return False
    return True

# Test cases
test_emails = [
    "info@www.yelp.com",
    "info@www.thevipsmokeshop.com",
    "info@vaporhaven.com.",
    "manager@arizonahookah.com.",
    "info@yelp.com",
    "tootersvapeshop@gmail.com",
    "holysmokeandvape@gmail.com",
    "info@denversmokeshop.com",
    "contact@phoenixsmoke.com"
]

print("Email Validation Test:")
print("="*50)
for email in test_emails:
    # Clean trailing dots first
    email = email.rstrip(".")
    valid = is_valid_email(email)
    status = "✅ VALID" if valid else "❌ INVALID"
    print(f"{status}: {email}")
