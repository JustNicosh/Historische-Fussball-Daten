#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv_handler

class MatchesSynchronizer():

	def __init__(self):
		self.mzMatchesPath = '../data/mz_data/$spiele.csv'
		self.mzTeamsPath = '../data/mz_data/liste_mannschaften.csv'

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

	def dev(self):
		mzData = self.returnMzData()
		mzMatches = self.getTeamIds(mzData)
		mzMatches_with_team_ids = mzMatches['matches_with_team_ids']
		mzMatches_without_team_ids = mzMatches['matches_without_team_ids']
		print(len(mzMatches_without_team_ids))




if __name__ == '__main__':
	MatchesSynchronizer().dev()