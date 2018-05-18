#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv_handler

class ActionsSynchronizer():

	def __init__(self):
		self.mzKaderPath = '../data/mz_data/$kader.csv'
		self.mzTorePath = '../data/mz_data/$tore.csv'
		self.mzSpielerPath = '../data/mz_data/$liste_spieler2.csv'

	def test(self):
		"""
		"""
		kader = csv_handler.CsvHandler().read_csv(self.mzKaderPath, 'r', 'utf-8', configDelimiter = '$')
		tore = csv_handler.CsvHandler().read_csv(self.mzTorePath, 'r', 'utf-8', configDelimiter = '$')
		spielerListe = csv_handler.CsvHandler().read_csv(self.mzSpielerPath, 'r', 'utf-8', configDelimiter = '$')

		spielerNamesListe1 = [spieler[-1] for spieler in spielerListe]
		spielerNamesListe2 = [spieler[1] for spieler in spielerListe]

		# IN 2 VERSCHIEDENE METHODEN AUFTEILEN: KADER UND TORE!

		"""
		count = 0
		for kad in kader:
			# kad[-1] -> welt_id (spieler)
			if kad[-1] != '"0"':
				continue
			# kad[-1] -> welt_id (spieler) und kad[2] -> spieler name
			if kad[-1] == '"0"' and kad[2] in spielerNamesListe1:
				continue
			else:
				count += 1
				#print(kad)
		print(count)
		"""
		
		# ERST KADER MIT WELT_IDS AUFFRISCHEN, DANN DEN NACHNAMEN-ABGLEICH MACHEN
		# (UND IN DIESEM ZUGE DIE WELT_IDS ÜBERNEHMEN)

		nachnamen_count = 0
		vornamen_count = 0
		#count = 0
		for tor in tore:
			# tor[4] -> welt_id (spieler)
			if tor[4] != '"0"':
				continue
			# tor[4] -> welt_id (spieler) und tor[2] -> spieler name
			if tor[4] == '"0"' and (tor[2] in spielerNamesListe1 or tor[2] in spielerNamesListe2):
				continue
			# tor[2] -> spieler name und tor[1] -> spiel_id
			else:
				try:
					for kad in kader:
						# kad[1] -> spiel_id und kad[2] -> spieler name
						if kad[1] == tor[1] and (kad[2].split(' ')[-1] == tor[2].split(' ')[-1]):
							nachnamen_count += 1
							print('________NACH___________')
							print(tor)
							print(kad)
							break
						# kad[1] -> spiel_id und kad[2] -> spieler name
						elif kad[1] == tor[1] and (kad[2].split(' ')[0] == tor[2].split(' ')[0] and kad[2].split(' ')[1][0] == tor[2].split(' ')[1][0]):
							vornamen_count += 1
							print('..........VOR.............')
							print(tor)
							print(kad)
							break
					continue
				except:
					continue
			#else:
				#count += 1
				#print(tor)
		#print(count)
		print(nachnamen_count)
		print(vornamen_count)

	def run(self):
		self.test()

if __name__ == '__main__':
	ActionsSynchronizer().run()
