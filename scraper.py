import icalendar
import requests

# Dina färdiga .ics-länkar från Sync2Cal
ics_länkar = [
    ("IFK Göteborg Herr", "http://ics.sync2cal.com/categories/get_ics/1b9695d3-2450-4686-aead-ceadabd9a0fe.ics"),
    ("Frölunda HC Herr", "https://ics.sync2cal.com/categories/get_ics/c0354fb4-73e4-47cb-815b-6d662eac6d64.ics"),
    ("Sverige Hockey Herr", "http://ics.sync2cal.com/categories/get_ics/3fb2c55b-b904-47e8-94b8-c646c78cda8f.ics"),
    ("Sverige Fotboll Dam", "http://ics.sync2cal.com/categories/get_ics/4504b764-fe86-4c52-b353-b25545b6d03f.ics"),
    ("Sverige Fotboll Herr", "https://ics.sync2cal.com/categories/get_ics/6a9f72e6-9fc7-440b-9482-9e92aa1a95ba.ics")
]

def bestam_kanal(sammanfattning):
    namn = sammanfattning.lower()
    if "frölunda" in namn:
        return "TV4 Play Hockey"
    elif "ifk göteborg" in namn:
        return "Max / Discovery+"
    elif "sverige" in namn:
        return "SVT / Viaplay"
    return "TV4 Play"

master_cal = icalendar.Calendar()
master_cal.add('prodid', '-//Sport Kalender Generator//briola80//SV')
master_cal.add('version', '2.0')

headers = {'User-Agent': 'Mozilla/5.0'}
ant_matcher = 0

for namn_kalender, url in ics_länkar:
    try:
        print(f"Hämtar {namn_kalender}...")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Statuskod för {namn_kalender}: {response.status_code}")
        
        if response.status_code == 200:
            ics_text = response.content.decode('utf-8', errors='ignore')
            cal = icalendar.Calendar.from_ical(ics_text)
            
            hittade_i_denna = 0
            for component in cal.walk('vevent'):
                summary = str(component.get('summary', ''))
                kanal = bestam_kanal(summary)
                component.add('location', kanal, overwrite=True)
                master_cal.add_component(component)
                ant_matcher += 1
                hittade_i_denna += 1
            print(f"-> Lade till {hittade_i_denna} matcher från {namn_kalender}.")
        else:
            print(f"-> Kunde inte hämta {namn_kalender}, status: {response.status_code}")
    except Exception as e:
        print(f"-> FEL vid hämtning av {namn_kalender}: {e}")

print(f"Totalt tillagda matcher i alla kalendrar: {ant_matcher}")

if ant_matcher > 0:
    with open('kalender.ics', 'wb') as f:
        f.write(master_cal.to_ical())
    print("kalender.ics sparad!")
else:
    print("VARNING: Inga matcher hittades. Skapar en grundläggande fil.")
    with open('kalender.ics', 'wb') as f:
        f.write(master_cal.to_ical())
```[cite: 9]
