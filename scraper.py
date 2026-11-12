import icalendar
import requests
import re

favorit_länkar = [
    ("Allsvenskan - IFK Göteborg Dam", "https://calendar.google.com/calendar/ical/4p80oqf0abvv671j0esisb4b04%40group.calendar.google.com/public/basic.ics"),
    ("SHL - Frölunda HC Herr", "https://ics.ecal.com/ecal-sub/6af61f2ab13970000221c64a/Swedish%20Hockey%20League.ics"),
    ("SDHL - Frölunda HC Dam", "https://ics.ecal.com/ecal-sub/6af62014b13970000221c655/Swedish%20Hockey%20League.ics"),
    ("Liverpool FC", "https://pub.fotmob.com/prod/pub/api/v2/calendar/team/8650.ics"),
    ("Landslag Fotboll Herr", "https://pub.fotmob.com/prod/pub/api/v2/calendar/team/8520.ics"),
    ("Landslag Hockey (Tre Kronor)", "https://ics.sync2cal.com/categories/get_ics/3fb2c55b-b904-47e8-94b8-c646c78cda8f.ics"),
    ("Landslag Fotboll Dam", "https://pub.fotmob.com/prod/pub/api/v2/calendar/team/5814.ics")
]

def bestam_kanal(sammanfattning, kalender_namn=""):
    """Mappar automatiskt rätt svensk kanal baserat på lag, turnering och källkalender."""
    namn = sammanfattning.lower()
    k_namn = kalender_namn.lower()
    
    # Specifik regel för damernas Elitettan / IFK Göteborg Dam
    if "elitettan" in k_namn or "ifk göteborg dam" in k_namn or "dam" in k_namn and "ifk göteborg" in namn:
        return "Expressen +Allt"
    
    # Ishockey
    if "frölunda" in namn or "shl" in namn:
        return "TV4 Play Hockey"
    elif "sdhl" in k_namn or ("dam" in namn and "hockey" in namn):
        return "SVT Play"
        
    # Fotboll - Herr Allsvenskan / Superettan
    elif "ifk göteborg" in namn or "allsvenskan" in namn:
        return "Max / Discovery+"
        
    # Internationell fotboll
    elif "liverpool" in namn or "premier league" in namn or "champions league" in namn:
        return "Viaplay"
    elif "la liga" in namn or "serie a" in namn:
        return "TV4 Play"
        
    # Landslag (Herr/Dam)
    elif "sverige" in namn or "tre kronor" in namn:
        if "herrar" in namn or "herr" in namn or "nations league" in namn:
            return "Viaplay SE / TV6"
        return "SVT / Viaplay"
        
    return "Viaplay / TV4 Play"

def städa_rubrik(summary_str):
    """Tar bort skräpord, emojis och ligaprefixer ur rubriken, samt behåller endast flaggor för landslag."""
    if any(ordet in summary_str.lower() for ordet in ["synced", "welcome"]):
        return None
        
    # Behåll endast tillåtna tecken + eventuella flagg-emojis (eller rensa bort andra emojis som klubbor 🏒)
    # Här rensar vi bort vanliga ikoner som hockeyklubbor men låter vanliga bokstäver och siffror vara kvar.
    rensad = re.sub(r'[^\w\s\-\–—äöåÄÖÅa-zA-Z0-9\U0001F1E6-\U0001F1FF]', '', summary_str)
    
    # Ta bort ligaprefixer i början
    rensad = re.sub(r'^(SHL|SDHL|Allsvenskan)\s*\|\s*', '', rensad, flags=re.IGNORECASE)
    
    return rensad.strip()

master_cal = icalendar.Calendar()
master_cal.add('prodid', '-//Olausson Sport Kalender//SV')
master_cal.add('version', '2.0')

headers = {'User-Agent': 'Mozilla/5.0'}
ant_matcher = 0

for namn_kalender, url in favorit_länkar:
    try:
        print(f"Hämtar favoriter för {namn_kalender}...")
        saker_url = url.replace("webcal://", "https://")
        response = requests.get(saker_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            ics_text = response.content.decode('utf-8', errors='ignore')
            cal = icalendar.Calendar.from_ical(ics_text)
            
            hittade_i_denna = 0
            for component in cal.walk('vevent'):
                original_summary = str(component.get('summary', ''))
                
                ny_summary = städa_rubrik(original_summary)
                if not ny_summary:
                    continue
                
                component['summary'] = ny_summary
                
                # Använd både matchtitel och källkalenderns namn för att få rätt kanal
                kanal = bestam_kanal(original_summary, namn_kalender)
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

print(f"Totalt tillagda favoritmatcher: {ant_matcher}")

with open('kalender.ics', 'wb') as f:
    f.write(master_cal.to_ical())
print("kalender.ics uppdaterad med korrekta kanaler och städade rubriker!")
