#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

import csv_handler

class MatchesSynchronizer():

	def __init__(self):
		self.matchesPath = '../data/mz_data/$spiele.csv'
		self.teamsPath = '../data/mz_data/liste_mannschaften.csv'

	def returnData(self):
		matches = csv_handler.CsvHandler().read_csv(self.matchesPath, 'r', 'latin-1', configDelimiter = '$')
		teams = csv_handler.CsvHandler().read_csv(self.teamsPath, 'r', 'latin-1')

		teams.append(['"USA"', '"UNITED S"', '"151"', '"151"'])
		teams.append(['"USA"', '"TATE"', '"151"', '"151"'])
		teams.append(['"Romania"', '"ROM"', '"40"', '"40"'])
		teams.append(['"Faroe Islands"', '"FAROE"', '"14"', '"14"'])

		return {'matches': matches, 'teams': teams}

	def returnWeltId(self, teams, name):
		welt_id = ''
		
		for team in teams:
			if team[1].split('"')[1].upper() in name:
				welt_id = team[2]

		return welt_id

	def synchronizeMatches(self):
		data = self.returnData()

		heim_miss_count = 0
		gast_miss_count = 0

		for match in data['matches']:

			# if length of row does not match 25 columns -> something is wrong
			if len(match) != 25:
				continue

			welt_heim_id = match[19]
			welt_gast_id = match[20]

			heim_name = match[9]
			gast_name = match[10]

			if welt_heim_id == '"0"':
				welt_heim_id = self.returnWeltId(data['teams'], heim_name)

				if welt_heim_id == '':
					heim_miss_count += 1
					print('heim -> '+str(heim_miss_count)+' '+heim_name)

			if welt_gast_id == '"0"':
				welt_gast_id = self.returnWeltId(data['teams'], gast_name)

				if welt_gast_id == '':
					gast_miss_count += 1
					print('gast -> '+str(gast_miss_count)+' '+gast_name)

		print(heim_miss_count)
		print(gast_miss_count)





if __name__ == '__main__':
	MatchesSynchronizer().synchronizeMatches()