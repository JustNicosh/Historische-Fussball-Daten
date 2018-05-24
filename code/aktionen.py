#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv_handler

class ActionsSynchronizer():

	def __init__(self):
		self.mzKaderPath = '../data/mz_data/$kader.csv'
		self.mzTorePath = '../data/mz_data/$tore.csv'
		self.mzSpielerPath = '../data/mz_data/$liste_spieler2.csv'

	def syncKaderWithWeltIds(self):
		"""
		"""
		kader = csv_handler.CsvHandler().read_csv(self.mzKaderPath, 'r', 'utf-8', configDelimiter = '$')
		spielerListe = csv_handler.CsvHandler().read_csv(self.mzSpielerPath, 'r', 'utf-8', configDelimiter = '$')

		#spielerNamesListe1 = [spieler[-1] for spieler in spielerListe]
		#spielerNamesListe2 = [spieler[1] for spieler in spielerListe]

		count = 0
		for kad in kader:
			found = False
			# kad[-1] -> welt_id (spieler)
			if kad[-1] != '"0"':
				found = True
				continue
			# kad[-1] -> welt_id (spieler) und kad[2] -> spieler name
			elif kad[-1] == '"0"':
				for spieler in spielerListe:
					if kad[2] == spieler[-1]:
						found = True
						break
			if not found:
				count += 1
				#print(kad)
		print(len(kader))
		print(count)


	def syncToreWithWeltIds(self):
		"""
		"""
		kader = csv_handler.CsvHandler().read_csv(self.mzKaderPath, 'r', 'utf-8', configDelimiter = '$')
		tore = csv_handler.CsvHandler().read_csv(self.mzTorePath, 'r', 'utf-8', configDelimiter = '$')
		spielerListe = csv_handler.CsvHandler().read_csv(self.mzSpielerPath, 'r', 'utf-8', configDelimiter = '$')

		spielerNamesListe1 = [spieler[-1] for spieler in spielerListe]
		spielerNamesListe2 = [spieler[1] for spieler in spielerListe]
		
		# ERST KADER MIT WELT_IDS AUFFRISCHEN, DANN DEN NACHNAMEN-ABGLEICH MACHEN
		# (UND IN DIESEM ZUGE DIE WELT_IDS ÜBERNEHMEN)

		vor_n_count = 0
		v_nach_namen_count = 0
		nachnamen_count = 0
		
		#count = 0
		for tor in tore:
			found = False
			# Haben wir bereits eine welt_id?
			# tor[4] -> welt_id (spieler)
			if tor[4] != '"0"':
				found = True
				continue
			# Haben wir keine welt_id, aber der Spielername taucht in der Kaderliste auf?
			# tor[4] -> welt_id (spieler) und tor[2] -> spieler name
			elif tor[4] == '"0"' and (tor[2] in spielerNamesListe1 or tor[2] in spielerNamesListe2):
				found = True
				continue
			elif not found:
				for kad in kader:
					try:
						# kad[1] -> spiel_id und kad[2] -> spieler name
						if kad[1] == tor[1] and (kad[2].split(' ')[0] == tor[2].split(' ')[0] and kad[2].split(' ')[1][0] == tor[2].split(' ')[1][0]):
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
						# kad[1] -> spiel_id und kad[2] -> spieler name
						if kad[1] == tor[1] and (kad[2].split(' ')[0][1] == tor[2].split(' ')[0][1] and kad[2].split(' ')[-1] == tor[2].split(' ')[-1]):
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
					# kad[1] -> spiel_id und kad[2] -> spieler name
					if kad[1] == tor[1] and (kad[2].split(' ')[-1] == tor[2].split(' ')[-1]):
						nachnamen_count += 1
						print('+++++++++NACH++++++++++')
						print(tor)
						print(kad)
						found = True
						break
			
			#else:
				#count += 1
				#print(tor)
		#print(count)
		print(vor_n_count)
		print(v_nach_namen_count)
		print(nachnamen_count)

	def run(self):
		self.syncKaderWithWeltIds()

if __name__ == '__main__':
	ActionsSynchronizer().run()
