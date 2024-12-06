from django.urls import path
from . import views

# Defines URL patterns for this app
urlpatterns = [
    # Maps root to analysis_view function in views
    path('', views.analysis_view)
]
