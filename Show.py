from Media import Media

class Show(Media):
    def __init__(self, ID, title, average_rating, show_type, directors, actors, country_code, date_added, release_year, rating, duration, genres, description):
        super().__init__(ID, title, average_rating)
        self.__show_type = show_type
        self.__directors = directors
        self.__actors = actors
        self.__country_code = country_code
        self.__date_added = date_added
        self.__release_year = release_year
        self.__rating = rating
        self.__duration = duration
        self.__genres = genres
        self.__description = description

    def get_show_type(self):
        return self.__show_type

    def get_directors(self):
        return self.__directors

    def get_actors(self):
        return self.__actors

    def get_country_code(self):
        return self.__country_code

    def get_date_added(self):
        return self.__date_added

    def get_release_year(self):
        return self.__release_year

    def get_rating(self):
        return self.__rating

    def get_duration(self):
        return self.__duration

    def get_genres(self):
        return self.__genres

    def get_description(self):
        return self.__description

    def set_show_type(self, show_type):
        self.__show_type = show_type

    def set_directors(self, directors):
        self.__directors = directors

    def set_actors(self, actors):
        self.__actors = actors

    def set_country_code(self, country_code):
        self.__country_code = country_code

    def set_date_added(self, date_added):
        self.__date_added = date_added

    def set_release_year(self, release_year):
        self.__release_year = release_year

    def set_rating(self, rating):
        self.__rating = rating

    def set_duration(self, duration):
        self.__duration = duration

    def set_genres(self, genres):
        self.__genres = genres

    def set_description(self, description):
        self.__description = description
