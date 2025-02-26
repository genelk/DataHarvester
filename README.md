# DataHarvester
An ETL workflow that scrapes public data, transforms it, and loads it into a database.

Key Elements:

1. Web scraper for publicly available data (weather, stock prices, etc.)
2. Data cleaning and transformation pipeline
3. Database storage with simple query examples
4. Basic dashboard or reporting element

Technologies: Python, BeautifulSoup/Scrapy, pandas, SQLite/PostgreSQL

# DataHarvester

A data pipeline that collects, processes, and visualizes movie data from The Movie Database (TMDB) API.

## Features
- Fetch movie data from TMDB's public API
- Process and clean data with pandas
- Store data in SQLite database
- Visualize movie stats with matplotlib/seaborn

## Setup
1. Clone this repository
2. Get a free API key from [TMDB](https://www.themoviedb.org/documentation/api)
3. Create a `.env` file in the root directory with: `TMDB_API_KEY=your_api_key_here`
4. Install requirements: `pip install -r requirements.txt`
5. Run the application: `python main.py`

## Data Pipeline
This project demonstrates a complete ETL (Extract, Transform, Load) pipeline:
- **Extract**: Fetch data from TMDB API
- **Transform**: Clean, normalize, and enrich the data
- **Load**: Store in SQLite database
- **Visualize**: Create insights through data visualization

## Technologies
- Python 3.8+
- pandas for data processing
- SQLite for data storage
- matplotlib/seaborn for visualization
- requests for API interaction
