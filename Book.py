# Book.py

class Book:
    def __init__(self, bookID, title, average_rating, authors, isbn, isbn13, language_code, num_pages, ratings_count, publication_date, publisher):
        self.__bookID = bookID
        self.__title = title
        self.__average_rating = average_rating
        self.__authors = authors
        self.__isbn = isbn
        self.__isbn13 = isbn13
        self.__language_code = language_code
        self.__num_pages = num_pages
        self.__ratings_count = ratings_count
        self.__publication_date = publication_date
        self.__publisher = publisher
