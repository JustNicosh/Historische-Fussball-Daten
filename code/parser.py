#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import urllib2
import bs4
import csv_handler

class FabianParser():

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
			print 'Error: Could not open ' + url
			return {'failed': True}
	
	def writeAllDateiIdsForAllCountriesIntoCsv(self):
		# Loop durch alle Laender (bis inkl. Chile), Datei-Infos pro Land in Liste speichern
		for i in range(1, 62):

			# Bolivien rauslassen
			if (i == 59):
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

	def test(self):

		#dateienListe = csv_handler.CsvReaderForPython2('../data/parser_data/alle_dateien.csv').read_csv()
		dateienListe = csv_handler.CsvHandler().read_csv('../data/parser_data/alle_dateien.csv', pythonVersion = '2')

		print(dateienListe)
		


if __name__ == '__main__':
	FabianParser().test()