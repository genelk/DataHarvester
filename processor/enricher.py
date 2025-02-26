import pandas as pd
from typing import Dict
import re

class DataEnricher:
    """
    Adds additional features and data to the movie dataset
    """
    
    def add_genre_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add one-hot encoded genre features
        
        Args:
            df: Movie DataFrame
            
        Returns:
            DataFrame with added genre features
        """
        # Create a copy to avoid SettingWithCopyWarning
        enriched_df = df.copy()
        
        # Get all unique genres
        all_genres = set()
        for genres in enriched_df["genre_list"]:
            if isinstance(genres, list):
                all_genres.update(genres)
        
        # Create one-hot encoded columns for genres
        for genre in all_genres:
            col_name = f"genre_{genre.lower().replace(' ', '_')}"
            enriched_df[col_name] = enriched_df["genre_list"].apply(
                lambda x: 1 if isinstance(x, list) and genre in x else 0
            )
        
        return enriched_df
    
    def add_language_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add features related to language
        
        Args:
            df: Movie DataFrame
            
        Returns:
            DataFrame with added language features
        """
        # Create a copy to avoid SettingWithCopyWarning
        enriched_df = df.copy()
        
        # Add common language indicators
        common_languages = ["en", "es", "fr", "de", "it", "ja", "ko", "zh"]
        for lang in common_languages:
            enriched_df[f"is_{lang}"] = (enriched_df["original_language"] == lang).astype(int)
        
        # Group other languages
        enriched_df["is_other_language"] = (~enriched_df["original_language"].isin(common_languages)).astype(int)
        
        return enriched_df
    
    def extract_title_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from movie titles
        
        Args:
            df: Movie DataFrame
            
        Returns:
            DataFrame with title features
        """
        # Create a copy to avoid SettingWithCopyWarning
        enriched_df = df.copy()
        
        # Check for patterns in titles
        enriched_df["has_colon_in_title"] = enriched_df["title"].str.contains(":").astype(int)
        enriched_df["has_number_in_title"] = enriched_df["title"].str.contains(r'\d').astype(int)
        
        # Check for sequel indicators
        sequel_patterns = r'(?i)(part|vol|volume|episode|\bii\b|\biii\b|\biv\b|2|3|4)$'
        enriched_df["is_likely_sequel"] = enriched_df["title"].str.contains(sequel_patterns).astype(int)
        
        return enriched_df
