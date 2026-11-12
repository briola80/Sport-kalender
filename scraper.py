import icalendar
import requests

# Dina färdiga .ics-länkar från Sync2Cal
ics_länkar = [
    "http://ics.sync2cal.com/categories/get_ics/1b9695d3-2450-4686-aead-ceadabd9a0fe.ics", # IFK Göteborg Herr
    "https://ics.sync2cal.com/categories/get_ics/c0354fb4-73e4-47cb-815b-6d662eac6d64.ics", # Frölunda HC Herr
    "http://ics.sync2cal.com/categories/get_ics/3fb2c55b-b904-47e8-94b8-c646c78cda8f.ics", # Sverige Hockey Herr
    "http://ics.sync2cal.com/categories/get_ics/4504b764-fe86-4c52-b353-b25545b6d03f.ics", # Sverige Fotboll Dam
    "https://ics.sync2cal.com/categories/get_ics/6a9f72e6-9fc7-440b-9482-9e92aa1a95ba.ics"  # Sverige Fotboll Herr
]

def bestam_kanal(sammanfattning):
    """Mappar automatiskt rätt kanal baserat på matchen/lagets namn i kalendern."""
    namn = sammanfattning.lower()
    if "frölunda" in namn:
        return "TV4 Play Hockey"
    elif "ifk göteborg" in namn:
        return "Max / Discovery+"
    elif "sverige" in namn:
        return "SVT / Viaplay"
    return "TV4 Play"

master_cal = icalendar.Calendar()

# Gå igenom alla länkarna och hämta matcherna
for url in ics_länkar:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            cal = icalendar.Calendar.from_ical(response.content)
            for component in cal.walk('vevent'):
                summary = str(component.get('summary', ''))
                
                # Lägg till sändande kanal i platsfältet (location)
                kanal = bestam_kanal(summary)
                component.add('location', kanal, overwrite=True)
                
                master_cal.add_component(component)
    except Exception as e:
        print(f"Kunde inte hämta länk {url}: {e}")

# Spara den sammanslagna kalendern
with open('kalender.ics', 'wb') as f:
    f.write(master_cal.to_ical())

print("Alla spelscheman har hämtats, slagits ihop och uppdaterats!")
