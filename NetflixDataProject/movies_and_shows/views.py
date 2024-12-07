from django.shortcuts import render
from .models import NetflixShow
from .plot import titles_per_genre_plot, titles_per_rating_plot, titles_per_year_plot, plot_to_base64

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

    # Generate the plots using the filtered titles
    genre_plot = titles_per_genre_plot(titles)
    rating_plot = titles_per_rating_plot(titles)
    year_plot = titles_per_year_plot(titles)

    # Convert the plots to base64 images for embedding in template
    genre_plot_data = plot_to_base64(genre_plot)
    rating_plot_data = plot_to_base64(rating_plot)
    year_plot_data = plot_to_base64(year_plot)

    # Get unique values for dropdown filters (genres, ratings, years)
    # Retrieve list of genres from 'listed_in' column
    genres = titles.values_list('listed_in', flat=True)
    # Split genres separated by commas into individual genres
    genres = [genre for sublist in genres for genre in sublist.split(', ')]
    # Get unique genres using set to remove duplicates
    unique_genres = list(set(genres))
    # Get unique ratings 
    ratings = titles.values_list('rating', flat=True).distinct()
    # Get unique years
    years = titles.values_list('year_added', flat=True).distinct()
    # Get only years greater than 0
    valid_years = [year for year in years if year > 0]

    # Prepare context data to pass to the template
    context = {
        'genre_plot': genre_plot_data,
        'rating_plot': rating_plot_data,
        'year_plot': year_plot_data,
        'genres': sorted(unique_genres),
        'ratings': sorted(ratings),
        'years': sorted(valid_years),
        'selected_genre': genre_filter,
        'selected_rating': rating_filter,
        'selected_year': int(year_filter) if year_filter else None,
    }

    # Render the 'analysis_template.html' with the context data
    return render(request, 'analysis_template.html', context)
