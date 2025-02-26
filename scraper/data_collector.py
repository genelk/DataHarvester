from typing import List, Dict, Any
import time
from tqdm import tqdm
from scraper.tmdb_api import TMDBApi

class MovieDataCollector:
    """
    Collects movie data from TMDB API
    """
    
    def __init__(self, api_key: str):
        self.api = TMDBApi(api_key)
    
    def get_popular_movies(self, pages: int = 5) -> List[Dict]:
        """
        Get multiple pages of popular movies
        
        Args:
            pages: Number of pages to fetch (20 movies per page)
            
        Returns:
            List of movie data dictionaries
        """
        movies = []
        
        for page in tqdm(range(1, pages + 1), desc="Fetching movies"):
            response = self.api.get_popular_movies(page)
            movies.extend(response.get("results", []))
            time.sleep(0.25)  # Respect rate limits
        
        print(f"Collected data for {len(movies)} movies")
        return movies
    
    def get_movie_with_details(self, movie_id: int) -> Dict:
        """
        Get detailed movie information including credits
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            Enriched movie data
        """
        movie = self.api.get_movie_details(movie_id)
        credits = self.api.get_movie_credits(movie_id)
        
        # Add credits to movie data
        movie["credits"] = credits
        
        return movie
    
    def get_genres(self) -> List[Dict]:
        """
        Get all movie genres
        
        Returns:
            List of genre dictionaries
        """
        response = self.api.get_genres()
        return response.get("genres", [])
