# Historische-Fussball-Daten

mz -> mz_buch_parser -> spiele
------------------------------

-> STRUKTUR: spiel_id (PI) | datum | heim_welt_id (HC) | gast_welt_id (HC) | ...
-> PROBLEM: nur bei 1500 von 27000 ist heim_welt_id zugeordnet

-> TODO:
	1) heim_welt_id | gast_welt_id auffüllen (mithilfe von mz -> laender und mz -> liste_mannschaften)
	2) über datum | heim_welt_id (HC) | gast_welt_id (HC) mithilfe der HC-Tabellen "1_Spiele" und "1_Ergebnisse" die match_ids (HC) ergänzen

mz -> mz_buch_parser -> kader / tore
------------------------------------

-> STRUKTUR: spiel_id (PI) | welt_id | ...
-> PROBLEM: 48000 von 348000 (kader) bzw. 43000 von 48000 (tore) haben keine welt_id

-> TODO:
	1) welt_ids auffüllen (mithilfe von mz -> spieler_liste2, welche evtl. noch ergänzt werden muss)
	2) match_ids (HC) über "mz -> mz_buch_parser -> spiele" ergänzen (sobald möglich)

