#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv_handler

class MatchesSynchronizer():

	def __init__(self):
		self.mzMatchesPath = '../data/mz_data/$spiele.csv'
		self.mzTeamsPath = '../data/mz_data/liste_mannschaften.csv'

		self.hcMatchesPath = '../data/hc_data/1_Spiele.csv'
		self.hcResultsPath = '../data/hc_data/1_Ergebnisse.csv'

		self.hcMatchesBefore2007Path = '../data/hc_data/1_Spiele_bis_2007.csv'
		self.hcResultsNationalteamsPath = '../data/hc_data/1_Ergebnisse_Nationalteams.csv'

	def returnMzData(self):
		matches = csv_handler.CsvHandler().read_csv(self.mzMatchesPath, 'r', 'utf-8', configDelimiter = '$')
		teams = csv_handler.CsvHandler().read_csv(self.mzTeamsPath, 'r', 'utf-8')

		teams.append(['"USA"', '"UNITED S"', '"151"', '"151"'])
		teams.append(['"USA"', '"UNITED Ś"', '"151"', '"151"'])
		teams.append(['"Romania"', '"ROM"', '"40"', '"40"'])
		teams.append(['"Faroe Islands"', '"FAROE"', '"14"', '"14"'])
		teams.append(['"Schottland"', '"OTLAND"', '"43"', '"43"'])
		teams.append(['"Chile"', '"ILE"', '"61"', '"61"'])
		teams.append(['"Tschechien"', '"CZEC"', '"49"', '"49"'])
		teams.append(['"Soviet Union"', '"T UNION"', '"49"', '"49"'])
		teams.append(['"Soviet Union"', '"OVIET"', '"49"', '"49"'])

		return {'matches': matches, 'teams': teams}

	def returnWeltId(self, teams, name):
		"""mz-db-table -> liste_mannschaften
		"""
		welt_id = ''
		
		for team in teams:
			if team[1].split('"')[1].upper() in name:
				welt_id = team[2]

		return welt_id

	def getTeamIds(self, data):
		"""mz-db-table -> spiele
		"""
		matches_with_team_ids= []
		matches_without_team_ids = []

		#miss_count = 0
		for match in data['matches']:

			# if length of row does not match 25 columns
			if len(match) != 25:
				matches_without_team_ids.append(match)
				continue

			welt_heim_id = match[19]
			welt_gast_id = match[20]
			heim_name = match[9]
			gast_name = match[10]

			if welt_heim_id == '"0"':
				welt_heim_id = self.returnWeltId(data['teams'], heim_name)
			if welt_gast_id == '"0"':
				welt_gast_id = self.returnWeltId(data['teams'], gast_name)

			# if team_id was not identified by team name
			if welt_heim_id == '' or welt_gast_id == '':
				matches_without_team_ids.append(match)
				#miss_count += 1
				#print(heim_name + ' - ' + gast_name)
				continue

			match.append(welt_heim_id)
			match.append(welt_gast_id)
			matches_with_team_ids.append(match)

		#print(miss_count)
		return {'matches_with_team_ids': matches_with_team_ids, 'matches_without_team_ids': matches_without_team_ids}

	def deleteHcMatchesAfter2007(self):
		"""hc-db-table -> 1_Spiele convertion to 1_Spiele_bis_2007
		"""

		matches = csv_handler.CsvHandler().read_csv(self.hcMatchesPath, 'r', 'utf-8')
		matchesBefore2008 = []
		for match in matches:
			try:
				if int(match[1].split('"')[1].split('-')[0]) < 2008:
					matchesBefore2008.append(match)
			except:
				continue

		csv_handler.CsvHandler().create_csv(matchesBefore2008, '1_Spiele_bis_2007.csv')

	def deleteHCResultsWithWrongTeams(self):
		"""hc-db-table -> 1_Ergebnisse convertion to 1_Ergebnisse_Nationalteams
		"""

		results = csv_handler.CsvHandler().read_csv(self.hcResultsPath, 'r', 'utf-8')
		teams = csv_handler.CsvHandler().read_csv(self.mzTeamsPath, 'r', 'utf-8')

		allTeamIds = [team[2] for team in teams]
		resultsWithWantedTeamIds = []

		for result in results:
			if result[2] in allTeamIds:
				resultsWithWantedTeamIds.append(result)

		csv_handler.CsvHandler().create_csv(resultsWithWantedTeamIds, '1_Ergebnisse_Nationalteams.csv')

	def deleteHcMatchesWithWrongMatchIds(self):
		"""hc-db-table -> 1_Spiele_bis_2007 convertion to 1_Spiele_bis_2007_Nationalteams
		"""

		matches = csv_handler.CsvHandler().read_csv(self.hcMatchesBefore2007Path, 'r', 'utf-8')
		results = csv_handler.CsvHandler().read_csv(self.hcResultsNationalteamsPath, 'r', 'utf-8')

		allMatchIds = [result[1] for result in results]
		resultsWithWantedMatchIds = []

		for i in range(len(matches)):
			if i == 0 or i == 50000 or i == 150000 or i == 300000 or i == 450000:
				print(matches[i])
			if matches[i][0] in allMatchIds:
				resultsWithWantedMatchIds.append(matches[i])

		csv_handler.CsvHandler().create_csv(resultsWithWantedMatchIds, '1_Spiele_bis_2007_Nationalteams.csv')

	def dev(self):
		#mzData = self.returnMzData()
		#mzMatches = self.getTeamIds(mzData)
		#mzMatches_with_team_ids = mzMatches['matches_with_team_ids']
		#mzMatches_without_team_ids = mzMatches['matches_without_team_ids']

		#self.deleteHcMatchesAfter2007()
		#self.deleteHCResultsWithWrongTeams()
		self.deleteHcMatchesWithWrongMatchIds()




if __name__ == '__main__':
	MatchesSynchronizer().dev()



# 1) -> NUR MATCH_IDS IN 1_SPIELE_BIS_2007 STEHEN LASSEN, DIE IN 1_ERGEBNISSE_NATIONALTEAMS AUFTAUCHEN
# 2) -> DIESE DOKUMENTE ZUSAMMENFÜGEN
# 3) -> MIT $SPIELE ABGLEICHEN UM DIE GESUCHTEN MATCH_IDS ZU ERHALTEN