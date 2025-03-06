import sqlite3
import pandas as pd
import os

class DatabaseConnector:
    """
    Handles database connections and operations
    """
    
    def __init__(self, db_path: str):
        """
        Initialize database connector
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
    
    def create_tables(self):
        """
        Create database tables if they don't exist
        """
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create movies table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        original_title TEXT,
        overview TEXT,
        popularity REAL,
        vote_average REAL,
        vote_count INTEGER,
        release_date TEXT,
        release_year INTEGER,
        genres TEXT,
        adult INTEGER,
        poster_path TEXT,
        backdrop_path TEXT,
        original_language TEXT,
        weighted_rating REAL,
        has_english_title INTEGER,
        title_length INTEGER,
        overview_length INTEGER
        )
        ''')
        
        # Create genres table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        ''')
        
        # Create movie_genres relationship table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_genres (
            movie_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (movie_id, genre_id),
            FOREIGN KEY (movie_id) REFERENCES movies (id),
            FOREIGN KEY (genre_id) REFERENCES genres (id)
        )
        ''')
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
    
    def store_movies(self, movies_df: pd.DataFrame):
        """
        Store movie data in the database
        
        Args:
            movies_df: DataFrame containing movie data
        """
        # Convert release_date to string format for SQLite
        df_to_store = movies_df.copy()
        if "release_date" in df_to_store.columns:
            df_to_store["release_date"] = df_to_store["release_date"].astype(str)
        
        # Remove list columns that can't be stored directly
        if "genre_list" in df_to_store.columns:
            df_to_store = df_to_store.drop(columns=["genre_list"])
        
        # Connect to database
        conn = sqlite3.connect(self.db_path)
        
        # Store in database using pandas to_sql but with sqlite3 connection
        df_to_store.to_sql("movies", conn, if_exists="replace", index=False)
        
        print(f"Stored {len(df_to_store)} movies in the database")
        
        # Close connection
        conn.close()
    
    def get_movies(self) -> pd.DataFrame:
        """
        Get all movies from the database
        
        Returns:
            DataFrame containing all movies
        """
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT * FROM movies", conn)
        conn.close()
        return df
    
    def get_top_rated_movies(self, limit: int = 10) -> pd.DataFrame:
        """
        Get top rated movies based on weighted rating
        
        Args:
            limit: Number of movies to return
            
        Returns:
            DataFrame with top rated movies
        """
        conn = sqlite3.connect(self.db_path)
        query = f"""
        SELECT id, title, release_year, vote_average, vote_count, weighted_rating
        FROM movies
        ORDER BY weighted_rating DESC
        LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def get_movies_by_year(self) -> pd.DataFrame:
        """
        Get movie counts grouped by year
        
        Returns:
            DataFrame with movie counts by year
        """
        conn = sqlite3.connect(self.db_path)
        query = """
        SELECT release_year, COUNT(*) as movie_count
        FROM movies
        WHERE release_year IS NOT NULL
        GROUP BY release_year
        ORDER BY release_year
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
