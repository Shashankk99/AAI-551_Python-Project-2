import csv

class Recommender:
    def __init__(self):
        self.__books = {}
        self.__shows = {}
        self.__associations = {}

    def loadBooks(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(row['bookID'], row['title'], float(row['average_rating']), row['authors'], row['isbn'], row['isbn13'], row['language_code'], int(row['num_pages']), int(row['ratings_count']), row['publication_date'], row['publisher'])
                self.__books[row['bookID']] = book

    def loadShows(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                show = Show(row['show_id'], row['title'], float(row['average_rating']), row['type'], row['director'], row['cast'], row['country'], row['date_added'], int(row['release_year']), row['rating'], row['duration'], row['listed_in'], row['description'])
                self.__shows[row['show_id']] = show
