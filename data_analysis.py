import pandas as pd
import numpy as np
import os

# Check if the cleaned data already exists
if os.path.exists('cleaned_netflix_titles.csv'):
    # Load the cleaned dataset if it exists
    df = pd.read_csv('cleaned_netflix_titles.csv')
    # Print confirmation message
    print("Loaded cleaned data from 'cleaned_netflix_titles.csv'.")
else:
    # Load the raw dataset if cleaned does not exist
    df = pd.read_csv('netflix_titles.csv')

    # Remove leading commas in 'country' column
    df['country'] = df['country'].str.lstrip(',')

    # Extract the year from the 'date_added' column using regex
    df['year_added'] = df['date_added'].str.extract(r'(\d{4})', expand=False)
    # Convert 'year_added' to numeric, then to integer after filling NaN values
    df['year_added'] = pd.to_numeric(df['year_added'], errors='coerce').fillna(0).astype(int)

    # Move values of 'rating' column resembling duration
    # Filter rows in 'rating' column containing "[digits] min"
    rating_filter = df['rating'].str.contains(r'\d+\s*min', na=False)
    # Set the 'duration' column to have the values from the rating column
    df.loc[rating_filter, 'duration'] = df.loc[rating_filter, 'rating']
    # Set the filtered rows' 'rating' column to NaN
    df.loc[rating_filter, 'rating'] = np.nan

    # Drop 'duration' column due to inconsistent data
    df.drop('duration', axis=1, inplace=True)

    # Fill missing values with "Unknown"
    df.fillna('Unknown', inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Reset index after cleaning
    df.reset_index(drop=True, inplace=True)

    # Save the cleaned data to a new CSV file
    df.to_csv('cleaned_netflix_titles.csv', index=False)
    # Print confirmation message
    print("Cleaned data saved to 'cleaned_netflix_titles.csv'.")