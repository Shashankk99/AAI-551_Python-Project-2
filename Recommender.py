import csv
from tkinter import messagebox
from Book import Book
from Show import Show
import re

class Recommender:
    def __init__(self):
        self.__books = {}
        self.__shows = {}
        self.__associations = {}

    def loadBooks(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(row['bookID'], row['title'], float(row['average_rating']), row['authors'], row['isbn'],
                            row['isbn13'], row['language_code'], int(row['num_pages']), int(row['ratings_count']),
                            row['publication_date'], row['publisher'])
                self.__books[row['bookID']] = book

    def loadShows(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dur = re.findall(r'\b\d+\b', row['duration'])
                show = Show(row['show_id'], row['title'], float(row['average_rating']), row['type'], row['director'],
                            row['cast'], row['country'], row['date_added'], int(row['release_year']), row['rating'],
                            dur[0], row['listed_in'], row['description'])
                self.__shows[row['show_id']] = show

    def loadAssociations(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                id1, id2 = row[0], row[1]
                if id1 not in self.__associations:
                    self.__associations[id1] = {}
                if id2 not in self.__associations[id1]:
                    self.__associations[id1][id2] = 1
                else:
                    self.__associations[id1][id2] += 1

                if id2 not in self.__associations:
                    self.__associations[id2] = {}
                if id1 not in self.__associations[id2]:
                    self.__associations[id2][id1] = 1
                else:
                    self.__associations[id2][id1] += 1

    def getMovieList(self):
        movie_list = []
        for show_id, show in self.__shows.items():
            if hasattr(show, 'type') and show.get_show_type() == "Movie":
                movie_list.append(show)
        return movie_list

    def getTVList(self):
        tv_list = []
        for show_id, show in self.__shows.items():
            if hasattr(show, 'type') and show.get_show_type() == "TV Show":
                tv_list.append(show)
        return tv_list

    def getBookList(self):
        return list(self.__books.values())

    def getMovieStats(self):
        if not self.__shows:
            return "No movie data available."

        ratings_count = {"R": 0, "ALL": 0, "18+": 0, "7+": 0, "13+": 0, "16+": 0, "None": 0, "NR": 0, "PG-13": 0,
                         "G": 0}
        total_duration = 0
        directors_count = {}
        actors_count = {}
        genres_count = {}

        for show_id, show in self.__shows.items():
            if hasattr(show, 'type') and show.get_show_type() == "Movie":
                # Rating count
                rating = show.get_rating()
                if rating in ratings_count:
                    ratings_count[rating] += 1
                else:
                    ratings_count[rating] = 1

                # Duration
                total_duration += int(show.get_duration())

                # Directors count
                director = show.get_director()
                if director in directors_count:
                    directors_count[director] += 1
                else:
                    directors_count[director] = 1

                # Actors count
                actors = show.get_cast().split(', ')
                for actor in actors:
                    if actor in actors_count:
                        actors_count[actor] += 1
                    else:
                        actors_count[actor] = 1

                # Genres count
                genres = show.get_listed_in().split(', ')
                for genre in genres:
                    if genre in genres_count:
                        genres_count[genre] += 1
                    else:
                        genres_count[genre] = 1

        num_movies = sum(ratings_count.values())
        avg_duration = total_duration / num_movies if num_movies > 0 else 0

        most_common_director = max(directors_count, key=directors_count.get)
        most_common_actor = max(actors_count, key=actors_count.get)
        most_common_genre = max(genres_count, key=genres_count.get)

        # Convert rating counts to percentages
        rating_percentages = {rating: round(count / num_movies * 100, 2) for rating, count in ratings_count.items()}

        return {
            "Ratings": rating_percentages,
            "Average Movie Duration": round(avg_duration, 2),
            "Most Prolific Director": most_common_director,
            "Most Prolific Actor": most_common_actor,
            "Most Frequent Genre": most_common_genre
        }


    def getTVStats(self):
        if not self.__shows:
            return "No TV show data available."

        ratings_count = {}
        total_seasons = 0
        actors_count = {}
        genres_count = {}

        for show_id, show in self.__shows.items():
            if hasattr(show, 'type') and show.get_show_type() == "TV Show":
                # Rating count
                rating = show.get_rating()
                if rating in ratings_count:
                    ratings_count[rating] += 1
                else:
                    ratings_count[rating] = 1

                # Total seasons
                total_seasons += int(show.get_seasons())

                # Actors count
                actors = show.get_cast().split(', ')
                for actor in actors:
                    if actor in actors_count:
                        actors_count[actor] += 1
                    else:
                        actors_count[actor] = 1

                # Genres count
                genres = show.get_listed_in().split(', ')
                for genre in genres:
                    if genre in genres_count:
                        genres_count[genre] += 1
                    else:
                        genres_count[genre] = 1

        num_shows = sum(ratings_count.values())
        avg_seasons = total_seasons / num_shows if num_shows > 0 else 0

        most_common_actor = max(actors_count, key=actors_count.get)
        most_common_genre = max(genres_count, key=genres_count.get)

        return {
            "Rating Counts": {rating: round(count / num_shows * 100, 2) for rating, count in ratings_count.items()},
            "Average Seasons": round(avg_seasons, 2),
            "Most Common Actor": most_common_actor,
            "Most Common Genre": most_common_genre
        }

    def getBookStats(self):
        if not self.__books:
            return "No book data available."

        total_pages = 0
        authors_count = {}
        publishers_count = {}

        # Iterate over each book in the dictionary
        for book in self.__books.values():
            # Accumulate total pages
            total_pages += book.get_num_pages()

            # Count occurrences of each author
            authors = book.get_authors().split(', ')
            for author in authors:
                if author:
                    authors_count[author] = authors_count.get(author, 0) + 1

            # Count occurrences of each publisher
            publisher = book.get_publisher()
            if publisher:
                publishers_count[publisher] = publishers_count.get(publisher, 0) + 1

        num_books = len(self.__books)
        if num_books == 0:
            return "No book data available."

        avg_pages = total_pages / num_books

        # Determine the most common author and publisher
        most_common_author = max(authors_count, key=authors_count.get, default="No data")
        most_common_publisher = max(publishers_count, key=publishers_count.get, default="No data")

        return {
            "Average Page Count": round(avg_pages, 2),
            "Most Prolific Author": most_common_author,
            "Top Publisher": most_common_publisher
        }
