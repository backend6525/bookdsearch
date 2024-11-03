from django.shortcuts import render

# Create your views here.
# bookdsearchapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
from .scraping_utils import scrape_book_data

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

#                 # Scrape data from multiple sources
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

logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Read Excel file
                excel_file = request.FILES['file']
                df = pd.read_excel(excel_file)

                # Validate columns
                if 'Title' not in df.columns or 'Author' not in df.columns:
                    return JsonResponse({'error': 'Invalid file format. Columns "Title" and "Author" are required.'}, status=400)

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
            except Exception as e:
                logger.error(f"Error processing file: {e}")
                return JsonResponse({'error': 'An error occurred while processing the file.'}, status=500)
    else:
        form = UploadFileForm()
    return render(request, 'bookdsearchapp/upload.html', {'form': form})