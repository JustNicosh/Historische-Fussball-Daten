#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv_handler

class ActionsSynchronizer():

	def __init__(self):
		self.mzKaderPath = '../data/mz_data/$kader.csv'
		self.mzKaderOnlyWithWeltIdsPath = '../data/mz_data/$mz_kader.csv'

		self.mzTorePath = '../data/mz_data/$tore.csv'
		self.mzSpielerPath = '../data/mz_data/$liste_spieler2.csv'

	def syncKaderWithWeltIds(self):
		"""
		"""
		kader = csv_handler.CsvHandler().read_csv(self.mzKaderPath, 'r', 'utf-8', configDelimiter = '$')
		spielerListe = csv_handler.CsvHandler().read_csv(self.mzSpielerPath, 'r', 'utf-8', configDelimiter = '$')

		knownWeltIds = []
		unknownWeltIds = []

		count = 0
		for kad in kader:
			found = False
			# kad[-1] -> welt_id (spieler)
			if kad[-1] != '"0"':
				found = True
				knownWeltIds.append(kad)
				continue
			# kad[-1] -> welt_id (spieler) und kad[2] -> spieler name
			elif kad[-1] == '"0"':
				for spieler in spielerListe:
					if kad[2] == spieler[-1]:
						found = True
						kad[-1] = spieler[5]
						knownWeltIds.append(kad)
						break
			if not found:
				count += 1
				unknownWeltIds.append(kad)
		
		csv_handler.CsvHandler().create_csv(knownWeltIds, '$mz_kader.csv', configDelimiter = '$')
		csv_handler.CsvHandler().create_csv(unknownWeltIds, '$mz_kader_problemes.csv', configDelimiter = '$')

	def syncToreWithWeltIds(self):
		"""
		"""
		kader = csv_handler.CsvHandler().read_csv(self.mzKaderOnlyWithWeltIdsPath, 'r', 'utf-8', configDelimiter = '$')
		tore = csv_handler.CsvHandler().read_csv(self.mzTorePath, 'r', 'utf-8', configDelimiter = '$')
		spielerListe = csv_handler.CsvHandler().read_csv(self.mzSpielerPath, 'r', 'utf-8', configDelimiter = '$')

		spielerNamesListe1 = [spieler[-1] for spieler in spielerListe]
		spielerNamesListe2 = [spieler[1] for spieler in spielerListe]

		toreWithWeltIds = []
		toreWithoutWeltIds = []

		was_there_count = 0
		normal_found_count = 0
		vor_n_count = 0
		v_nach_namen_count = 0
		nachnamen_count = 0
		not_found_count = 0
		
		#count = 0
		for tor in tore:
			found = False
			# Haben wir bereits eine welt_id?
			# tor[4] -> welt_id (spieler)
			if tor[4] != '"0"':
				toreWithWeltIds.append(tor)
				was_there_count += 1
				found = True
				continue
			# Haben wir keine welt_id, aber der Spielername taucht in der Kaderliste auf?
			# tor[4] -> welt_id (spieler) und tor[2] -> spieler name
			elif tor[4] == '"0"' and (tor[2] in spielerNamesListe1 or tor[2] in spielerNamesListe2):
				toreWithWeltIds.append(tor)
				normal_found_count += 1
				found = True
				continue
			elif not found:
				for kad in kader:
					try:
						# Kommt im richtigen Spiel der gleiche Vorname und der gleiche Anfangsbuchstabe des Nachnames vor?
						# kad[1] -> spiel_id und kad[2] -> spieler name
						if kad[1] == tor[1] and (kad[2].split(' ')[0] == tor[2].split(' ')[0] and kad[2].split(' ')[1][0] == tor[2].split(' ')[1][0]):
							toreWithWeltIds.append(tor)
							vor_n_count += 1
							print('..........VOR_N.............')
							print(tor)
							print(kad)
							found = True
							break
					except:
						found = False
			if not found:
				for kad in kader:
					try:
						# Kommt im richtigen Spiel der gleiche Nachname und der gleiche Anfangsbuchstabe des Vornamens vor?
						# kad[1] -> spiel_id und kad[2] -> spieler name
						if kad[1] == tor[1] and (kad[2].split(' ')[0][1] == tor[2].split(' ')[0][1] and kad[2].split(' ')[-1] == tor[2].split(' ')[-1]):
							toreWithWeltIds.append(tor)
							v_nach_namen_count += 1
							print('_________V_NACH__________')
							print(tor)
							print(kad)
							found = True
							break
					except:
						found = False
			if not found:
				for kad in kader:
					# Kommt im richtigen Spiel der gleiche Nachname vor (und die Fälle vorher trafen nicht ein)?
					# kad[1] -> spiel_id und kad[2] -> spieler name
					if kad[1] == tor[1] and (kad[2].split(' ')[-1] == tor[2].split(' ')[-1]) and kad[2] != '" "':
						toreWithWeltIds.append(tor)
						nachnamen_count += 1
						print('+++++++++NACH++++++++++')
						print(tor)
						print(kad)
						found = True
						break
			if not found:
				toreWithoutWeltIds.append(tor)
				not_found_count += 1

		print(was_there_count)
		print(normal_found_count)
		print(vor_n_count)
		print(v_nach_namen_count)
		print(nachnamen_count)
		print(not_found_count)

		'''
		26620
		10438
		1740
		816
		8577
		'''

		csv_handler.CsvHandler().create_csv(toreWithWeltIds, '$mz_tore.csv', configDelimiter = '$')
		csv_handler.CsvHandler().create_csv(toreWithoutWeltIds, '$mz_tore_problemes.csv', configDelimiter = '$')

	def run(self):
		self.syncToreWithWeltIds()

if __name__ == '__main__':
	ActionsSynchronizer().run()
