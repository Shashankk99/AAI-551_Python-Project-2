from Media import Media


class Show(Media):
    def __init__(self, ID, title, average_rating, show_type, directors, actors, country_code, date_added, release_year,
                 rating, duration, genres, description):
        super().__init__(ID, title, average_rating)
        self.type = show_type
        self.directors = directors
        self.actors = actors
        self.country_code = country_code
        self.date_added = date_added
        self.release_year = release_year
        self.rating = rating
        self.duration = duration
        self.seasons = duration
        self.genres = genres
        self.description = description

    def get_show_type(self):
        return self.type

    def get_director(self):
        return self.directors

    def get_cast(self):
        return self.actors

    def get_country_code(self):
        return self.country_code

    def get_date_added(self):
        return self.date_added

    def get_release_year(self):
        return self.release_year

    def get_rating(self):
        return self.rating

    def get_duration(self):
        return self.duration

    def get_seasons(self):
        return self.duration

    def get_listed_in(self):
        return self.genres

    def get_description(self):
        return self.description

    def set_show_type(self, show_type):
        self.type = show_type

    def set_director(self, directors):
        self.directors = directors

    def set_cast(self, actors):
        self.actors = actors

    def set_country_code(self, country_code):
        self.country_code = country_code

    def set_date_added(self, date_added):
        self.date_added = date_added

    def set_release_year(self, release_year):
        self.release_year = release_year

    def set_rating(self, rating):
        self.rating = rating

    def set_duration(self, duration):
        self.duration = duration

    def set_seasons(self, duration):
        self.seasons = duration

    def set_listed_in(self, genres):
        self.genres = genres

    def set_description(self, description):
        self.description = description
