class Media:
    def __init__(self, ID, title, average_rating):
        self.__ID = ID
        self.__title = title
        self.__average_rating = average_rating

    def get_ID(self):
        return self.__ID

    def get_title(self):
        return self.__title

    def get_average_rating(self):
        return self.__average_rating

    def set_ID(self, ID):
        self.__ID = ID

    def set_title(self, title):
        self.__title = title

    def set_average_rating(self, average_rating):
        self.__average_rating = average_rating
