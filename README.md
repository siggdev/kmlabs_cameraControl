# KM Laboratory - CameraControl

## Hintergrund
In einer Box befinden sich ein MacMini und eine Systemkamera (unterschiedliche Typen), welche in einem definierten Rhythmus Bilder aufzeichnen und automatisch über das Internet an einen definierten Ort laden. Bisher ist jedoch nur einstellbar, welchen Abstand die Bilder haben (z.B. 15 Minuten). Es lässt sich kein Zeitraum einstellen, von wann bis wann diese Bilder gemacht und hochgeladen werden. Somit machen die Kameras auch in der Nacht Bilder, die aufgrund der nicht passenden Lichtverhältnisse einfach nur schwarz sind. Das ist zum einen Sortierarbeit und zum anderen natürlich auch verschleiß für die mechanischen Teile der Kamera.

## Ziel
Ziel ist es ein Relaisboard incl. Ansteuerung zu entwickeln, welches über einen Relaiskontakt die Kamera ansteuern kann und den Auslöser betätigt. Die Ansteuerung soll so einstellbar sein, dass ein Intervall in Minuten für den Abstand der Bilder festgelegt werden kann, dieses jedoch auf bestimmte Uhrzeiten und Tage beschränkt werden kann (z.B. Intervall 15 Minuten, nur Werktags von 10 bis 17 Uhr). Das Relaisboard soll dabei so ausgelegt werden, dass später über weitere Relais auch noch Zusatzkomponenten installiert werden können (z.B. ein Lüfter/Scheibenwischer bei beschlagener Linsenhaube).
