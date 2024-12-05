import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# Check if the cleaned data already exists
if os.path.exists('cleaned_netflix_titles.csv'):
    # Load the cleaned dataset if it exists
    df = pd.read_csv('cleaned_netflix_titles.csv')
    print("Loaded cleaned data from 'cleaned_netflix_titles.csv'.")
else:
    # Load the raw dataset
    df = pd.read_csv('netflix_titles.csv')

    # Remove leading commas in country column
    df['country'] = df['country'].str.lstrip(',')

    # Drop rows with missing values in the 'date_added' column
    df.dropna(subset=['date_added'], inplace=True)
    # Extract the year from the 'date_added' column using regex
    df['year_added'] = df['date_added'].str.extract(r'(\d{4})', expand=False)
    # Convert 'year_added' to numeric, then to integer after filling NaN values
    df['year_added'] = pd.to_numeric(df['year_added'], errors='coerce').fillna(0).astype(int)

    # Convert 'release_year' to numeric for analysis
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').fillna(0).astype(int)

    # Move values of 'rating' column resembling duration
    # Filter rows in 'rating' column containing "[digits] min"
    rating_filter = df['rating'].str.contains(r'\d+\s*min', na=False)
    # Set the 'duration' column to have the values from the rating column
    df.loc[rating_filter, 'duration'] = df.loc[rating_filter, 'rating']
    # Set the filtered rows' 'rating' column to NaN
    df.loc[rating_filter, 'rating'] = np.nan
    # Drop rows with missing values in the 'rating' column
    df.dropna(subset=['rating'], inplace=True)

    # Drop 'duration' column 
    df.drop('duration', axis=1, inplace=True)

    # Fill missing values with 'Unknown'
    df.fillna('Unknown', inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Reset index after cleaning
    df.reset_index(drop=True, inplace=True)

    # Save the cleaned data to a new CSV file
    df.to_csv('cleaned_netflix_titles.csv', index=False)
    print("Cleaned data saved to 'cleaned_netflix_titles.csv'.")

# Common Genres
genres = df['listed_in'].str.split(', ').explode()

# Count the frequency of each genre
genre_counts = genres.value_counts()

# Set up 1x3 subplots (all three subplots in one row)
fig, axs = plt.subplots(1, 3, figsize=(18, 7))

# First subplot - Bar chart for the most common genres
axs[0].bar(genre_counts.head(5).index, genre_counts.head(5).values, color=plt.cm.Paired.colors[:5])
axs[0].set_title('Top 5 Most Common Genres on Netflix', fontsize=12)
axs[0].set_xlabel('Genres', fontsize=10)
axs[0].set_ylabel('Frequency', fontsize=10)

# Adjust the x-axis labels size
axs[0].tick_params(axis='x', rotation=45)

# Second subplot - Line plot for the trend of additions over the years
# Filter out rows where `year_added` is NaN or invalid
valid_years = df['year_added'].notna() & (df['year_added'] > 0)  # Keep only valid years
yearly_additions = df[valid_years].groupby('year_added').size()
# Plot the trend of additions over years
yearly_additions.plot(kind='line', marker='o', title='Trend of Additions Over Years', ax=axs[1])
# Set x-axis limits to avoid starting from 0 (only valid years)
axs[1].set_xlim(yearly_additions.index.min(), yearly_additions.index.max())
# Customize x-axis labels and ticks
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Number of Titles Added')
axs[1].set_xticks(yearly_additions.index) 
axs[1].tick_params(axis='x', rotation=45)



# Third subplot - Scatter plot between rating and release year (as an example)
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df.dropna(subset=['release_year'], inplace=True)
axs[2].scatter(df['release_year'], df['rating'], alpha=0.5, color=plt.cm.Paired.colors[3])
axs[2].set_xlabel('Release Year')
axs[2].set_ylabel('Rating', fontsize=10)
axs[2].set_title('Rating vs. Release Year')

# Adjust layout for better spacing
plt.tight_layout()
plt.subplots_adjust(wspace=0.3)  # Increase the horizontal space

# Display the plot
plt.show()
