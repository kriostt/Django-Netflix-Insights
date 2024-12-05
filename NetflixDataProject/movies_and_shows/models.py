from django.db import models

# Create your models here
class NetflixShow(models.Model):
    show_id = models.CharField(max_length=50, unique=True)  # Unique ID for each show
    type = models.CharField(max_length=50)  # Movie or TV Show
    title = models.CharField(max_length=200)  # Show title
    director = models.CharField(max_length=200, null=True, blank=True)  # Director(s), can be empty
    cast = models.CharField(max_length=500, null=True, blank=True)  # Cast, can be empty
    country = models.CharField(max_length=200, null=True, blank=True)  # Country, can be empty
    date_added = models.DateField(null=True, blank=True)  # Date when the show was added to Netflix
    year_added = models.IntegerField(null=True, blank=True)  # Year when the show was added to Netflix 
    release_year = models.IntegerField()  # Year of release
    rating = models.CharField(max_length=50)  # Rating (e.g., PG, R)
    listed_in = models.CharField(max_length=200)  # Genre or categories
    description = models.TextField(null=True, blank=True)  # Description of the show

    def __str__(self):
        return self.title
