import icalendar
from datetime import datetime

def hamta_kanal(liga, hemmalag):
    """Mappar automatiskt rätt sändande kanal baserat på liga eller lag."""
    kanaler = {
        "SHL": "TV4 Play",
        "CHL": "Viaplay",
        "Allsvenskan": "Max / TV4 Play",
        "Frölunda HC": "TV4 Play",
        "IFK Göteborg": "Max / Discovery+"
    }
    # Om laget eller ligan finns i listan returneras kanalen, annars standard "TV4 Play"
    return kanaler.get(liga, kanaler.get(hemmalag, "TV4 Play"))

# Lägg till alla dina matcher/lag här
matcher = [
    {
        "hemma": "Frölunda HC",
        "borta": "Malmö Redhawks",
        "liga": "SHL",
        "tid": datetime(2026, 11, 15, 19, 0)
    },
    {
        "hemma": "IFK Göteborg",
        "borta": "AIK",
        "liga": "Allsvenskan",
        "tid": datetime(2026, 11, 16, 15, 0)
    }
    # Du kan lägga till hur många rader som helst här nedanför på samma sätt!
]

cal = icalendar.Calendar()

for m in matcher:
    event = icalendar.Event()
    event.add('summary', f"{m['hemma']} - {m['borta']}")
    event.add('dtstart', m['tid'])
    
    # Sätter kanalen automatiskt i Plats-fältet
    kanal = hamta_kanal(m['liga'], m['hemma'])
    event.add('location', kanal)
    
    cal.add_component(event)

# Sparar kalenderfilen med det exakta namnet kalender.ics
with open('kalender.ics', 'wb') as f:
    f.write(cal.to_ical())

print("Matchkalender med uppdaterade lag genererad!")
