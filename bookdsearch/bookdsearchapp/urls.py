# bookdsearchapp/urls.py

from django.urls import path
from . import views
from . import scrape_views  # Add this import
from .scrape_views import scrape_data, save_data 

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('upload/', views.upload_file, name='upload_file'),
    path('scrape/', scrape_data, name='scrape_data'),
    path('save/', save_data, name='save_data'), 
      # Now this will work
]
