#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import urllib2
import bs4
import csv_handler

class FabianParserModifier():
	"""Automatismus, um im Editor (Buch-Parser von Fabian) alle noch nicht zugeordneten Spieler (Kadereintraege und Torschuetzen) mit dem wahrscheinlichsten Treffer zu matchen.
		-> http://prj.endstand.de/fabian/buch-parser/dbeditor.php
	"""

	def __init__(self):
		self.buchParserUrl = 'http://prj.endstand.de/fabian/buch-parser/dbeditor.php'
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive'}

	def returnWebContent(self, url):
		request = urllib2.Request(url, headers = self.headers)
		try:
			response = urllib2.urlopen(request)
			return {'content': bs4.BeautifulSoup(response, 'html.parser'), 'failed': False}
		except:
			print('Error: Could not open ' + url)
			return {'failed': True}
	
	def writeAllDateiIdsForAllCountriesIntoCsv(self):
		# Loop durch alle Laender (bis inkl. Chile), Datei-Infos pro Land in Liste speichern
		for i in range(1, 62):

			# Oesterreich, Deutschland, DDR, Niederlande und Bolivien rauslassen
			if i == 4 or i == 20 or i == 21 or i == 23 or i == 59:
				continue

			webContent = self.returnWebContent(self.buchParserUrl + '?land=' + str(i))['content']
			dateiInfosList = str(webContent).split('<h4>Datei</h4>')[1].split('<br/><br/><a')[0].replace('&gt;&gt; <a href="?land=' + str(i) + '&amp;datei=', '').splitlines()
			
			# Loop durch alle Datei-Infos, nur Datei-Nummer extrahieren und in Liste speichern
			allDateien = [str(i)]
			for j in range(1, len(dateiInfosList)):
				allDateien.append(dateiInfosList[j].split('">')[0])

			# Jeweils Land mit allen dazugehoerigen Dateien speichern
			csv_handler.CsvHandler().create_csv([allDateien], 'alle_dateien.csv')
		return allDateien

	def clickAllReadyLinks(self):
		dateienListe = csv_handler.CsvHandler().read_csv('../data/parser_data/alle_dateien.csv', pythonVersion = '2')
		
		# Loop durch alle Laender (countryId steht jeweils an erster Stelle)
		for k in range(55,len(dateienListe)): #range(0,5): #range(5,10): #range(10,15): #len(dateienListe)):
			countryId = dateienListe[k][0]
			print('________________________________')
			print('countryId=' + countryId)
			landLinkPart = self.buchParserUrl + '?land=' + countryId
			
			# Loop durch alle Dateien, fuer welche jeweils Kadereintraege und Torschuetzen kompletiert werden muessen
			for i in range(1,len(dateienListe[k])):
				dateiId = dateienListe[k][i]
				print('dateiId=' + dateiId)
				dateiLinkPart = '&datei=' + dateiId
				kaderLink = landLinkPart + dateiLinkPart + '&bereich=kader&ready=1'
				toreLink = landLinkPart + dateiLinkPart + '&bereich=tore&ready=1'
				webContent = self.returnWebContent(kaderLink)
				webContent = self.returnWebContent(toreLink)
		return True


if __name__ == '__main__':
	#FabianParserModifier().writeAllDateiIdsForAllCountriesIntoCsv()
	FabianParserModifier().clickAllReadyLinks()
