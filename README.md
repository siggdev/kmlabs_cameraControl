# KM Laboratory - CameraControl

## Hintergrund
In einer Box befinden sich ein MacMini und eine Systemkamera (unterschiedliche Typen), welche in einem definierten Rhythmus Bilder aufzeichnen und automatisch über das Internet an einen definierten Ort laden. Bisher ist jedoch nur einstellbar, welchen Abstand die Bilder haben (z.B. 15 Minuten). Es lässt sich kein Zeitraum einstellen, von wann bis wann diese Bilder gemacht und hochgeladen werden. Somit machen die Kameras auch in der Nacht Bilder, die aufgrund der nicht passenden Lichtverhältnisse einfach nur schwarz sind. Das ist zum einen Sortierarbeit und zum anderen natürlich auch verschleiß für die mechanischen Teile der Kamera.

## Ziel
Ziel ist es ein Relaisboard incl. Ansteuerung zu entwickeln, welches über einen Relaiskontakt die Kamera ansteuern kann und den Auslöser betätigt. Die Ansteuerung soll so einstellbar sein, dass ein Intervall in Minuten für den Abstand der Bilder festgelegt werden kann, dieses jedoch auf bestimmte Uhrzeiten und Tage beschränkt werden kann (z.B. Intervall 15 Minuten, nur Werktags von 10 bis 17 Uhr). Das Relaisboard soll dabei so ausgelegt werden, dass später über weitere Relais auch noch Zusatzkomponenten installiert werden können (z.B. ein Lüfter/Scheibenwischer bei beschlagener Linsenhaube).

## Umsetzung
Geplant ist das Projekt auf einem Raspberry Pi laufen zu lassen, da dieser über die notwendigen GPIOs verfügt, um die Relaisplatine anzusteuern. Passende Relaiskarten für MacOS sind schwer zu finden. Die Steuerung der GPIOs lässt sich am einfachsten über Python bewerkstelligen, weshalb Python als Hauptprogrammiersprache für dieses Projekt gewählt wurde. Um die Steuerung des Raspberrys so einfach und kompatibel wie möglich zu halten, wird dafür eine Weboberfläche mit Python und Flask getestet. Auf diesem Wege muss der Anwender nicht über eine Remoteverbindung auf den Raspberry gelangen, sondern kann diesen über den mit verbauten MacMini steuern.

### Hardware
#### Raspberry Pi 3B+ / 4 ([Link zur Produktseite][1])
Als Controller zur Steuerung wurde der Raspberry Pi ausgewählt. Dieser ist günstig in der Beschaffung, nutzt ein lizenzfreies Betriebssystem und bringt die notwendigen GPIOs mit, um Reilais ohne große Treiberaufwände zu steuern. Zudem ist er Leistungsfähig genug auch den Betrieb des Webservers und eventuell noch weitere folgende Aufgaben nebenbei mit leichtigkeit zu bewerkstelligen. Nachteil am Raspberry Pi ist, dass dieser als Systemlaufwerk eine SD-Karte verwendet. Da das Betriebssystem jedoch relativ viel im Normalbetrieb schreibt, alter diese sehr schnell und wird schnell defekt. Daher wird versucht die SD-Karte im ReadOnly Betrieb zu fahren und das Betriebssystem und die Aufgaben im RAM des Raspberrys zu betreiben. Eine Anleitung für eine mögliche Umsetzung findet sich z.B. [hier][2]. Nachteil dieser Variante ist, dass keine Daten persistent gespeichert werden könnne (z.B. Anzahl der gesamten Bilder geht bei einem Neustart verloren). Für solche Funktionen muss dann (falls gewünscht) eine Datenbank auf einem anderen Server betrieben werden.

#### 4-Kanal Relaismodul mit Optokoppler ([Link zur Produktseite][3])
Als Relaismodul wurde das 4-Kanal Relaismodul mit Optokoppler von Paradisetronics ausgewählt. Zum einen lässt es sich sowohl von einem Raspberry Pi als auch mit einem Arduino ohne weitere Hardware ansteuern, zum anderen bietet es mit insgesamt 4 verbauten Relais viel Möglichkeit zur Erweiterung. Auch die Möglichkeit über das Relais 10A mit 250V(AC) oder 30V(DC) zu schalten, lässt für die Zukunft viel Spielraum.

### Software + Bibliotheken
#### Python
Als Programmiersprache kommt [Python][4] in der Version 3.8 zum Einsatz. Dieses ist eine leichte, easy-to-use Programmiersprache und für sie existieren hunderte von Bibliotheken für die Steuerung eines Raspberry Pis. Am interessanntesten sind hier die Bibliotheken [RPi.GPIO][5] für die Steuerung der GPIOs und [Flask][6] für den Betrieb der Weboberfläche mit den Einstellungen.

### APIs
Um die Einstellungen einfacher zu machen, können über Web-APIs Daten für die Steuerung des Raspberrys gewonnen werden.

#### sunrise-sunset.org
Über die API von [sunrise-sunset.org][7] lassen sich (lizenzfrei und ohne Anmeldung oder Token) Informationen über das Tageslicht gewinnen. So kann man hier z.B. die Uhrzeiten für Sonnenaufgang und Sonnenuntergang eines bestimmten Datums abgerufen werden. Aber auch Informationen über weitere Zeitpunkte, wie z.B. Sonnenhöchststand, zivilies, nautisches und astronomisches Zwielicht lassen sich hier gewinnen.

## Linksammlung
### Hardware-Dokumentation
[Raspberry Pi 4B Produktseite][1]  
[Paradisetronic 4-Kanal Relaismodul mit Optokoppler][3]  

### Software-Dokumentation
[Python Dokumentation und Projektseite][4]  
[RPi.GPIO Bibliothek zur Steuerung von Raspberry-GPIOs][5]  
[Flask: Webserver und Bibliotheken für Python][6]  
[sunrise-sunset.org, API für Sonnenauf- und -untergang][7]  

### Anleitungen und HowTos
[Anleitung zum Betrieb eines Raspberrys mit RO-SD-Karte][2]  

[1]: https://www.raspberrypi.org/products/raspberry-pi-4-model-b/specifications/
[2]: https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353
[3]: https://paradisetronic.com/de/4-kanal-relais-modul-optokoppler-5v
[4]: https://www.python.org/
[5]: https://pypi.org/project/RPi.GPIO/
[6]: https://flask.palletsprojects.com/en/1.1.x/
[7]: https://sunrise-sunset.org/api
