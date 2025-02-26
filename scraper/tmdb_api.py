import requests
from typing import Dict, List, Any, Optional

class TMDBApi:
    """
    Wrapper for The Movie Database (TMDB) API
    """
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a request to the TMDB API
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["api_key"] = self.api_key
        
        response = self.session.get(url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        return response.json()
    
    def get_popular_movies(self, page: int = 1) -> Dict:
        """
        Get popular movies
        
        Args:
            page: Page number
            
        Returns:
            Page of popular movies
        """
        return self._make_request("/movie/popular", {"page": page})
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """
        Get detailed information about a movie
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            Movie details
        """
        return self._make_request(f"/movie/{movie_id}")
    
    def get_movie_credits(self, movie_id: int) -> Dict:
        """
        Get cast and crew for a movie
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            Movie credits
        """
        return self._make_request(f"/movie/{movie_id}/credits")
    
    def get_genres(self) -> Dict:
        """
        Get the list of official genres
        
        Returns:
            List of movie genres
        """
        return self._make_request("/genre/movie/list")
