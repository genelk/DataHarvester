import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

class DataTransformer:
    """
    Transforms raw movie data into clean, structured format
    """
    
    def process_movies(self, movies: List[Dict], genres: List[Dict]) -> pd.DataFrame:
        """
        Process movie data into a clean pandas DataFrame
        
        Args:
            movies: List of raw movie data dictionaries
            genres: List of genre dictionaries
            
        Returns:
            Processed DataFrame
        """
        # Create a genre lookup dictionary
        genre_lookup = {genre["id"]: genre["name"] for genre in genres}
        
        # Extract relevant fields and normalize data
        processed_data = []
        
        for movie in movies:
            # Convert genre IDs to names
            genre_names = [genre_lookup.get(genre_id, "Unknown") 
                          for genre_id in movie.get("genre_ids", [])]
            
            # Parse release date
            release_date = None
            try:
                if movie.get("release_date"):
                    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
            except ValueError:
                pass  # Keep as None if date is invalid
            
            # Create processed movie record
            processed_movie = {
                "id": movie.get("id"),
                "title": movie.get("title"),
                "original_title": movie.get("original_title"),
                "overview": movie.get("overview"),
                "popularity": movie.get("popularity"),
                "vote_average": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "release_date": release_date,
                "release_year": release_date.year if release_date else None,
                "genres": ", ".join(genre_names),
                "genre_list": genre_names,
                "adult": movie.get("adult", False),
                "poster_path": movie.get("poster_path"),
                "backdrop_path": movie.get("backdrop_path"),
                "original_language": movie.get("original_language")
            }
            
            processed_data.append(processed_movie)
        
        # Create DataFrame
        df = pd.DataFrame(processed_data)
        
        # Clean and transform data
        return self._clean_dataframe(df)
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform the DataFrame
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Make a copy to avoid SettingWithCopyWarning
        cleaned_df = df.copy()
        
        # Fill missing values
        cleaned_df["overview"] = cleaned_df["overview"].fillna("")
        cleaned_df["vote_average"] = cleaned_df["vote_average"].fillna(0)
        cleaned_df["vote_count"] = cleaned_df["vote_count"].fillna(0)
        cleaned_df["popularity"] = cleaned_df["popularity"].fillna(0)
        
        # Create additional features
        cleaned_df["has_english_title"] = cleaned_df["title"] == cleaned_df["original_title"]
        cleaned_df["title_length"] = cleaned_df["title"].str.len()
        cleaned_df["overview_length"] = cleaned_df["overview"].str.len()
        
        # Calculate weighted rating (IMDB formula)
        # Weighted Rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C
        # Where:
        # v = vote count
        # m = minimum votes required (we'll use 100)
        # R = average rating for the movie
        # C = mean vote across the whole dataset
        m = 100  # minimum votes required
        C = cleaned_df["vote_average"].mean()
        
        cleaned_df["weighted_rating"] = (
            (cleaned_df["vote_count"] / (cleaned_df["vote_count"] + m)) * cleaned_df["vote_average"] +
            (m / (cleaned_df["vote_count"] + m)) * C
        )
        
        return cleaned_df
