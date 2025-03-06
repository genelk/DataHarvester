import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class TrendDetector:
    """
    Analyzes movie data to detect trends in ratings, popularity, and genres over time
    """
    
    def __init__(self):
        """Initialize the trend detector"""
        self.trends = {}
    
    def detect_rating_trends(self, movies_df):
        """
        Detect trends in movie ratings over time
        
        Args:
            movies_df: DataFrame containing movie data
            
        Returns:
            DataFrame with rating trends by year
        """
        # Group data by year and calculate average ratings
        rating_trends = movies_df.groupby('release_year')['vote_average'].agg([
            'mean', 'median', 'std', 'count'
        ]).reset_index()
        
        # Calculate rolling averages for smoothing
        if len(rating_trends) > 3:
            rating_trends['rolling_avg'] = rating_trends['mean'].rolling(window=3, min_periods=1).mean()
        else:
            rating_trends['rolling_avg'] = rating_trends['mean']
        
        # Detect years with significant changes
        rating_trends['yearly_change'] = rating_trends['mean'].pct_change() * 100
        
        # Store results
        self.trends['ratings'] = rating_trends
        
        return rating_trends
    
    def detect_genre_trends(self, movies_df):
        """
        Detect trends in movie genres over time
        
        Args:
            movies_df: DataFrame containing movie data
            
        Returns:
            DataFrame with genre popularity by year
        """
        # Create a list of all years
        years = sorted(movies_df['release_year'].unique())
        
        # Extract all unique genres
        all_genres = set()
        for genres in movies_df['genre_list']:
            if isinstance(genres, list):
                all_genres.update(genres)
        
        # Count genres by year
        genre_counts = {}
        
        for year in years:
            year_movies = movies_df[movies_df['release_year'] == year]
            year_total = len(year_movies)
            
            genre_counts[year] = {}
            
            for genre in all_genres:
                # Count movies with this genre in this year
                count = sum(1 for genres in year_movies['genre_list'] 
                            if isinstance(genres, list) and genre in genres)
                
                # Calculate percentage
                percentage = (count / year_total * 100) if year_total > 0 else 0
                genre_counts[year][genre] = percentage
        
        # Convert to DataFrame
        genre_trends = pd.DataFrame(genre_counts).T
        genre_trends.index.name = 'release_year'
        genre_trends = genre_trends.reset_index()
        
        # Store results
        self.trends['genres'] = genre_trends
        
        return genre_trends
    
    def detect_popularity_trends(self, movies_df):
        """
        Detect trends in movie popularity over time
        
        Args:
            movies_df: DataFrame containing movie data
            
        Returns:
            DataFrame with popularity trends by year
        """
        # Group data by year and calculate average popularity
        popularity_trends = movies_df.groupby('release_year')['popularity'].agg([
            'mean', 'median', 'max', 'count'
        ]).reset_index()
        
        # Calculate yearly changes
        popularity_trends['yearly_change'] = popularity_trends['mean'].pct_change() * 100
        
        # Store results
        self.trends['popularity'] = popularity_trends
        
        return popularity_trends
    
    def visualize_trends(self, output_dir='visualizations'):
        """
        Create visualizations of detected trends
        
        Args:
            output_dir: Directory to save visualizations
        """
        # Ensure output directory exists
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("darkgrid")
        plt.rcParams["figure.figsize"] = (12, 8)
        
        # Visualize rating trends
        if 'ratings' in self.trends:
            plt.figure(figsize=(12, 6))
            rating_data = self.trends['ratings']
            
            plt.plot(rating_data['release_year'], rating_data['rolling_avg'], 
                     marker='o', linewidth=2, label='3-Year Rolling Average')
            plt.title("Average Movie Ratings by Year", fontsize=16)
            plt.xlabel("Release Year", fontsize=12)
            plt.ylabel("Average Rating", fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Save plot
            plt.savefig(f"{output_dir}/rating_trends.png")
            plt.close()
        
        # Visualize genre trends
        if 'genres' in self.trends:
            plt.figure(figsize=(14, 8))
            genre_data = self.trends['genres']
            
            # Select top 5 genres by average percentage
            top_genres = genre_data.drop('release_year', axis=1).mean().nlargest(5).index
            
            for genre in top_genres:
                plt.plot(genre_data['release_year'], genre_data[genre], 
                         marker='o', linewidth=2, label=genre)
            
            plt.title("Top Genre Trends Over Time", fontsize=16)
            plt.xlabel("Release Year", fontsize=12)
            plt.ylabel("Percentage of Movies (%)", fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save plot
            plt.savefig(f"{output_dir}/genre_trends.png")
            plt.close()
        
        # Visualize popularity trends
        if 'popularity' in self.trends:
            plt.figure(figsize=(12, 6))
            pop_data = self.trends['popularity']
            
            plt.bar(pop_data['release_year'], pop_data['mean'], alpha=0.7)
            plt.title("Average Movie Popularity by Year", fontsize=16)
            plt.xlabel("Release Year", fontsize=12)
            plt.ylabel("Average Popularity", fontsize=12)
            plt.grid(axis='y', alpha=0.3)
            
            # Save plot
            plt.savefig(f"{output_dir}/popularity_trends.png")
            plt.close()