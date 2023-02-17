import csv


class GoodreadsCsvParser:
    reader = None

    def __init__(self):
        f = open("goodreads_library_export.csv", "r", encoding="cp1252")
        self.reader = csv.reader(f)
        f.close()

    def printrows(self):

        for row in self.reader:
            print(row)
