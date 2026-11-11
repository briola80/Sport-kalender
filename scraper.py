import datetime
import re
import urllib.request

# Alla dina tre Sync2Cal-länkar samlade i en lista
ICS_URLS = [
    "http://ics.sync2cal.com/categories/get_ics/6a9f72e6-9fc7-440b-9482-9e92aa1a95ba.ics",  # Sveriges landslag
    "http://ics.sync2cal.com/categories/get_ics/457ba07a-9d3a-4653-9acd-fa832141e8a6.ics",  # Allsvenskan (fyra lag)
    "http://ics.sync2cal.com/categories/get_ics/c0354fb4-73e4-47cb-815b-6d662eac6d64.ics",   # SHL - Frölunda HC
    "http://ics.sync2cal.com/categories/get_ics/782eb907-6267-4a6d-8c65-3b24c42b7b0e.ics"    # PL - Liverpool
]

def fetch_and_fix_ics():
    all_events = []
    header = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Olausson Sport Calendar//SV\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\n"
    
    # Hämta och loopa igenom samtliga länkar
    for url in ICS_URLS:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8', errors='ignore')
                events = content.split("BEGIN:VEVENT")
                if len(events) > 1:
                    all_events.extend(events[1:])
        except Exception as e:
            print(f"Kunde inte hämta länk {url}: {e}")

    new_events = []

    # Lista över svenska sportkanaler och tjänster
    channels = [
        "TV4 Play", "TV4 Hockey", "TV4 Sport", "TV4 Fotboll", "TV4 Motor", "TV4",
        "Max", "HBO Max", "Viaplay", "V Sport", "SVT1", "SVT2", "SVT Play", "SVT",
        "Kanal 5", "Kanal 9", "Discovery+", "Eurosport 1", "Eurosport 2", "Eurosport",
        "Prime Video", "Disney+"
    ]

    for event_str in all_events:
        lines = event_str.split("\r\n")
        if len(lines) < 2:
            lines = event_str.split("\n")
            
        description = ""
        summary = ""
        current_location = ""
        other_lines = []

        for line in lines:
            if line.startswith("DESCRIPTION:"):
                description = line[12:]
            elif line.startswith("SUMMARY:"):
                summary = line[8:]
            elif line.startswith("LOCATION:"):
                current_location = line[9:]
            else:
                if line.strip() and not line.startswith("END:VEVENT") and not line.startswith("END:VCALENDAR"):
                    other_lines.append(line)

        # Sök efter kanal i texten
        detected_channel = None
        search_text = f"{summary} {description} {current_location}"
        
        for ch in channels:
            if re.search(r'\b' + re.escape(ch) + r'\b', search_text, re.IGNORECASE):
                detected_channel = ch
                break

        # Sätt Plats-fältet till den hittade kanalen
        final_location = detected_channel if detected_channel else (current_location if current_location else "Se sändningstablå")

        fixed_event = "BEGIN:VEVENT\n"
        fixed_event += f"SUMMARY:{summary}\n"
        fixed_event += f"DESCRIPTION:{description}\n"
        fixed_event += f"LOCATION:{final_location}\n"
        for l in other_lines:
            fixed_event += f"{l}\n"
        fixed_event += "END:VEVENT"
        
        new_events.append(fixed_event)

    full_ics = header + "\n".join(new_events) + "\nEND:VCALENDAR"
    
    with open("kalender.ics", "w", encoding="utf-8") as f:
        f.write(full_ics)
    
    print(f"kalender.ics har skapats med {len(new_events)} matcher totalt!")

if __name__ == "__main__":
    fetch_and_fix_ics()
