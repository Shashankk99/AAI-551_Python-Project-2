import re
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import os
import matplotlib.pyplot
from Recommender import Recommender
from tkinter import messagebox
import matplotlib


class RecommenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Recommender System")
        self.root.geometry("1200x800")  # Window size
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.recommender = Recommender()

        # Initialize all tabs
        self.create_notebook_tab()
        self.create_tv_shows_tab()
        self.create_books_tab()
        self.create_search_media_tab()
        self.create_search_books_tab()
        self.setup_recommendations_tab()
        self.create_ratings_tab()
        self.notebook.pack(fill='both', expand=True)

        # Buttons frame at the bottom
        self.load_buttons_frame = tk.Frame(self.root)
        self.load_buttons_frame.pack(side="bottom", pady=10)

        # Initialize buttons for various operations
        self.init_buttons()

    def init_buttons(self):
        load_shows_button = tk.Button(self.load_buttons_frame, text="Load Shows", command=self.load_shows_based_on_tab)
        load_shows_button.grid(row=0, column=0, padx=5)

        load_books_button = tk.Button(self.load_buttons_frame, text="Load Books", command=self.load_books)
        load_books_button.grid(row=0, column=1, padx=5)

        load_recommendations_button = tk.Button(self.load_buttons_frame, text="Load Recommendations",
                                                command=self.load_recommendations)
        load_recommendations_button.grid(row=0, column=2, padx=5)

        quit_button = tk.Button(self.load_buttons_frame, text="Quit", command=self.root.quit)
        quit_button.grid(row=0, column=3, padx=5)

    def load_shows_based_on_tab(self):
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if current_tab == "Movies":
            self.load_movies()
        elif current_tab == "TV Shows":
            self.load_tv_shows()

    def create_notebook_tab(self):
        notebook_tab = ttk.Frame(self.notebook)
        self.notebook.add(notebook_tab, text="Movies")

        # Setup for movies tab with treeview and text widget for display
        self.movies_title_runtime_frame = tk.Frame(notebook_tab)
        self.movies_title_runtime_frame.pack(fill="both", expand=True)
        self.movies_tree_scroll = tk.Scrollbar(self.movies_title_runtime_frame)
        self.movies_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.movies_tree = ttk.Treeview(self.movies_title_runtime_frame, columns=("Title", "Runtime"), show="headings",
                                        yscrollcommand=self.movies_tree_scroll.set)
        self.movies_tree.heading("Title", text="Title")
        self.movies_tree.heading("Runtime", text="Runtime")
        self.movies_tree.pack(fill="both", expand=True)
        self.movies_tree_scroll.config(command=self.movies_tree.yview)
        self.movies_ratings_frame = tk.Frame(notebook_tab)
        self.movies_ratings_frame.pack(fill="both", expand=True)
        self.movies_ratings_text = tk.Text(self.movies_ratings_frame, wrap="word", height=10)
        self.movies_ratings_text.pack(fill="both", expand=True)

    def load_movies(self):
        filename = filedialog.askopenfilename(title="Select Movie File", filetypes=(("CSV files", "*.csv"),))
        if filename:
            self.recommender.loadShows(filename)
            self.movies_tree.delete(*self.movies_tree.get_children())
            self.movies_ratings_text.delete("1.0", tk.END)
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["type"] == "Movie":
                        title = row["title"]
                        runtime = row["duration"]
                        rating = row["average_rating"]
                        self.movies_tree.insert("", tk.END, values=(title, runtime))

            movie_stats = self.recommender.getMovieStats()
            # Display statistics and ratings in the text widget
            self.movies_ratings_text.insert(tk.END, "Ratings Breakdown:\n")
            for rating, percentage in movie_stats['Ratings'].items():
                self.movies_ratings_text.insert(tk.END, f"{rating}: {percentage}%\n")
            self.movies_ratings_text.insert(tk.END, "Movie Statistics:\n")
            self.movies_ratings_text.insert(tk.END,
                                            f"Average Movie Duration: {movie_stats['Average Movie Duration']} minutes\n")
            self.movies_ratings_text.insert(tk.END,
                                            f"Most Prolific Director: {movie_stats['Most Prolific Director']}\n")
            self.movies_ratings_text.insert(tk.END, f"Most Prolific Actor: {movie_stats['Most Prolific Actor']}\n")
            self.movies_ratings_text.insert(tk.END, f"Most Frequent Genre: {movie_stats['Most Frequent Genre']}\n")
            self.create_movie_ratings_pie_chart()

    def create_tv_shows_tab(self):
        tv_shows_tab = ttk.Frame(self.notebook)
        self.notebook.add(tv_shows_tab, text="TV Shows")

        # Setup for TV shows tab with treeview and text widget for display
        self.tv_shows_title_runtime_frame = tk.Frame(tv_shows_tab)
        self.tv_shows_title_runtime_frame.pack(fill="both", expand=True)
        self.tv_shows_tree_scroll = tk.Scrollbar(self.tv_shows_title_runtime_frame)
        self.tv_shows_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tv_shows_tree = ttk.Treeview(self.tv_shows_title_runtime_frame, columns=("Title", "Seasons"),
                                          show="headings", yscrollcommand=self.tv_shows_tree_scroll.set)
        self.tv_shows_tree.heading("Title", text="Title")
        self.tv_shows_tree.heading("Seasons", text="Seasons")
        self.tv_shows_tree.pack(fill="both", expand=True)
        self.tv_shows_tree_scroll.config(command=self.tv_shows_tree.yview)
        self.tv_shows_ratings_frame = tk.Frame(tv_shows_tab)
        self.tv_shows_ratings_frame.pack(fill="both", expand=True)
        self.tv_shows_ratings_text = tk.Text(self.tv_shows_ratings_frame, wrap="word", height=10)
        self.tv_shows_ratings_text.pack(fill="both", expand=True)

    def load_tv_shows(self):
        filename = filedialog.askopenfilename(title="Select TV Show File", filetypes=(("CSV files", "*.csv"),))
        if filename:
            show_info = self.recommender.loadShows(filename)  # Load the shows
            self.tv_shows_tree.delete(*self.tv_shows_tree.get_children())  # Clear previous TV show entries
            self.tv_shows_ratings_text.delete("1.0", tk.END)  # Clear previous ratings text

            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["type"] == "TV Show":
                        title = row["title"]
                        seasons = row["duration"]  # Assuming 'seasons' is represented by the 'duration' column
                        self.tv_shows_tree.insert("", tk.END, values=(title, seasons))

            # Calculate TV show statistics and display
            tv_stats = self.recommender.getTVStats()
            self.tv_shows_ratings_text.insert(tk.END, "\nTV Show Statistics:\n")
            self.tv_shows_ratings_text.insert(tk.END, "Ratings Breakdown:\n")
            for rating, percentage in tv_stats['Rating Counts'].items():
                self.tv_shows_ratings_text.insert(tk.END, f"{rating}: {percentage}%\n")
            self.tv_shows_ratings_text.insert(tk.END, f"Average Seasons per Show: {tv_stats['Average Seasons']}\n")
            self.tv_shows_ratings_text.insert(tk.END, f"Most Common Actor: {tv_stats['Most Common Actor']}\n")
            self.tv_shows_ratings_text.insert(tk.END, f"Most Common Genre: {tv_stats['Most Common Genre']}\n")
            self.create_tv_ratings_pie_chart()

    def create_books_tab(self):
        books_tab = ttk.Frame(self.notebook)
        self.notebook.add(books_tab, text="Books")

        # Setup for books tab with treeview and text widget for statistics
        self.books_title_details_frame = tk.Frame(books_tab)
        self.books_title_details_frame.pack(fill="both", expand=True)
        self.books_tree_scroll = tk.Scrollbar(self.books_title_details_frame)
        self.books_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_tree = ttk.Treeview(self.books_title_details_frame, columns=("Title", "Author", "Publisher"),
                                       show="headings", yscrollcommand=self.books_tree_scroll.set)
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Publisher", text="Publisher")
        self.books_tree.pack(fill="both", expand=True)
        self.books_tree_scroll.config(command=self.books_tree.yview)
        self.books_stats_frame = tk.Frame(books_tab)
        self.books_stats_frame.pack(fill="both", expand=True)
        self.books_stats_text = tk.Text(self.books_stats_frame, wrap="word", height=10)
        self.books_stats_text.pack(fill="both", expand=True)
        self.books_stats_text.insert(tk.END, "Load book data to view statistics.")
        self.books_stats_text.config(state=tk.DISABLED)

    def load_books(self):
        filename = filedialog.askopenfilename(title="Select Book File", filetypes=(("CSV files", "*.csv"),))
        if filename:
            file = os.path.basename(filename)
            num = file[5:]

            association_file = os.path.dirname(filename)

            self.recommender.loadAssociations(association_file + '/associated' + num)
            self.books_tree.delete(*self.books_tree.get_children())
            self.books_stats_text.config(state=tk.NORMAL)
            self.books_stats_text.delete('1.0', tk.END)

            # Load books and display statistics
            self.recommender.loadBooks(filename)
            book_list = self.recommender.getBookList()
            for book in book_list:
                self.books_tree.insert("", tk.END, values=(book.get_title(), book.get_authors(), book.get_publisher()))

            book_stats = self.recommender.getBookStats()
            self.books_stats_text.insert(tk.END, str(book_stats))
            self.books_stats_text.config(state=tk.DISABLED)

    def create_search_media_tab(self):
        search_media_tab = ttk.Frame(self.notebook)
        self.notebook.add(search_media_tab, text="Search Movies/TV")

        # Entry widgets and labels for user inputs in the search media tab
        tk.Label(search_media_tab, text="Type:").grid(row=0, column=0, padx=10, pady=10)
        self.media_type_combobox_search = ttk.Combobox(search_media_tab, values=["Movie", "TV Show"], state="readonly")
        self.media_type_combobox_search.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(search_media_tab, text="Title:").grid(row=1, column=0, padx=10, pady=10)
        self.title_entry_search = tk.Entry(search_media_tab)
        self.title_entry_search.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(search_media_tab, text="Director:").grid(row=2, column=0, padx=10, pady=10)
        self.director_entry_search = tk.Entry(search_media_tab)
        self.director_entry_search.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(search_media_tab, text="Actor:").grid(row=3, column=0, padx=10, pady=10)
        self.actor_entry_search = tk.Entry(search_media_tab)
        self.actor_entry_search.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(search_media_tab, text="Genre:").grid(row=4, column=0, padx=10, pady=10)
        self.genre_entry_search = tk.Entry(search_media_tab)
        self.genre_entry_search.grid(row=4, column=1, padx=10, pady=10)

        # Button to trigger the search
        search_button = tk.Button(search_media_tab, text="Search", command=self.searchShows)
        search_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Text area for displaying search results
        self.search_results_text = tk.Text(search_media_tab, wrap="word", height=10)
        self.search_results_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        search_media_tab.grid_rowconfigure(6, weight=1)  # Dynamic expansion for text area
        search_media_tab.grid_columnconfigure(1, weight=1)

        # Add scrollbars
        search_scroll = tk.Scrollbar(search_media_tab, command=self.search_results_text.yview)
        search_scroll.grid(row=6, column=2, sticky='nsew')
        self.search_results_text.config(yscrollcommand=search_scroll.set)
        self.search_results_text.insert(tk.END, "Enter search parameters and click 'Search'.")
        self.search_results_text.config(state=tk.DISABLED)

    def searchShows(self):
        # Process search queries and display results for movies and TV shows
        type_ = self.media_type_combobox_search.get()
        title = self.title_entry_search.get()
        director = self.director_entry_search.get()
        actor = self.actor_entry_search.get()
        genre = self.genre_entry_search.get()

        if type_ not in ["Movie", "TV Show", "Books"]:
            messagebox.showerror("Error", "Please select 'Movie' or 'TV Show' from the Type dropdown.")
            return

        if not (title or director or actor or genre):
            messagebox.showerror("Error", "Please enter at least one search criterion.")
            return

        results = self.recommender.searchTVMovies(type_, title, director, actor, genre)
        self.search_results_text.config(state=tk.NORMAL)
        self.search_results_text.delete('1.0', tk.END)
        if results == "No Results":
            self.search_results_text.insert(tk.END, "No Results found based on the search criteria.")
        else:
            self.search_results_text.insert(tk.END, results)
        self.search_results_text.config(state=tk.DISABLED)

    def searchBooks(self):
        # Process search queries and display results for books
        type_ = self.book_type_combobox_search.get()
        title = self.title_entry_search_books.get()
        authors = self.authors_entry_search_books.get()
        publisher = self.publisher_entry_search_books.get()

        if type_ not in ["Book"]:
            messagebox.showerror("Error", "Please select 'Book' from the Type dropdown.")
            return

        if not (title or authors or publisher):
            messagebox.showerror("Error", "Please enter at least one search criterion.")
            return

        results = self.recommender.searchBooks(title, authors, publisher)
        self.search_results_text_books.config(state=tk.NORMAL)
        self.search_results_text_books.delete('1.0', tk.END)
        if results == "No Results":
            self.search_results_text_books.insert(tk.END, "No Results found based on the search criteria.")
        else:
            self.search_results_text_books.insert(tk.END, results)
        self.search_results_text_books.config(state=tk.DISABLED)

    def create_search_books_tab(self):
        # Setup for the search books tab
        search_books_tab = ttk.Frame(self.notebook)
        self.notebook.add(search_books_tab, text="Search Books")

        tk.Label(search_books_tab, text="Type:").grid(row=0, column=0, padx=10, pady=10)
        self.book_type_combobox_search = ttk.Combobox(search_books_tab, values=["Book"], state="readonly")
        self.book_type_combobox_search.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(search_books_tab, text="title:").grid(row=1, column=0, padx=10, pady=10)
        self.title_entry_search_books = tk.Entry(search_books_tab)
        self.title_entry_search_books.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(search_books_tab, text="Authors:").grid(row=2, column=0, padx=10, pady=10)
        self.authors_entry_search_books = tk.Entry(search_books_tab)
        self.authors_entry_search_books.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(search_books_tab, text="Publisher:").grid(row=3, column=0, padx=10, pady=10)
        self.publisher_entry_search_books = tk.Entry(search_books_tab)
        self.publisher_entry_search_books.grid(row=3, column=1, padx=10, pady=10)

        search_button = tk.Button(search_books_tab, text="Search", command=self.searchBooks)
        search_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.search_results_text_books = tk.Text(search_books_tab, wrap="word", height=10)
        self.search_results_text_books.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        search_books_tab.grid_rowconfigure(6, weight=1)  # Dynamic expansion for text area
        search_books_tab.grid_columnconfigure(1, weight=1)

        search_scroll = tk.Scrollbar(search_books_tab, command=self.search_results_text_books.yview)
        search_scroll.grid(row=4, column=2, sticky='nsew')
        self.search_results_text_books.config(yscrollcommand=search_scroll.set)
        self.search_results_text_books.insert(tk.END, "Enter search parameters and click 'Search'.")
        self.search_results_text_books.config(state=tk.DISABLED)

    def setup_recommendations_tab(self):
        # Setup for the recommendations tab
        rec_tab = ttk.Frame(self.notebook)
        self.notebook.add(rec_tab, text="Recommendations")

        tk.Label(rec_tab, text="Type:").grid(row=0, column=0, padx=10, pady=10)
        self.media_type_combobox = ttk.Combobox(rec_tab, values=["Movie", "TV Show", "Book"], state="readonly")
        self.media_type_combobox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(rec_tab, text="Title:").grid(row=1, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(rec_tab)
        self.title_entry.grid(row=1, column=1, padx=10, pady=10)

        load_rec_button = tk.Button(rec_tab, text="Load Recommendations", command=self.get_recommendations)
        load_rec_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.results_text = tk.Text(rec_tab, wrap="word", height=10)
        self.results_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        rec_tab.grid_rowconfigure(3, weight=1)  # Dynamic expansion for text area
        rec_tab.grid_columnconfigure(1, weight=1)
        self.results_text.insert(tk.END, "Enter a title and select a type to get recommendations.")
        self.results_text.config(state=tk.DISABLED)

    def load_recommendations(self):
        filedialog.askopenfilename(title="Select Book File", filetypes=(("CSV files", "*.csv"),))

    def get_recommendations(self):
        # Get recommendations based on user inputs
        type_ = self.media_type_combobox.get()
        title = self.title_entry.get()
        results = self.recommender.get_recommendations(type_, title)

        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        if results == "No Results":
            self.results_text.insert(tk.END, "No Results found based on the search criteria.")
        else:
            self.results_text.insert(tk.END, results)
        self.results_text.config(state=tk.DISABLED)

    def create_ratings_tab(self):
        # Setup for the ratings tab with canvas for pie charts
        ratings_tab = ttk.Frame(self.notebook)
        self.notebook.add(ratings_tab, text="Ratings")

        self.movie_ratings_canvas = tk.Canvas(ratings_tab, width=600, height=600)
        self.movie_ratings_canvas.grid(row=0, column=0, padx=0, pady=0)

        self.tv_ratings_canvas = tk.Canvas(ratings_tab, width=600, height=600)
        self.tv_ratings_canvas.grid(row=0, column=1, padx=0, pady=0)

    def create_movie_ratings_pie_chart(self):
        # Create and display a pie chart for movie ratings
        movie_stats = self.recommender.getMovieStats()
        if "Ratings" in movie_stats:
            ratings = movie_stats["Ratings"]
            labels = [f"{rating} ({value:.2f}%)" for rating, value in ratings.items()]
            values = list(ratings.values())

        self.movie_ratings_canvas.delete("all")
        pie = matplotlib.pyplot.pie(values, labels=labels, autopct='%1.1f%%')
        matplotlib.pyplot.axis('equal')
        matplotlib.pyplot.savefig("movie_ratings.png")
        movie_ratings_image = tk.PhotoImage(file="movie_ratings.png")
        self.movie_ratings_canvas.create_image(0, 0, anchor=tk.NW, image=movie_ratings_image)
        self.movie_ratings_canvas.image = movie_ratings_image

    def create_tv_ratings_pie_chart(self):
        # Create and display a pie chart for TV show ratings
        tv_stats = self.recommender.getTVStats()
        if "Rating Counts" in tv_stats:
            ratings = tv_stats["Rating Counts"]
        labels = [f"{rating} ({value:.2f}%)" for rating, value in ratings.items()]
        values = list(ratings.values())

        self.tv_ratings_canvas.delete("all")
        pie = matplotlib.pyplot.pie(values, labels=labels, autopct='%1.1f%%')
        matplotlib.pyplot.axis('equal')
        matplotlib.pyplot.savefig("tv_ratings.png")
        tv_ratings_image = tk.PhotoImage(file="tv_ratings.png")
        self.tv_ratings_canvas.create_image(0, 0, anchor=tk.NW, image=tv_ratings_image)
        self.tv_ratings_canvas.image = tv_ratings_image

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = RecommenderGUI(root)
    app.run()


if __name__ == "__main__":
    main()
