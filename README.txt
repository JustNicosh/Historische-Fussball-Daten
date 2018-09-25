Historische Fussballdaten – Readme

Datenlage

Inhalt der MZ-DB:
kader_rohdaten
tore_rohdaten
spiele_rohdaten
liste_spieler2_rohdaten
liste_mannschaften_rohdaten

Benötigte Tabellen aus der HC-DB:
1_Spiele
1_Ergebnisse

Vorgehen

1) Spiele

Zeilen (verschiedene Spiele) in spiele_rohdaten: 27.032 
Synchronisation mit liste_mannschaften_rohdaten und eigener kleiner DB zu 1.1)

1.1) mz_matches und mz_matches_problemes

Zeilen (verschiedene Spiele) in mz_matches: 25.330
Zeilen (verschiedene Spiele) in mz_matches_problemes: 1.702
Grund der Probleme: Teamnamen wie "LAT%IA" wurden nicht identifiziert
Synchronisation mit 1_Spiele und 1_Ergebnisse zu 1.2)

1.2) sync_matches und sync_matches_problemes

Zeilen (verschiedene Spiele) in sync_matches: 21.939
Zeilen (verschiedene Spiele) in sync_matches_problemes: 3.391
Grund der Probleme: Zum angegebenen Datum (Bsp.: 22.08.1946) hat laut HC-DB kein Spiel zwischen zwei angegebenen Teams (Bsp.: Albanien – Montenegro) stattgefunden

2) Aktionen – Kader

Zeilen (verschiedene Kadereinträge) in kader_rohdaten: 348.052
Synchronisation mit liste_spieler2_rohdaten zu 2.1)

2.1) mz_kader und mz_kader_problemes

Zeilen (verschiedene Kadereinträge) in  mz_kader: 305.980
Zeilen (verschiedene Kadereinträge) in  mz_kader_problemes: 42.070
Grund der Probleme: Spieler (Bsp.: Davor duker) tauchen nicht in der Spielerliste auf
Synchronisation mit sync_matches zu 2.2)

2.2) sync_kader und sync_kader_problemes

Zeilen (verschiedene Kadereinträge) in  sync_kader: 248.290
Zeilen (verschiedene Kadereinträge) in  sync_kader_problemes: 57.690
Grund der Probleme: Matches, welche nicht zugeordnet werden konnten und sich in sync_matches_problemes befinden, tauchen nicht in sync_matches auf (Bsp.:  Albanien – Montenegro vom  22.08.1946, s.o.)

3) Aktionen – Tore

Zeilen (verschiedene Toreinträge) in tore_rohdaten: 48.191
Synchronisation mit liste_spieler2_rohdaten, mz_kader und eigener Suche zu 3.1)

3.1) mz_tore und mz_tore_problemes

Zeilen (verschiedene Toreinträge) in mz_tore: 42.300
Zeilen (verschiedene Toreinträge) in mz_tore_problemes: 8.577
Grund der Probleme: Spieler (Bsp.: Davor duker) tauchen nicht in der Spielerliste auf
Synchronisation mit sync_matches zu 3.2)

3.2) sync_tore und sync_tore_problemes

Zeilen (verschiedene Toreinträge) in  sync_tore: 30.341
Zeilen (verschiedene Toreinträge) in  sync_tore_problemes: 11.959
Grund der Probleme: Matches, welche nicht zugeordnet werden konnten und sich in sync_matches_problemes befinden, tauchen nicht in sync_matches auf (Bsp.:  Albanien – Montenegro vom  22.08.1946, s.o.) + Viele Matches, welche mit einer MZ-internen spiel_id in tore_rohdaten (und damit auch in mz_tore) gelistet werden, tauchen nicht in spiele_rohdaten (und damit auch nicht in mz_matches und sync_matches) auf


ToDo

-> Mit aktuellem sync_matches aktuelle Versionen von sync_tore und sync_kader erstellen


