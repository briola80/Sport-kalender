import icalendar
from datetime import datetime

# Exakta matcher med exakta klockslag, datum och specifika kanaler
matcher = [
    {
        "hemma": "Frölunda HC",
        "borta": "Malmö Redhawks",
        "serie": "SHL",
        "tid": datetime(2026, 11, 12, 19, 0),  # Exakt datum och tid från din bild
        "kanal": "TV4 Play Hockey / TV12"       # Exakta kanaler
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
    
    # Sätter den exakta kanalen direkt i Plats-fältet
    event.add('location', m['kanal'])
    
    # Lägger till serie/turnering i beskrivningen
    event.add('description', f"Serie/Turnering: {m['serie']}")
    
    cal.add_component(event)

# Sparar kalenderfilen med det exakta namnet kalender.ics
with open('kalender.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Kalender uppdaterad med korrekta tider och exakta kanaler!")
