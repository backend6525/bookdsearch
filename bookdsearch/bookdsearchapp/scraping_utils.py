# bookdsearchapp/scraping_utils.py

import requests
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

# # Google Books API setup
# API_KEY = 'YOUR_GOOGLE_API_KEY'  # Replace with your Google API Key
# service = build('books', 'v1', developerKey=API_KEY)

# def fetch_book_data_google(title, author):
#     """Fetch book metadata (genre, tags, cover image) from Google Books API."""
#     try:
#         query = f'intitle:{title} inauthor:{author}'
#         request = service.volumes().list(q=query, maxResults=1)
#         response = request.execute()

#         if 'items' in response:
#             volume_info = response['items'][0]['volumeInfo']
#             genre = volume_info.get('categories', ['Unknown'])[0]
#             tags = volume_info.get('categories', [])
#             image_url = volume_info.get('imageLinks', {}).get('thumbnail', '')

#             # Ensure image quality (upscale if possible)
#             if 'zoom=1' in image_url:
#                 image_url = image_url.replace('zoom=1', 'zoom=2')

#             return genre, tags, image_url
#         return 'Unknown', [], ''
#     except Exception as e:
#         print(f"Error fetching data from Google Books API: {e}")
#         return 'Unknown', [], ''

# def fetch_high_res_image(title):
#     """Fetch high-resolution image from Google search (as a fallback)."""
#     query = f"{title} book cover"
#     url = f"https://www.google.com/search?q={query}&tbm=isch"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     images = soup.find_all('img', {'src': True})

#     # Filter for large images (approximation)
#     for img in images:
#         img_url = img['src']
#         if 'encrypted-tbn0.gstatic.com' not in img_url:  # Filter out low-res thumbnails
#             return img_url
#     return ''
# bookdsearchapp/scraping_utils.py

import requests
from bs4 import BeautifulSoup
import time

def fetch_book_data_open_library(title, author):
    """Fetch book metadata (genre, tags, cover image) from Open Library API."""
    try:
        url = f"https://openlibrary.org/search.json?title={title}&author={author}"
        response = requests.get(url)
        data = response.json()

        if data['docs']:
            book_info = data['docs'][0]
            tags = book_info.get('subject', [])
            genre = tags[0] if tags else 'Unknown'
            cover_id = book_info.get('cover_i')
            image_url = f"http://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else ''
            return genre, tags, image_url
        return 'Unknown', [], ''
    except Exception as e:
        print(f"Open Library Error: {e}")
        return 'Unknown', [], ''

def fetch_book_data_goodreads(title, author):
    """Scrape book metadata from Goodreads (high-level example)."""
    try:
        search_url = f"https://www.goodreads.com/search?q={title}+{author}&search_type=books"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example parsing logic for genre and cover image (Goodreads structure may vary)
        genre = 'Fiction'  # Placeholder; actual parsing needed
        image_url = ''  # Placeholder; actual parsing needed
        # More detailed parsing here...

        return genre, ['Fiction', 'Adventure'], image_url
    except Exception as e:
        print(f"Goodreads Error: {e}")
        return 'Unknown', [], ''

def fetch_book_data_amazon(title, author):
    """Scrape book metadata from Amazon (example placeholder)."""
    try:
        search_url = f"https://www.amazon.com/s?k={title}+{author}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Amazon blocks bots aggressively; actual parsing might be challenging
        genre = 'Unknown'
        image_url = ''  # Replace with actual parsing

        return genre, ['Unknown'], image_url
    except Exception as e:
        print(f"Amazon Error: {e}")
        return 'Unknown', [], ''

def scrape_book_data(title, author):
    """Attempt to scrape book data from multiple sources."""
    # Priority order: Open Library -> Goodreads -> Amazon
    for fetch_function in [fetch_book_data_open_library, fetch_book_data_goodreads, fetch_book_data_amazon]:
        genre, tags, image_url = fetch_function(title, author)
        if genre != 'Unknown' and image_url:  # Check if valid data is returned
            return genre, tags, image_url
        time.sleep(1)  # Respect rate limits between requests
    return 'Unknown', [], ''  # Default return if all sources fail
