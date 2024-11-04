# bookdsearchapp/urls.py

from django.urls import path
from . import views
from . import scrape_views  # Add this import

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('scrape/', scrape_views.scrape_data, name='scrape_data'),  # Now this will work
]
