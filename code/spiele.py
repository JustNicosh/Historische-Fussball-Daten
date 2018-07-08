#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv_handler

class MatchesSynchronizer():

	def __init__(self):
		self.mzMatchesPath = '../data/mz_data/$spiele.csv'
		self.mzTeamsPath = '../data/mz_data/liste_mannschaften.csv'
		self.mzCleanMatchesPath = '../data/mz_data/mz_matches.csv'
		self.mzCleanMatchesProblemesPath = '../data/mz_data/mz_matches_problemes.csv'

		self.hcMatchesPath = '../data/hc_data/1_Spiele.csv'
		self.hcResultsPath = '../data/hc_data/1_Ergebnisse.csv'
		self.hcMatchesBefore2007Path = '../data/hc_data/1_Spiele_bis_2007.csv'
		self.hcResultsNationalteamsPath = '../data/hc_data/1_Ergebnisse_Nationalteams.csv'
		self.hcMatchesBefore2007OnlyNationalteamsPath = '../data/hc_data/1_Spiele_bis_2007_Nationalteams.csv'
		self.hcMatchesWithTeamIdsPath = '../data/hc_data/1_Spiele_mit_team_ids.csv'
		self.hcCleanMatchesPath = '../data/hc_data/hc_matches.csv'

	def returnMzData(self):
		"""mz-db-table -> liste_mannschaften and spiele
		"""
		matches = csv_handler.CsvHandler().read_csv(self.mzMatchesPath, 'r', 'utf-8', configDelimiter = '$')
		teams = csv_handler.CsvHandler().read_csv(self.mzTeamsPath, 'r', 'utf-8')

		teams.append(['"USA"', '"UNITED S"', '"151"', '"151"'])
		teams.append(['"USA"', '"UNITED Ś"', '"151"', '"151"'])
		teams.append(['"Romania"', '"ROM"', '"40"', '"40"'])
		teams.append(['"Faroe Islands"', '"FAROE"', '"14"', '"14"'])
		teams.append(['"Schottland"', '"OTLAND"', '"43"', '"43"'])
		teams.append(['"Chile"', '"ILE"', '"61"', '"61"'])
		teams.append(['"Tschechien"', '"CZEC"', '"49"', '"49"'])
		teams.append(['"Soviet Union"', '"T UNION"', '"52"', '"52"'])
		teams.append(['"Soviet Union"', '"OVIET"', '"52"', '"52"'])
		teams.append(['"Mexiko"', '"MEX"', '"139"', '"139"'])
		teams.append(['"Costa Rica"', '"TA RICA"', '"126"', '"126"'])
		teams.append(['"Argentinien"', '"TINA"', '"58"', '"58"'])
		teams.append(['"Argentinien"', '"ARGENT"', '"58"', '"58"'])
		teams.append(['"Belarus"', '"ВЕLА"', '"56"', '"56"'])
		teams.append(['"Südkorea"', '"UTH KOREA"', '"184"', '"184"'])
		teams.append(['"Estland"', '"ЕЅТОNІА"', '"13"', '"13"'])
		teams.append(['"Israel"', '"RAEL"', '"24"', '"24"'])
		teams.append(['"VA Emirate"', '"UNITED ARAB EMIRATES"', '"191"', '"191"'])

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

			# if length of row does not match 25 columns or if match_date is missing
			if len(match) != 25 or match[3] == '':
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

	def createMzMatchesWithAndWithoutTeamIds(self):
		"""mz-db-table -> spiele convertion to mz_matches and mz_matches_problemes
		"""
		mzData = self.returnMzData()
		mzMatches = self.getTeamIds(mzData)
		mzMatches_with_team_ids = mzMatches['matches_with_team_ids']
		mzMatches_without_team_ids = mzMatches['matches_without_team_ids']

		cleanMzMatches_with_team_ids = []
		for match in mzMatches_with_team_ids:
			cleanMzMatches_with_team_ids.append([match[0].split('"')[1], match[3].split('"')[1], match[25].split('"')[1], match[26].split('"')[1]])

		csv_handler.CsvHandler().create_csv(cleanMzMatches_with_team_ids, 'mz_matches.csv')
		csv_handler.CsvHandler().create_csv(mzMatches_without_team_ids, 'mz_matches_problemes.csv', configDelimiter = '$')


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
		"""modified hc-db-table -> 1_Spiele_bis_2007 convertion to 1_Spiele_bis_2007_Nationalteams
		"""

		matches = csv_handler.CsvHandler().read_csv(self.hcMatchesBefore2007Path, 'r', 'utf-8')
		results = csv_handler.CsvHandler().read_csv(self.hcResultsNationalteamsPath, 'r', 'utf-8')

		allMatchIds = [result[1] for result in results]
		resultsWithWantedMatchIds = []

		for i in range(len(matches)):
			if matches[i][0] in allMatchIds:
				resultsWithWantedMatchIds.append(matches[i])

		csv_handler.CsvHandler().create_csv(resultsWithWantedMatchIds, '1_Spiele_bis_2007_Nationalteams.csv')

	def syncHcMatchesWithHcResults(self):
		"""modified hc-db-table -> 1_Ergebnisse_Nationalteams and 1_Spiele_bis_2007_Nationalteams synchronisation to 1_Spiele_mit_team_ids
		"""

		matches = csv_handler.CsvHandler().read_csv(self.hcMatchesBefore2007OnlyNationalteamsPath, 'r', 'utf-8')
		results = csv_handler.CsvHandler().read_csv(self.hcResultsNationalteamsPath, 'r', 'utf-8')

		for i in range(len(matches)):
			if i == 100 or i == 1000 or i == 10000 or i == 20000:
				print(i)
			for result in results:
				if matches[i][0].split('"""""""')[1] == result[1].split('"""')[1]:
					matches[i].append(result[2])

		csv_handler.CsvHandler().create_csv(matches, '1_Spiele_mit_team_ids.csv')

	def cleanHcmatchesWithTeamIds(self):
		"""modified hc-db-table -> 1_Spiele_mit_team_ids convertion to hc_matches
		"""

		matches = csv_handler.CsvHandler().read_csv(self.hcMatchesWithTeamIdsPath, 'r', 'utf-8')

		cleanMatches = []
		for match in matches:
			if len(match) != 13:
				continue
			cleanMatch = []
			cleanMatch.append(match[0].split('"""""""""""""""')[1])
			cleanMatch.append(match[1].split('"""""""""""""""')[1])
			cleanMatch.append(match[11].split('"""""""')[1])
			cleanMatch.append(match[12].split('"""""""')[1])
			cleanMatches.append(cleanMatch)

		csv_handler.CsvHandler().create_csv(cleanMatches, 'hc_matches.csv')

	def syncHcWithMzMatches(self):
		"""modified hc-db-table -> hc_matches synchronisation with modified mz-db-table -> mz_matches to sync_matches and mz_matches_not_matching_with_hc_matches
		"""

		hcMatches = csv_handler.CsvHandler().read_csv(self.hcCleanMatchesPath, 'r', 'utf-8')
		mzMatches = csv_handler.CsvHandler().read_csv(self.mzCleanMatchesPath, 'r', 'utf-8')

		identifiedMatches = []
		notIdentifiedMatches = []
		for mzMatch in mzMatches:
			found = False
			mzDate = mzMatch[1].split('.')
			modMzDate = mzDate[2] + '-' + mzDate[1] + '-' + mzDate[0]
			for hcMatch in hcMatches:
				if mzMatch[2] in hcMatch and mzMatch[3] in hcMatch and modMzDate in hcMatch:
					mzMatch.append(hcMatch[0])
					identifiedMatches.append(mzMatch)
					found = True
					break
			if not found:
				notIdentifiedMatches.append(mzMatch)

		csv_handler.CsvHandler().create_csv(identifiedMatches, 'sync_matches.csv')
		csv_handler.CsvHandler().create_csv(notIdentifiedMatches, 'mz_matches_not_matching_with_hc_matches.csv')

	def createListForHsRedaktion(self):
		"""Liste aller nicht identifizierten Spiele (aufgrund von nicht zuzuordnenden Team-Strings) für Redaktion aufabeiten.
		"""

		mzMatchesProblemes = csv_handler.CsvHandler().read_csv(self.mzCleanMatchesProblemesPath, 'r', 'utf-8', configDelimiter = '$')

		cleanerMatches = []
		for match in mzMatchesProblemes:
			try:
				cleanerMatches.append([match[0], match[3], match[9], match[10]])
			except:
				print(len(match))
				print(match)

		csv_handler.CsvHandler().create_csv(cleanerMatches, 'redaktion_mz_matches_problemes.csv')

	def run(self):
		#self.createMzMatchesWithAndWithoutTeamIds()
		#self.deleteHcMatchesAfter2007()
		#self.deleteHCResultsWithWrongTeams()
		#self.deleteHcMatchesWithWrongMatchIds()
		#self.syncHcMatchesWithHcResults()
		#self.cleanHcmatchesWithTeamIds()
		self.createListForHsRedaktion()

if __name__ == '__main__':
	MatchesSynchronizer().run()
