import datetime
import re
import urllib.request

# Webcal/ICS-länk till dina lag (Allsvenskan, SHL, CHL eller TV-tablå)
# Ersätt länken nedan med din egen ICS-länk om du har en specifik från eCal/SHL/TVsporten!
ICS_URL = "http://ics.sync2cal.com/categories/get_ics/7d885003-80f8-4ee9-9b0a-6914d8fd28af.ics"

def fetch_and_fix_ics():
    # Hämta orginal-ICS
    req = urllib.request.Request(
        ICS_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Kunde inte hämta ICS: {e}")
        return

    events = content.split("BEGIN:VEVENT")
    header = events[0]
    new_events = []

    for event_str in events[1:]:
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

        # Sök efter kanal i beskrivningen (TV4 Play, Max, Viaplay, TV4, Kanal 5, etc.)
        detected_channel = None
        search_text = f"{summary} {description} {current_location}"
        
        channels = ["TV4 Play", "TV4 Hockey", "TV4 Sport", "TV4", "Max", "Viaplay", "SVT", "Kanal 5", "Eurosport"]
        for ch in channels:
            if re.search(r'\b' + re.escape(ch) + r'\b', search_text, re.IGNORECASE):
                detected_channel = ch
                break

        # Om ingen känd kanal hittades, behåll befintlig plats eller sätt standard
        final_location = detected_channel if detected_channel else (current_location if current_location else "Se sändningstablå")

        # Bygg ihop händelsen igen med LOCATION satt till kanalen!
        fixed_event = "BEGIN:VEVENT\n"
        fixed_event += f"SUMMARY:{summary}\n"
        fixed_event += f"DESCRIPTION:{description}\n"
        fixed_event += f"LOCATION:{final_location}\n"
        for l in other_lines:
            fixed_event += f"{l}\n"
        fixed_event += "END:VEVENT"
        
        new_events.append(fixed_event)

    # Slå ihop alla händelser och spara till kalender.ics
    full_ics = header + "\n".join(new_events) + "\nEND:VCALENDAR"
    
    with open("kalender.ics", "w", encoding="utf-8") as f:
        f.write(full_ics)
    
    print("kalender.ics uppdaterad med kanal i Plats-fältet!")

if __name__ == "__main__":
    fetch_and_fix_ics()
