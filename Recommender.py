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

    def searchTVMovies(self, type, title, director, actor, genre):
        """Search shows based on type and various attributes."""
        if type not in ["Movie", "TV Show"]:
            return "No Results"
        results = []
        for show in self.__shows.values():
            if show.get_show_type() == type:
                if title and title.lower() not in show.get_title().lower():
                    continue
                if director and director.lower() not in show.get_director().lower():
                    continue
                if actor:
                    if not any(actor.lower() in cast_member.lower() for cast_member in show.get_cast().split(', ')):
                        continue
                if genre:
                    if not any(genre.lower().strip() in g.lower() for g in show.get_listed_in().split(',')):
                        continue
                results.append(show)
        if not results:
            return "No Results"
        return self.format_results(results)




        if not results:
            print("No matching results found.")
            return "No Results"
        return self.format_results(results)

    def format_results(self, results):
        output =""
        for show in results:
            output += f"Title: {show.get_title()}\n"
            output += f"Director: {show.get_director()}\n"
            output += f"Cast: {show.get_cast()}\n"
            output += f"Genre(s): {show.get_listed_in()}\n\n"
        return output

        header = f"{'Title':<{max_title_len}} {'Director':<{max_director_len}} {'Cast':<{max_cast_len}} {'Genre':<{max_genre_len}}"
        output = header + "\n" + "-" * len(header) + "\n"
        for show in results:
            output += f"{show.get_title():<{max_title_len}} {show.get_director():<{max_director_len}} {show.get_cast():<{max_cast_len}} {show.get_listed_in():<{max_genre_len}}\n"
        return output

    def searchBooks(self, title, authors, publisher):
        if not title and not authors and not publisher:
            messagebox.showerror("Error", "Please enter information for the Title, Author, and/or Publisher.")
            return "No Results"

        results = []
        for book in self.__books.values():
            matches_title = title.lower() in book.get_title().lower() if title else True
            matches_author = authors.lower() in book.get_authors().lower() if authors else True
            matches_publisher = publisher.lower() in book.get_publisher().lower() if publisher else True

            if matches_title and matches_author and matches_publisher:
                results.append(book)

        if not results:
            return "No Results"

        # Formatting results
        output = "Title\t\tAuthor\t\tPublisher\n"
        output += "\n".join(f"{book.get_title()}\t\t{book.get_authors()}\t\t{book.get_publisher()}" for book in results)
        return output

    def get_recommendations(self, media_type, title):
        # Load data (normally, you'd do this once, not every time a recommendation is sought)
        self.__shows['1'] = Show('1', 'The Great Adventure', '8.0', 'Movie', 'John Doe', 'John Actor', 'US', '2022-01-01',
                               '2022', 'PG-13', '120', 'Adventure, Comedy', 'An adventurous journey.')
        self.__books['101'] = Book('101', 'Adventures in Programming', '4.0', 'Charles Babbage', '1234567890',
                                 '987654321', 'en', '300', '100', '2019-01-01', 'Tech __books Publishing')
        self.__associations['1'] = ['101']
        self.__associations['101'] = ['1']

        # Check media type and fetch recommendations
        if media_type in ["Movie", "TV Show"]:
            for show_id, show in self.__shows.items():
                if  title.lower() in show.get_title().lower():
                    # Finding related __books
                    related_books = self.__associations.get(show_id, [])
                    details = [
                        f"Title: {self.__books[bid].get_title()}, Author: {self.__books[bid].get_authors()}, ISBN: {self.__books[bid].get_isbn()}"
                        for bid in related_books if bid in self.__books]
                    return "\n".join(details) if details else "No related __books found."
            return "No results found for the provided title."

        elif media_type == "Book":
            for book_id, book in self.__books.items():
                if book.get_title().lower() == title.lower():
                    # Finding related __shows
                    related_shows = self.__associations.get(book_id, [])
                    details = [
                        f"Title: {self.__shows[sid].get_title()}, Director: {self.__shows[sid].get_directors()}, Genres: {self.__shows[sid].get_genres()}"
                        for sid in related_shows if sid in self.__shows]
                    return "\n".join(details) if details else "No related __shows found."
            return "No results found for the provided title."

        return "Invalid media type provided."