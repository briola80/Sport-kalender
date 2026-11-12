import icalendar
from datetime import datetime, timedelta

def hamta_kanal(lag, serie):
    """Mappar automatiskt rätt sändande kanal baserat på lag och serie."""
    if "Frölunda" in lag:
        return "TV4 Play / C More"
    elif "IFK Göteborg" in lag:
        return "Max / Discovery+"
    elif "Sverige" in lag:
        return "SVT / Viaplay"
    return "TV4 Play"

# Lista över dina prioriterade lag och serier som skriptet genererar ifrån
# (Du kan enkelt lägga till eller uppdatera datum/matcher här efter hand)
matcher = [
    {
        "hemma": "Frölunda HC",
        "borta": "Färjestad BK",
        "serie": "SHL",
        "tid": datetime.now() + timedelta(days=1)
    },
    {
        "hemma": "IFK Göteborg",
        "borta": "AIK",
        "serie": "Allsvenskan",
        "tid": datetime.now() + timedelta(days=2)
    },
    {
        "hemma": "Sverige",
        "borta": "Tjeckien",
        "serie": "Landskamp",
        "tid": datetime.now() + timedelta(days=3)
    }
]

cal = icalendar.Calendar()

for m in matcher:
    event = icalendar.Event()
    event.add('summary', f"{m['hemma']} - {m['borta']}")
    event.add('dtstart', m['tid'])
    
    # Sätter sändande kanal automatiskt i Plats-fältet
    kanal = hamta_kanal(m['hemma'], m['serie'])
    event.add('location', kanal)
    
    # Lägger till serien i beskrivningen
    event.add('description', f"Serie/Turnering: {m['serie']}")
    
    cal.add_component(event)

# Sparar kalenderfilen med det exakta namnet kalender.ics
with open('kalender.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Automatiskt genererad kalender för dina favoritlag är klar!")
