# Sportkalender 🏆🏒⚽

En automatiserad sportkalender som samlar matcher och sändningskanaler för prioriterade favoritlag och turneringar. Skriptet körs automatiskt via GitHub Actions för att hålla `.ics`-filen uppdaterad.

## 📌 Funktioner
* **Automatiska uppdateringar:** Hämtar och uppdaterar spelscheman via GitHub Actions.
* **Kanalinformation:** Sätter automatiskt rätt sändande kanal (t.ex. *Max*, *TV4 Play Hockey*, *Viaplay*, *Expressen +Allt*) direkt i kalenderhändelsens platsfält (`LOCATION`).
* **Städade rubriker:** Rensar bort skräpnotiser, onödiga emojis och ligaprefixer för en ren och överskådlig kalender i telefonen.
* **Webbapp (GUI):** Innehåller även en interaktiv webbapp (`index.html`) för att bläddra bland matcher och filtrera.

---

## 📱 Prenumerera i iPhone / Apple Kalender
För att prenumerera på kalendern i din telefon, lägg till följande publika länk som en prenumererad kalender:

```text
[https://raw.githubusercontent.com/briola80/Sport-kalender/refs/heads/main/kalender.ics](https://raw.githubusercontent.com/briola80/Sport-kalender/refs/heads/main/kalender.ics)
