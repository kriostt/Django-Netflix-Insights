from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from movies_and_shows.models import NetflixShow

# Function to generate plot for the most common genres
def titles_per_genre_plot(titles):
    # Retrieve list of genres from 'listed_in' column
    genres = titles.values_list('listed_in', flat=True)
    # Split genres separated by commas into individual genres
    genres = [genre for sublist in genres for genre in sublist.split(', ')]
    # Count the frequency of each genre
    genre_counts = pd.Series(genres).value_counts()

    # Create a plot for the top 5 most common genres
    fig, ax = plt.subplots()
    ax.bar(genre_counts.head(5).index, genre_counts.head(5).values, color=plt.cm.Paired.colors[:5])

    # Customize title, axis labels, x-tick rotation
    ax.set_title('Top 5 Most Common Genres on Netflix', fontsize=12)
    ax.set_xlabel('Genres', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.tick_params(axis='x', rotation=25)

    # Use tight layout to avoid overlapping
    plt.tight_layout()

    # Return the plot figure
    return fig

# Function to generate plot for the content distribution by ratings
def titles_per_rating_plot(titles):
    # Retrieve list of ratings from 'rating' column
    ratings = titles.values_list('rating', flat=True)
    # Count the frequency of each rating
    rating_counts = pd.Series(ratings).value_counts()  

    # Create a plot for the content distribution by ratings
    fig, ax = plt.subplots()
    ax.bar(rating_counts.index, rating_counts.values, color=plt.cm.Paired.colors[:len(rating_counts)])

    # Customize title, axis labels, x-tick rotation
    ax.set_title('Content Distribution by Ratings', fontsize=12)
    ax.set_xlabel('Ratings', fontsize=10)
    ax.set_ylabel('Number of Titles', fontsize=10)
    ax.tick_params(axis='x', rotation=25)

    # Use tight layout to avoid overlapping
    plt.tight_layout()

    # Return the plot figure
    return fig

# Function to generate plot for trend of additions over the years
def titles_per_year_plot(titles):
    # Retrieve list of years from 'year_added' column
    years = titles.values_list('year_added', flat=True)
    # Filter out rows where year_added is NaN or invalid
    # Remove NaN values from list
    valid_years = pd.Series(years).dropna() 
    # Remove invalid year valiues
    valid_years = valid_years[valid_years > 0]
    # Count the frequency of additions by year
    yearly_additions = valid_years.value_counts().sort_index()

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

    # Use tight layout to avoid overlapping
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
    # Return base64 string of image 
    return base64.b64encode(img.getvalue()).decode('utf-8')

# Main view function to handle the analysis page request with filters
def analysis_view(request):
    # Retrieve all Netflix titles from database
    titles = NetflixShow.objects.all()

    # Get filter parameters from request
    genre_filter = request.GET.get('genre', None)
    rating_filter = request.GET.get('rating', None)
    year_filter = request.GET.get('year', None)

    # Apply filters to titles if filters are provided
    if genre_filter:
        titles = titles.filter(listed_in__icontains=genre_filter)
    if rating_filter:
        titles = titles.filter(rating=rating_filter)
    if year_filter:
        titles = titles.filter(year_added=year_filter)

    # Generate the plots using the filtered queryset
    genre_plot = titles_per_genre_plot(titles)
    rating_plot = titles_per_rating_plot(titles)
    year_plot = titles_per_year_plot(titles)

    # Convert the plots to base64 images for embedding in template
    genre_plot_data = plot_to_base64(genre_plot)
    rating_plot_data = plot_to_base64(rating_plot)
    year_plot_data = plot_to_base64(year_plot)

    # Get unique values for dropdown filters (genres, ratings, years)
    genres = titles.values_list('listed_in', flat=True).distinct()
    ratings = titles.values_list('rating', flat=True).distinct()
    years = titles.values_list('year_added', flat=True).distinct()

    # Prepare context data to pass to the template
    context = {
        'genre_plot': genre_plot_data,
        'rating_plot': rating_plot_data,
        'year_plot': year_plot_data,
        'genres': genres,
        'ratings': ratings,
        'years': sorted(years),
        'selected_genre': genre_filter,
        'selected_rating': rating_filter,
        'selected_year': year_filter,
    }

    # Render the 'analysis.html' with the context data
    return render(request, 'analysis.html', context)
