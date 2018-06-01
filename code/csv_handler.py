#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

import csv

class CsvHandler():
    """Handles csv-module interaction.
    """

    def read_csv(self, path, configFormat = 'rb', configEncoding = 'utf-8', configDelimiter = ',', configQuotechar = '|', pythonVersion = '3'):
        """Returns the content of a csv document.
        """
        csvFile = open(path, configFormat, encoding = configEncoding)
        reader = csv.reader(csvFile, delimiter = configDelimiter, quotechar = configQuotechar)

        outputList = []
        for row in reader:
            if len(row) > 0:
                outputList.append(row)
        csvFile.close()
        return outputList

    def create_csv(self, content, path, configDelimiter = ','):
        """Creates a new csv document.
        """
        inputList = content
        csvFile = open(path, 'a')
        writer = csv.writer(csvFile, delimiter = configDelimiter)

        for item in inputList:
            if type(item) == list:
                writer.writerow(item)
            else:
                writer.writerow([item])
        csvFile.close()
        return csvFile
