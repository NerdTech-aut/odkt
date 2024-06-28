# Open Data Karten Tool
### Was macht das Open Data Karten Tool?
Mit dem Open Data Karten Tool können detaillierte Karten für die Mobilfunk und Festnetz Anbieter in Österreich erstellt werden.

Aktuell können die folgenden Daten mit dem Tool visualisiert werden:
- A1 Telekom Austria - 5G n78 und Speedmap
- Magenta Telekom - 5G n78 und Speedmap
- Hutchison Drei Austria - 5G n78 und Speedmap
- Mass Response aka. Spusu - 5G n78
- LIWEST - 5G n78
- Graz Holding Citycom - 5G n78
- Salzburg AG Cable Link Ai - 5G n78
- Festnetz von allen Netzbetreibern
- Geförderter Breitbandausbau

### Verwendung des Open Data Karten Tools:
Das Open Data Karten Tool stellt eine grafische Oberfläche bereit um eine an die eigenen Bedürfnisse angepasste Karten mit den oben genannten Daten zu erstellen.
Damit die Software funktioniert müssen die oben genannten Daten vorab mit dem "Daten aktualisieren" Button in eine lokale Datenbank heruntergeladen werden.
Um eine Karte zu erstellen muss der Mittelpunkt der Karte als ETRS89e Raster-ID (kann z.B. vom [Breitbandatlas](https://breitbandatlas.gv.at/) kopiert werden), als klassische Koordinaten oder als Adresse eingegeben werden.
Außerdem muss der Radius um den Mittelpunkt eingegeben werden wobei es Standardwert von zwei Kilometer vordefiniert ist.
Zuletzt werden die gewünschten Daten ausgewählt bevor die Karte mit "Karte erstellen" erstellt wird.
Diese Karte wird im Anschluss im Open Data Karten Tool angezeigt und kann als HTML-Datei zum Teilen und zur Darstellung im einem Webbrowser exportiert werden.

### Woher kommen die Daten?
Das Open Data Karten Tool kann Daten aus mehreren Quellen automatisch herunterladen, welche im Anschluss visualisiert werden können.
Die Daten bezüglich Mobilfunk werden von den Mobilfunkanbietern veröffentlicht und sind unter der [CC BY 4.0 Lizenz](https://creativecommons.org/licenses/by/4.0/deed.de) verfügbar.
Eine Übersicht über diese Daten kann auf [dieser Webseite der RTR](https://www.rtr.at/TKP/was_wir_tun/telekommunikation/spectrum/framework/Open_Data.de.html) abgerufen werden.  
Daten bezüglich Festnetz und gefördertem Breitbandausbau werden vom Bundesministerium für Finanzen und RUNDFUNK UND TELEKOM REGULIERUNGS-GMBH [auf der Webseite data.gv.at - Bundeskanzleramt](https://www.data.gv.at/katalog/dataset/588b9fdc-d2dd-4628-b186-f7b974065d40) und [auf der Webseite bmf.gv.at - Bundesministerium für Finanzen](https://www.bmf.gv.at/themen/telekommunikation-post_2/breitband/breitbandfoerderung/projekte.html) unter der [CC BY 3.0 AT Lizenz](https://creativecommons.org/licenses/by/3.0/at/deed.de) veröffentlicht.

### Warum ist das Open Data Karten Tool nützlich?
Das Open Data Karten Tool bietet die Möglichkeit die Daten, welche die Mobilfunkanbieter veröffentlichen müssen, besser zu visualisieren.
Es kann eine Karte mit demselben Kartenmaterial mit den Daten von mehreren Anbietern erstellt werden, wodurch Vergleiche der theoretisch Abdeckung besser möglich sind. 
Zusätzlich können auch Daten für Festnetz für jeden Netzbetreiber visualisiert werden, wobei Bandbreiten für A1 xDSL auf jene von Privatkunden nutzbaren angepasst werden.
Außerdem können detailliertere Daten zu den Projekten des geförderten Breitbandausbaus auf derselben Karte dargestellt werden.

### Warum wird im Vergleich zu breitbandatlas.gv.at nur die halbe Bandbreite für A1 xDSL angezeigt?
Die auf [breitbandatlas.gv.at](https://breitbandatlas.gv.at/) angezeigte xDSL-Bandbreite ist jene Bandbreite welche durch den Einsatz von VDSL2LR-Bonding, VDSL2-Bonding oder VPlus-Bonding erreicht wird.  
Beim Bonding werden zwei DSL-Leitungen zu einer kombiniert, um die doppelte Datenrate zu erzielen.
Die meisten Unternehmen mit xDSL Tarifen bieten jedoch kein Bonding von zwei Leitungen an und die Unternehmen mit Bonding xDSL Tarifen bieten diese nur für Geschäftskunden an.
Da die meisten Menschen xDSL Bonding nicht nutzen können wurde beschlossen, die von diesem Tool gemeldete xDSL-Bandbreite zu ändern.  
Es gibt weitere Ungereimtheiten in den A1 Festnetz Daten, welche nicht korrigiert werden können (z.B.: bei Mobilfunkmasten oder FTTC-Kästen wird teilweise FTTH als verfügbar gemeldet).

## Systemvoraussetzungen:
- 16 Gigabyte Arbeitsspeicher
- 20 Gigabyte freier Speicherplatz
- Internetverbindung (Adressabfrage, Kartenmaterial und Download der Open Data Dateien)

## Installation:
### Repository herunterladen:
Dieses Repository kann entweder als Zip-Archiv oder über Git heruntergeladen werden.
Für diejenigen die das Repository über Git herunterladen wollen, nehme ich an, dass bekannt ist was zu tun ist.
Ansonsten das Repository einfach als Zip-Archiv herunterladen. Klicke dazu auf die grüne Schaltfläche "Code" und wählen im Anschluss die Option "Download ZIP". Nachdem der Download abgeschlossen ist, kann das ZIP-Archiv entpackt werden.

### Nützliche Software für Windows-Nutzer:
Windows 10 oder 11 Nutzer können sich die Installation mit der [Windows Terminal App aus dem Microsoft Store](https://www.microsoft.com/store/productId/9N0DX20HK701) deutlich erleichtern.
 
### Python:
Bitte zunächst sicherstellen, dass Python installiert ist.  
Wenn nicht sicher ist, ob Python bereits installiert ist, kann der folgende Befehl in einem Terminal-Fenster ausgeführt werden:
```
python -V
```
Wenn Python nicht installiert ist, bitte die aktuelle Version herunterladen.  
[Python Download-Seite](https://www.python.org/downloads/)  
[Python im Microsoft Store für Windows 10 & 11](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5)

### Python-Pakete:   
Nachdem Python erfolgreich installiert wurde, bitte die folgenden Pakete installieren:
- pyproj
- folium
- pywebview
- pandas
- geopandas
- beautifulsoup4
- geopy
- lxml

Ich habe eine Datei vorbereitet, um die Installation dieser Pakete zu erleichtern.  
Windows-Nutzer mit installierter Windows Terminal Anwendung: Im Datei Explorer rechts klicken im ODKT Ordner und auswählen der Option "In Terminal öffnen". Dadurch wird ein neues Windows Terminal Fenster an der richtigen Stelle geöffnet.  
Alle anderen öffnen einfach einen Terminal und navigieren zu dem Ordner.  
Jetzt müssen Sie nur noch diesen Befehl ausführen:
```
pip install -r requirements.txt
```
### Zusätzliche Software:
Unter Windows wird grundsätzlich Microsoft Edge WebView2 vorausgesetzt und sollte unter Windows 11 vorinstalliert sein.
Ob Microsoft Edge WebView2 installiert ist kann in der Einstellungen App im Bereich Apps durch Suchen von "webview" überprüft werden.
Wenn Microsoft Edge WebView2 nicht vorhanden ist bitte [Microsoft Edge WebView2 Evergreen](https://go.microsoft.com/fwlink/p/?LinkId=2124703) herunterladen und installieren.

## Wie kann aus diesen Daten eine Karte erstellt werden?
[styxer](https://www.lteforum.at/user/styxer.7288/) alias [styx3r](https://github.com/styx3r) hat mir die Grundlagen erklärt:
Die Position für jedes Quadrat muss mit [pyproj](https://pyproj4.github.io/pyproj/stable/) (Python-Bibliothek) in reguläre Koordinaten umgewandelt werden.  
Um dies zu ermöglichen habe ich [re](https://www.w3schools.com/python/python_regex.asp) (Python RegEx) verwendet, um die Positionsdaten in drei Teile aufzuteilen (Maßstab, Norden und Osten).  
Der Maßstab dieser Daten ist 100 Meter.  
Um ein Quadrat zu erhalten, muss für jede Ecke eine Transformation durchgeführt werden (links unten, rechts unten, rechts oben und links oben).
```
from pyproj import Transformer
import re

LAEA_Europe_split = re.split('mN|E','100mN28000E47000')
scale = int(WSG84_split[0])
north = int(WSG84_split[1])
east = int(WSG84_split[2])

transformer = Transformer.from_crs(3035, 4326)

transformation_result_lower_left = transformer.transform((north * scale), (east * scale))
transformation_result_lower_right = transformer.transform((north * scale), ((east + 1) * scale))
transformation_result_top_right = transformer.transform(((north + 1) * scale), ((east + 1) * scale))
transformation_result_top_left = transformer.transform(((north + 1) * scale), (east * scale))
```

## Informationen zu den Bestandteilen vom Open Data Karten Tool:
### Grafische Oberfläche
Die grafische Oberfläche wird mit HTML Dateien realisiert.
Sowohl die Konfigurationsseite als auch die Karte sind mit Web-Technologien realisiert.
Die grafische Oberfläche und Verknüpfung zum Python Backend wurde mit der [pywebview](https://pywebview.flowrl.com/) Bibliothek implementiert
### Kartendarstellung:
Die Kartendarstellung wird mit [Leaflet.js](https://leafletjs.com/) realisiert und verwendet [OpenStreetMap](https://www.openstreetmap.org/) Kartenmaterial.
Leaflet.js wurde mit der [Folium](https://python-visualization.github.io/folium/latest/) Bibliothek implementiert
### Adressabfrage:
Die Adressabfrage wird über [Nominatim](https://nominatim.org/) realisiert und wandelt Adressen mittels [OpenStreetMap](https://www.openstreetmap.org/) Daten im Koordinaten um.
Nominatim wurde mit der [geopy](https://geopy.readthedocs.io/en/stable/) Bibliothek implementiert.

## Veränderungen an den Open Data Dateien:
### Mobilfunk Open Data:
- Ersetzen der leicht unterschiedlichen Kopfzeilen der CSV Dateien durch eine einheitliche Kopfzeile
- Ersetzen der nicht im UTF-8 Zeichenset enthaltenen Anführungszeichen in den A1 Open Data Dateien durch jene die im UTF-8 Zeichenset enthalten sind und von den anderen Mobilfunkanbietern für ihre Open Data Dateien verwendet werden.
- Aufteilen der Raster-ID in separate Spalten für Norden und Osten sowie das Entfernen der Skalierung, da diese einheitlich ist
- Entfernen der Spalten Operator, Reference und License
### Festnetz Open Data:
- Aufteilen der Raster-ID in separate Spalten für Norden und Osten sowie das Entfernen der Skalierung, da diese einheitlich ist
- Entfernen der Spalte agg_id
### Geförderter Ausbau Open Data:
- BBA2020: Entfernen der Spalten Förderungsinstrument (auch in Spalte Ausschreibung enthalten), Bundesland, NUTS-3-ID, NUTS-3-Region, Investitionsstandort bei BBA2020: Connect, Organisationsart Detail, Wirtschaftszweig auf Ebene der NACE-Gruppe, Beihilfeinstrument, Ziel der Beihilfe, Bewilligungsbehörde und Nummer der Beihilfemaßnahme
- BBA2030: Entfernen der Spalten Förderungsinstrument (auch in Spalte Ausschreibung enthalten), Bundesland, NUTS-3-ID, NUTS-3-Region, Bezirkskennung, Bezirk, Gemeindekennung, Gemeinde, Organisationsart Detail, Wirtschaftszweig auf Ebene der NACE-Gruppe, Beihilfeinstrument, Ziel der Beihilfe, Bewilligungsbehörde und Nummer der Beihilfemaßnahme

## Danksagung:
Danke an [styxer](https://www.lteforum.at/user/styxer.7288/) aka. [styx3r](https://github.com/styx3r) für die Bereitstellung der grundlegenden Konvertierung der Raster-ID in Koordinaten für dieses Projekt! Sein Projekt ist [hier](https://github.com/styx3r/breitbandatlas_analysis) abrufbar.  
Danke an [Jonas12](https://www.lteforum.at/user/jonas12.1666/) aka. [JonasGhost](https://github.com/JonasGhost) für die Mitwirkung am Code!