from django.urls import path
from . import views

urlpatterns = [
    # path('data-visualization/', views.data_visualization),
    path('analysis/', views.analysis_view)
]
