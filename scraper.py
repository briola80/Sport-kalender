import icalendar
import requests

# Dina riktiga ICS-länkar (konverterade från webcal:// till https:// eller http://)
ics_länkar = [
    ("Allsvenskan (Hela)", "https://pub.fotmob.com/prod/pub/api/v2/calendar/league/67.ics"),
    ("Allsvenskan - IFK Göteborg Dam", "https://calendar.google.com/calendar/ical/4p80oqf0abvv671j0esisb4b04%40group.calendar.google.com/public/basic.ics"),
    ("SHL - Frölunda HC Herr", "https://ics.ecal.com/ecal-sub/6af61f2ab13970000221c64a/Swedish%20Hockey%20League.ics"),
    ("SDHL - Frölunda HC Dam", "https://ics.ecal.com/ecal-sub/6af62014b13970000221c655/Swedish%20Hockey%20League.ics"),
    ("Liverpool FC", "https://pub.fotmob.com/prod/pub/api/v2/calendar/team/8650.ics"),
    ("Landslag Fotboll Herr", "https://pub.fotmob.com/prod/pub/api/v2/calendar/team/8520.ics"),
    ("Landslag Hockey (Tre Kronor)", "https://ics.sync2cal.com/categories/get_ics/3fb2c55b-b904-47e8-94b8-c646c78cda8f.ics"),
    ("Landslag Fotboll Dam", "https://pub.fotmob.com/prod/pub/api/v2/calendar/team/5814.ics"),
    ("Premier League", "https://pub.fotmob.com/prod/pub/api/v2/calendar/league/47.ics"),
    ("La Liga", "https://pub.fotmob.com/prod/pub/api/v2/calendar/league/87.ics"),
    ("Serie A", "https://pub.fotmob.com/prod/pub/api/v2/calendar/league/55.ics"),
    ("Champions League", "https://pub.fotmob.com/prod/pub/api/v2/calendar/league/42.ics")
]

def bestam_kanal(sammanfattning):
    """Mappar automatiskt rätt svensk kanal baserat på lag eller turnering."""
    namn = sammanfattning.lower()
    if "frölunda" in namn or "shl" in namn:
        return "TV4 Play Hockey"
    elif "ifk göteborg" in namn or "allsvenskan" in namn:
        return "Max / Discovery+"
    elif "liverpool" in namn or "premier league" in namn or "champions league" in namn:
        return "Viaplay"
    elif "la liga" in namn:
        return "TV4 Play"
    elif "serie a" in namn:
        return "TV4 Play"
    elif "sverige" in namn or "tre kronor" in namn:
        return "SVT / Viaplay"
    return "TV4 Play / Viaplay"

master_cal = icalendar.Calendar()
master_cal.add('prodid', '-//Olausson Sport Kalender//SV')
master_cal.add('version', '2.0')

headers = {'User-Agent': 'Mozilla/5.0'}
ant_matcher = 0

for namn_kalender, url in ics_länkar:
    try:
        print(f"Hämtar {namn_kalender}...")
        # Byt ut webcal mot https om det av misstag hänger kvar
        saker_url = url.replace("webcal://", "https://")
        response = requests.get(saker_url, headers=headers, timeout=15)
        print(f"Statuskod för {namn_kalender}: {response.status_code}")
        
        if response.status_code == 200:
            ics_text = response.content.decode('utf-8', errors='ignore')
            cal = icalendar.Calendar.from_ical(ics_text)
            
            hittade_i_denna = 0
            for component in cal.walk('vevent'):
                summary = str(component.get('summary', ''))
                kanal = bestam_kanal(summary)
                
                # Sätt platsfältet säkert
                if component.get('location'):
                    component['location'] = kanal
                else:
                    component.add('location', kanal)
                    
                master_cal.add_component(component)
                ant_matcher += 1
                hittade_i_denna += 1
            print(f"-> Lade till {hittade_i_denna} matcher från {namn_kalender}.")
        else:
            print(f"-> Kunde inte hämta {namn_kalender}, status: {response.status_code}")
    except Exception as e:
        print(f"-> FEL vid hämtning av {namn_kalender}: {e}")

print(f"Totalt tillagda matcher i alla kalendrar: {ant_matcher}")

# Spara den sammanslagna filen
with open('kalender.ics', 'wb') as f:
    f.write(master_cal.to_ical())
print("kalender.ics sparad!")
