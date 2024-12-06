from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Function to generate plot for the most common genres
def titles_per_genre_plot(df):
    # Split the 'listed_in' column by commas and explode into rows
    genres = df['listed_in'].str.split(', ').explode()
    # Count the frequency of each genre
    genre_counts = genres.value_counts()

    # Create a plot for the top 5 most common genres
    fig, ax = plt.subplots()
    ax.bar(genre_counts.head(5).index, genre_counts.head(5).values, color=plt.cm.Paired.colors[:5])

    # Customize title, axis labels, x-tick rotation
    ax.set_title('Top 5 Most Common Genres on Netflix', fontsize=12)
    ax.set_xlabel('Genres', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.tick_params(axis='x', rotation=25)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Return the plot figure
    return fig

# Function to generate plot for the content distribution by ratings
def titles_per_rating_plot(df):
    # Count the frequency of each rating
    rating_counts = df['rating'].value_counts()  

    # Create a plot for the content distribution by ratings
    fig, ax = plt.subplots()
    ax.bar(rating_counts.index, rating_counts.values, color=plt.cm.Paired.colors[:len(rating_counts)])

    # Customize title, axis labels, x-tick rotation
    ax.set_title('Content Distribution by Ratings', fontsize=12)
    ax.set_xlabel('Ratings', fontsize=10)
    ax.set_ylabel('Number of Titles', fontsize=10)
    ax.tick_params(axis='x', rotation=25)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Return the plot figure
    return fig

# Function to generate plot for trend of additions over the years
def titles_per_year_plot(df):
    # Filter out rows where year_added is NaN or invalid
    valid_years = df['year_added'].notna() & (df['year_added'] > 0)
    yearly_additions = df[valid_years].groupby('year_added').size()

    # Create a plot for the trend of additions over the years
    fig, ax = plt.subplots()
    ax.plot(yearly_additions.index, yearly_additions.values, marker='o')

    # Set x-axis limits to avoid starting from 0 (only valid years)
    ax.set_xlim(yearly_additions.index.min(), yearly_additions.index.max())

    # Customize title, axis labels, ticks
    ax.set_title('Trend of Additions Over Years', fontsize=12)
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Number of Titles Added', fontsize=10)
    ax.set_xticks(yearly_additions.index) 
    ax.tick_params(axis='x', rotation=25)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Return the plot figure
    return fig

# Function to convert plot figure to base64 string for embedding in template
def plot_to_base64(fig):
    # Create an in-memory byte stream to save the plot
    img = io.BytesIO()
    # Save the figure as PNG format to the byte stream
    fig.savefig(img, format='png')
    # Rewind the byte stream to the beginning
    img.seek(0)
    # Return converted byte data to base64 
    return base64.b64encode(img.getvalue()).decode('utf-8')

# Main view function to handle the analysis page request with filters
def analysis_view(request):
    # Load the cleaned Netflix dataset
    df = pd.read_csv("C:/Users/krisa/Desktop/CPRO 2201/Django-Netflix-Insights/cleaned_netflix_titles.csv")

    # Get the filter parameters from the request (use default None if not provided)
    genre_filter = request.GET.get('genre', None)
    rating_filter = request.GET.get('rating', None)
    year_filter = request.GET.get('year', None)

    # Apply filters to dataframe if filter values are provided
    # Filter by genre
    if genre_filter:
        df = df[df['listed_in'].str.contains(genre_filter, case=False, na=False)]
    # Filter by rating
    if rating_filter:
        df = df[df['rating'] == rating_filter]
    # Filter by year added
    if year_filter:
        df = df[df['year_added'] == int(year_filter)]

    # Generate the plots using the filtered data
    genre_plot = titles_per_genre_plot(df)
    rating_plot = titles_per_rating_plot(df)
    year_plot = titles_per_year_plot(df)

    # Convert the plots to base64 images for embedding in template
    genre_plot_data = plot_to_base64(genre_plot)
    rating_plot_data = plot_to_base64(rating_plot)
    year_plot_data = plot_to_base64(year_plot)

    # Get unique values for dropdown filters (genres, ratings, years)
    genres = df['listed_in'].str.split(', ').explode().unique()  # Unique genres from 'listed_in'
    ratings = df['rating'].unique()  # Unique ratings
    years = df['year_added'].unique()  # Unique years added

    # Prepare context data to pass to the template
    context = {
        'genre_plot': genre_plot_data,  # Plot for top genres
        'rating_plot': rating_plot_data,  # Plot for content distribution by ratings
        'trend_plot': year_plot_data,  # Plot for trend of additions over years
        'genres': genres,  # Dropdown options for genres
        'ratings': ratings,  # Dropdown options for ratings
        'years': sorted(years),  # Dropdown options for years (sorted)
        'selected_genre': genre_filter,  # Currently selected genre filter
        'selected_rating': rating_filter,  # Currently selected rating filter
        'selected_year': year_filter,  # Currently selected year filter
    }

    # Render the 'analysis_template.html' with the context data
    return render(request, 'analysis.html', context)
