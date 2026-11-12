import icalendar
from datetime import datetime, timedelta

matcher = [
    {
        "hemma": "Frölunda HC",
        "borta": "Malmö Redhawks",
        "serie": "SHL",
        "tid": datetime(2026, 11, 12, 19, 0),
        "kanal": "TV4 Play Hockey / TV12"
    },
    {
        "hemma": "Sverige",
        "borta": "Schweiz",
        "serie": "Hockey-VM Dam",
        "tid": datetime(2026, 11, 13, 19, 0),
        "kanal": "SVT Play / SVT2"
    },
    {
        "hemma": "IFK Göteborg",
        "borta": "AIK",
        "serie": "Allsvenskan",
        "tid": datetime(2026, 11, 16, 15, 0),
        "kanal": "Max / Discovery+"
    }
]

cal = icalendar.Calendar()

for m in matcher:
    event = icalendar.Event()
    event.add('summary', f"{m['hemma']} - {m['borta']}")
    event.add('dtstart', m['tid'])
    
    # Sätter sluttid automatiskt till 2 timmar efter start (eller anpassa efter sport)
    sluttid = m['tid'] + timedelta(hours=2, minutes=15)
    event.add('dtend', sluttid)
    
    # Sätter den exakta kanalen i Plats-fältet
    event.add('location', m['kanal'])
    event.add('description', f"Serie/Turnering: {m['serie']}")
    
    cal.add_component(event)

# Sparar kalenderfilen
with open('kalender.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Kalender uppdaterad med både start- och sluttider!")
