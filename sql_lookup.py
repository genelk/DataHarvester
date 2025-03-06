import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('movie_data.db')

# Query the top 10 movies by weighted rating
query = """
SELECT title, release_year, vote_average, weighted_rating 
FROM movies 
ORDER BY weighted_rating DESC 
LIMIT 10
"""

# Execute query and load results into a DataFrame
df = pd.read_sql_query(query, conn)

# Display the results
print("\nTop 10 Movies by Weighted Rating:")
print(df)

# Close the connection
conn.close()
