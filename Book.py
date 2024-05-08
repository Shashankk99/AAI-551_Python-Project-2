from Media import Media

class Book(Media):
    def __init__(self, ID, title, average_rating, authors, isbn, isbn13, language_code, num_pages, ratings_count, publication_date, publisher):
        super().__init__(ID, title, average_rating)
        self.__authors = authors
        self.__isbn = isbn
        self.__isbn13 = isbn13
        self.__language_code = language_code
        self.__num_pages = num_pages
        self.__ratings_count = ratings_count
        self.__publication_date = publication_date
        self.__publisher = publisher

    def get_authors(self):
        return self.__authors

    def get_isbn(self):
        return self.__isbn

    def get_isbn13(self):
        return self.__isbn13

    def get_language_code(self):
        return self.__language_code

    def get_num_pages(self):
        return self.__num_pages

    def get_ratings_count(self):
        return self.__ratings_count

    def get_publication_date(self):
        return self.__publication_date

    def get_publisher(self):
        return self.__publisher

    def set_authors(self, authors):
        self.__authors = authors

    def set_isbn(self, isbn):
        self.__isbn = isbn

    def set_isbn13(self, isbn13):
        self.__isbn13 = isbn13

    def set_language_code(self, language_code):
        self.__language_code = language_code

    def set_num_pages(self, num_pages):
        self.__num_pages = num_pages

    def set_ratings_count(self, ratings_count):
        self.__ratings_count = ratings_count

    def set_publication_date(self, publication_date):
        self.__publication_date = publication_date

    def set_publisher(self, publisher):
        self.__publisher = publisher
