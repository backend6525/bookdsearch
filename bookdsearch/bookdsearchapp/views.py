from django.shortcuts import render

# Create your views here.
# bookdsearchapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
import pandas as pd
import requests
from bs4 import BeautifulSoup


# def scrape_book_data(title, author):
#     # Placeholder function for scraping or using an API for genres, tags, and images
#     genre = 'Fiction'  # Replace with actual scraping logic
#     tags = ['Suspense', 'Thriller']  # Replace with actual scraping logic
#     image_url = 'https://example.com/sample-cover.jpg'  # Replace with actual image scraping logic
#     return genre, tags, image_url

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Read Excel file
#             excel_file = request.FILES['file']
#             df = pd.read_excel(excel_file)

#             # Extract book titles and authors
#             book_data = []
#             for _, row in df.iterrows():
#                 title = row['Title']
#                 author = row['Author']
#                 genre, tags, image_url = scrape_book_data(title, author)
#                 book_data.append({
#                     'title': title,
#                     'author': author,
#                     'genre': genre,
#                     'tags': ', '.join(tags),
#                     'image_url': image_url
#                 })

#             # Pass data to template
#             return render(request, 'bookdsearchapp/results.html', {'book_data': book_data})
#     else:
#         form = UploadFileForm()
#     return render(request, 'bookdsearchapp/upload.html', {'form': form})


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Read Excel file
#             excel_file = request.FILES['file']
#             df = pd.read_excel(excel_file)

#             # Extract book titles and authors
#             book_data = []
#             for _, row in df.iterrows():
#                 title = row['Title']
#                 author = row['Author']

#                 # Fetch data from Google Books API
#                 genre, tags, image_url = fetch_book_data_google(title, author)

#                 # If no image from Google Books, use BeautifulSoup to scrape a high-res image
#                 if not image_url or 'zoom=2' not in image_url:
#                     image_url = fetch_high_res_image(title)

#                 book_data.append({
#                     'title': title,
#                     'author': author,
#                     'genre': genre,
#                     'tags': ', '.join(tags),
#                     'image_url': image_url
#                 })

#             # Pass data to template
#             return render(request, 'bookdsearchapp/results.html', {'book_data': book_data})
#     else:
#         form = UploadFileForm()
#     return render(request, 'bookdsearchapp/upload.html', {'form': form})# bookdsearchapp/views.py

from .scraping_utils import scrape_book_data

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Read Excel file
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            # Extract book titles and authors
            book_data = []
            for _, row in df.iterrows():
                title = row['Title']
                author = row['Author']

                # Scrape data from multiple sources
                genre, tags, image_url = scrape_book_data(title, author)

                book_data.append({
                    'title': title,
                    'author': author,
                    'genre': genre,
                    'tags': ', '.join(tags),
                    'image_url': image_url
                })

            # Pass data to template
            return render(request, 'bookdsearchapp/results.html', {'book_data': book_data})
    else:
        form = UploadFileForm()
    return render(request, 'bookdsearchapp/upload.html', {'form': form})
