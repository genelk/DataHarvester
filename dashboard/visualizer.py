import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from storage.db_connector import DatabaseConnector

class MovieDashboard:
    """
    Creates visualizations for movie data
    """
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize the dashboard
        
        Args:
            db_connector: Database connector
        """
        self.db = db_connector
        
        # Create output directory if it doesn't exist
        os.makedirs("visualizations", exist_ok=True)
        
        # Set style
        sns.set_style("darkgrid")
        plt.rcParams["figure.figsize"] = (12, 8)
    
    def generate_visualizations(self):
        """
        Generate all visualizations
        """
        self.plot_movies_by_year()
        self.plot_top_rated_movies()
        self.plot_language_distribution()
        self.plot_vote_vs_popularity()
        
        print("Visualizations saved to 'visualizations' directory")
    
    def plot_movies_by_year(self):
        """
        Plot number of movies by release year
        """
        # Get data
        movies_by_year = self.db.get_movies_by_year()
        
        # Create plot
        plt.figure(figsize=(12, 6))
        sns.barplot(x="release_year", y="movie_count", data=movies_by_year)
        plt.title("Number of Movies by Release Year")
        plt.xlabel("Release Year")
        plt.ylabel("Number of Movies")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot
        plt.savefig("visualizations/movies_by_year.png")
        plt.close()
    
    def plot_top_rated_movies(self):
        """
        Plot top rated movies
        """
        # Get data
        top_movies = self.db.get_top_rated_movies(10)
        
        # Create plot
        plt.figure(figsize=(12, 6))
        sns.barplot(x="weighted_rating", y="title", data=top_movies)
        plt.title("Top 10 Movies by Weighted Rating")
        plt.xlabel("Weighted Rating")
        plt.ylabel("Movie Title")
        plt.tight_layout()
        
        # Save plot
        plt.savefig("visualizations/top_rated_movies.png")
        plt.close()
    
    def plot_language_distribution(self):
        """
        Plot distribution of original languages
        """
        # Get data
        movies = self.db.get_movies()
        language_counts = movies["original_language"].value_counts()
        
        # Group languages with few occurrences
        threshold = 3
        other_languages = language_counts[language_counts < threshold].sum()
        main_languages = language_counts[language_counts >= threshold]
        
        # Add "Other" category
        if other_languages > 0:
            main_languages["Other"] = other_languages
        
        # Create plot
        plt.figure(figsize=(10, 10))
        plt.pie(main_languages, labels=main_languages.index, autopct="%1.1f%%", 
                shadow=True, startangle=90)
        plt.axis("equal")
        plt.title("Distribution of Original Languages")
        
        # Save plot
        plt.savefig("visualizations/language_distribution.png")
        plt.close()
    
    def plot_vote_vs_popularity(self):
        """
        Plot vote average vs popularity
        """
        # Get data
        movies = self.db.get_movies()
        
        # Create plot
        plt.figure(figsize=(10, 8))
        sns.scatterplot(x="popularity", y="vote_average", 
                        size="vote_count", sizes=(20, 500),
                        alpha=0.7, data=movies)
        plt.title("Vote Average vs Popularity")
        plt.xlabel("Popularity")
        plt.ylabel("Vote Average")
        
        # Save plot
        plt.savefig("visualizations/vote_vs_popularity.png")
        plt.close()
