# Rudi's PseudoCode Executor 
rpce

## Wie man Pseudocode-Dateien erstellen muss
Vor algorithm kann man beliebig viele Kommentarzeilen schreiben.

Die Pfeile in der Schnittstelle müssen wie folgt abgespeichert werden:
    \o ... Ausgangsparameter (Pfeil nach oben)
    \i ... Eingangsparameter (Pfeil nach unten)
    \b ... Übergangsparameter (Pfeil in beide Richtungen)

Parameter, die für Feldindexe benötigt werden, müssen vor den Feldern definiert werden
Feldgröße maximal 100

Nach den lokalen Variablen muss eine Zeile freigelassen werden.

## Known Bugs:

- Bei lokalen Arrays funktioniert die Deklaration nur mit "= 0" bzw. "= 'Wert'";
- Keine Unterstützung von case-statements