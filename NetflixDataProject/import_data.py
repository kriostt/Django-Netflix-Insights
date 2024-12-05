import pandas as pd
from movies_and_shows.models import NetflixShow

# Load the cleaned dataset
df = pd.read_csv('/Users/alessandrahenriz/Desktop/Django-Netflix-Insights/cleaned_netflix_titles.csv')

# Loop through each row and insert data into the database
for index, row in df.iterrows():
    # Handle the 'date_added' column: Convert to datetime, coerce errors to NaT
    date_added = pd.to_datetime(row['date_added'], errors='coerce') if 'date_added' in row else None

    # If 'date_added' is a valid date, assign it; otherwise, leave as None
    if pd.isna(date_added):
        date_added = None
    
    # Handle the 'year_added' column: Get the year from the 'year_added' column
    year_added = row['year_added'] if 'year_added' in row else None

    # Check if the show_id already exists to avoid duplicates
    if not NetflixShow.objects.filter(show_id=row['show_id']).exists():
        # Create and save the model instance
        NetflixShow.objects.create(
            show_id=row['show_id'],  # Assuming the dataset has a unique show_id column
            type=row['type'],  # Movie or TV Show
            title=row['title'],  # Show title
            director=row['director'] if 'director' in row else None,  # Director(s), can be empty
            cast=row['cast'] if 'cast' in row else None,  # Cast, can be empty
            country=row['country'] if 'country' in row else None,  # Country, can be empty
            date_added=date_added,  # Only valid dates will be assigned here
            year_added=year_added, 
            release_year=row['release_year'],  # Year of release
            rating=row['rating'],  # Rating (e.g., PG, R)
            listed_in=row['listed_in'],  # Genre or categories
            description=row['description'] if 'description' in row else None  # Description of the show
        )

print("Cleaned data successfully imported into the database.")
