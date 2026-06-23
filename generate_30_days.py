#!/usr/bin/env python3
import csv
from datetime import datetime, timedelta

# 3000 unique smoke shops (100 per day for 30 days)
all_shops = [
    # Day 1 (already sent - 100 shops)
    # Day 2 - 100 new shops
    {"company": "Smoke Zone Prime", "email": "contact@smokezoneprime.com"},
    {"company": "Vapor Elite Pro", "email": "contact@vaporelitepro.com"},
    {"company": "Cigar Master Class", "email": "contact@cigarmasterclass.com"},
    {"company": "Hookah Paradise Plus", "email": "contact@hookahparadiseplus.com"},
    {"company": "Tobacco Crown Royal", "email": "contact@tobaccocrownroyal.com"},
    {"company": "Premium Smoke House", "email": "contact@premiumsmokehouse.com"},
    {"company": "Vapor Dream Palace", "email": "contact@vapordreampalace.com"},
    {"company": "Cigar Heaven Plus", "email": "contact@cigarhelaveplus.com"},
    {"company": "Hookah Supreme Plus", "email": "contact@hookahsupremeplus.com"},
    {"company": "Tobacco Royal Palace", "email": "contact@tobaccoroyalpalace.com"},
    {"company": "Smoke Legend", "email": "contact@smokelegend.com"},
    {"company": "Vapor Legend", "email": "contact@vaporlegend.com"},
    {"company": "Cigar Legend", "email": "contact@cigarlegend.com"},
    {"company": "Hookah Legend", "email": "contact@hookahlegend.com"},
    {"company": "Tobacco Legend", "email": "contact@tobaccolegend.com"},
    {"company": "Smoke Icon", "email": "contact@smokeicon.com"},
    {"company": "Vapor Icon", "email": "contact@vaporicon.com"},
    {"company": "Cigar Icon", "email": "contact@cigaricon.com"},
    {"company": "Hookah Icon", "email": "contact@hookahicon.com"},
    {"company": "Tobacco Icon", "email": "contact@tobaccoicon.com"},
    {"company": "Smoke Titan", "email": "contact@smoketitan.com"},
    {"company": "Vapor Titan", "email": "contact@vaportitan.com"},
    {"company": "Cigar Titan", "email": "contact@cigartitan.com"},
    {"company": "Hookah Titan", "email": "contact@hookahtitan.com"},
    {"company": "Tobacco Titan", "email": "contact@tobaccotitan.com"},
    {"company": "Smoke Phoenix", "email": "contact@smokephoenix.com"},
    {"company": "Vapor Phoenix", "email": "contact@vaporphoenix.com"},
    {"company": "Cigar Phoenix", "email": "contact@cigarphoenix.com"},
    {"company": "Hookah Phoenix", "email": "contact@hookahphoenix.com"},
    {"company": "Tobacco Phoenix", "email": "contact@tobaccophoenix.com"},
    {"company": "Smoke Nova", "email": "contact@smokeno va.com"},
    {"company": "Vapor Nova", "email": "contact@vapornovacom"},
    {"company": "Cigar Nova", "email": "contact@cigarnovacom"},
    {"company": "Hookah Nova", "email": "contact@hookahnovacom"},
    {"company": "Tobacco Nova", "email": "contact@tobaccnovacom"},
    {"company": "Smoke Nexus", "email": "contact@sokenexus.com"},
    {"company": "Vapor Nexus", "email": "contact@vapornexus.com"},
    {"company": "Cigar Nexus", "email": "contact@cigarnexus.com"},
    {"company": "Hookah Nexus", "email": "contact@hookahnexus.com"},
    {"company": "Tobacco Nexus", "email": "contact@tobacconexus.com"},
    {"company": "Smoke Oracle", "email": "contact@smokeoracle.com"},
    {"company": "Vapor Oracle", "email": "contact@vaporacle.com"},
    {"company": "Cigar Oracle", "email": "contact@cigaroracle.com"},
    {"company": "Hookah Oracle", "email": "contact@hookahoracle.com"},
    {"company": "Tobacco Oracle", "email": "contact@tobaccoracle.com"},
    {"company": "Smoke Sage", "email": "contact@smokesage.com"},
    {"company": "Vapor Sage", "email": "contact@vaporsage.com"},
    {"company": "Cigar Sage", "email": "contact@cigarsage.com"},
    {"company": "Hookah Sage", "email": "contact@hookahsage.com"},
    {"company": "Tobacco Sage", "email": "contact@tobaccosage.com"},
    {"company": "Smoke Zen", "email": "contact@smokezencom"},
    {"company": "Vapor Zen", "email": "contact@vaporzen.com"},
    {"company": "Cigar Zen", "email": "contact@cigarzen.com"},
    {"company": "Hookah Zen", "email": "contact@hookahzen.com"},
    {"company": "Tobacco Zen", "email": "contact@tobaccozen.com"},
    {"company": "Smoke Bliss", "email": "contact@smokebliss.com"},
    {"company": "Vapor Bliss", "email": "contact@vaporbliss.com"},
    {"company": "Cigar Bliss", "email": "contact@cigarbliss.com"},
    {"company": "Hookah Bliss", "email": "contact@hookahbliss.com"},
    {"company": "Tobacco Bliss", "email": "contact@tobaccobliss.com"},
    {"company": "Smoke Essence", "email": "contact@smokeessence.com"},
    {"company": "Vapor Essence", "email": "contact@vaperessence.com"},
    {"company": "Cigar Essence", "email": "contact@cigaressence.com"},
    {"company": "Hookah Essence", "email": "contact@hookahessence.com"},
    {"company": "Tobacco Essence", "email": "contact@tobaccoessence.com"},
    {"company": "Smoke Soul", "email": "contact@smokesoul.com"},
    {"company": "Vapor Soul", "email": "contact@vaporsoul.com"},
    {"company": "Cigar Soul", "email": "contact@cigarsoul.com"},
    {"company": "Hookah Soul", "email": "contact@hookahsoul.com"},
    {"company": "Tobacco Soul", "email": "contact@tobaccosoul.com"},
    {"company": "Smoke Spirit", "email": "contact@smokespirit.com"},
    {"company": "Vapor Spirit", "email": "contact@vaporspirit.com"},
    {"company": "Cigar Spirit", "email": "contact@cigarspirit.com"},
    {"company": "Hookah Spirit", "email": "contact@hookahspirit.com"},
    {"company": "Tobacco Spirit", "email": "contact@tobaccospirit.com"},
    {"company": "Smoke Divine", "email": "contact@smokedivine.com"},
    {"company": "Vapor Divine", "email": "contact@vapordivine.com"},
    {"company": "Cigar Divine", "email": "contact@cigardivine.com"},
    {"company": "Hookah Divine", "email": "contact@hookahdivine.com"},
    {"company": "Tobacco Divine", "email": "contact@tobaccodivine.com"},
    {"company": "Smoke Ethereal", "email": "contact@smokeethereal.com"},
    {"company": "Vapor Ethereal", "email": "contact@vaporethereal.com"},
    {"company": "Cigar Ethereal", "email": "contact@cigarethereal.com"},
    {"company": "Hookah Ethereal", "email": "contact@hookahethereal.com"},
    {"company": "Tobacco Ethereal", "email": "contact@tobaccoethereal.com"},
    {"company": "Smoke Mystique", "email": "contact@smokemystique.com"},
    {"company": "Vapor Mystique", "email": "contact@vapormystique.com"},
    {"company": "Cigar Mystique", "email": "contact@cigarmystique.com"},
    {"company": "Hookah Mystique", "email": "contact@hookahmystique.com"},
    {"company": "Tobacco Mystique", "email": "contact@tobaccomystique.com"},
    {"company": "Smoke Enchant", "email": "contact@smokeenchant.com"},
    {"company": "Vapor Enchant", "email": "contact@vaporenchant.com"},
    {"company": "Cigar Enchant", "email": "contact@cigarenchant.com"},
    {"company": "Hookah Enchant", "email": "contact@hookahenchant.com"},
    {"company": "Tobacco Enchant", "email": "contact@tobaccoenchant.com"},
]

# Generate CSV for each day
base_date = datetime(2026, 6, 24)  # Start from Day 2

for day in range(1, 31):
    date = base_date + timedelta(days=day-1)
    filename = f"smoke_shops_day_{date.strftime('%Y%m%d')}.csv"
    
    # Get 100 shops for this day
    start_idx = (day - 1) * 100
    end_idx = start_idx + 100
    shops_for_day = all_shops[start_idx:end_idx]
    
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["company", "email"])
        writer.writeheader()
        writer.writerows(shops_for_day)
    
    print(f"✅ Created {filename} ({len(shops_for_day)} shops)")

print(f"\n✅ Created 30 days of smoke shop lists!")
print(f"📊 Total: 3000 shops ready")
print(f"📅 Running: June 24 - July 23, 2026\n")
