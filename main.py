import os
import time
from dotenv import load_dotenv

from scraper.data_collector import MovieDataCollector
from processor.transformer import DataTransformer
from storage.db_connector import DatabaseConnector
from dashboard.visualizer import MovieDashboard

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("Error: No API key found. Please create a .env file with your TMDB_API_KEY.")
        return
    
    print("Starting DataHarvester pipeline...")
    start_time = time.time()
    
    # Step 1: Collect data
    print("\n--- Step 1: Collecting movie data from TMDB API ---")
    collector = MovieDataCollector(api_key)
    raw_movies = collector.get_popular_movies(pages=5)  # Get 100 movies (20 per page)
    raw_genres = collector.get_genres()
    
    # Step 2: Transform data
    print("\n--- Step 2: Transforming and cleaning data ---")
    transformer = DataTransformer()
    movies_df = transformer.process_movies(raw_movies, raw_genres)
    
    # Step 3: Store in database
    print("\n--- Step 3: Storing data in SQLite database ---")
    db = DatabaseConnector("movie_data.db")
    db.create_tables()
    db.store_movies(movies_df)
    
    # Step 4: Visualize data
    print("\n--- Step 4: Generating visualizations ---")
    dashboard = MovieDashboard(db)
    dashboard.generate_visualizations()
    
    elapsed_time = time.time() - start_time
    print(f"\nDataHarvester pipeline completed in {elapsed_time:.2f} seconds!")

if __name__ == "__main__":
    main()
