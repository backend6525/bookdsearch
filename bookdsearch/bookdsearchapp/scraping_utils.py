# import requests
# from bs4 import BeautifulSoup
# import time
# import logging
# from urllib.parse import quote

# # Configure logging
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def fetch_book_data_open_library(title, author):
#     """Fetch book metadata (genre, tags, cover image) from Open Library API."""
#     try:
#         url = f"https://openlibrary.org/search.json?title={quote(title)}&author={quote(author)}"
#         logger.info(f"Fetching data from Open Library: {url}")
#         response = requests.get(url)
#         logger.info(f"Open Library response status: {response.status_code}")
#         data = response.json()
#         logger.debug(f"Open Library response content: {data}")

#         if data['docs']:
#             book_info = data['docs'][0]
#             tags = book_info.get('subject', [])
#             genre = tags[0] if tags else 'Unknown'
#             cover_id = book_info.get('cover_i')
#             image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else ''
#             return genre, tags, image_url
#         return 'Unknown', [], ''
#     except Exception as e:
#         logger.error(f"Open Library Error: {e}")
#         return 'Unknown', [], ''

# def fetch_book_data_goodreads(title, author):
#     """Scrape book metadata from Goodreads (high-level example)."""
#     try:
#         search_url = f"https://www.goodreads.com/search?q={quote(title)}+{quote(author)}&search_type=books"
#         headers = {'User-Agent': 'Mozilla/5.0'}
#         logger.info(f"Fetching data from Goodreads: {search_url}")
#         response = requests.get(search_url, headers=headers)
#         logger.info(f"Goodreads response status: {response.status_code}")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         logger.debug(f"Goodreads response content: {soup}")

#         # Example parsing logic for genre and cover image (Goodreads structure may vary)
#         genre = 'Fiction'  # Placeholder; actual parsing needed
#         image_url = ''  # Placeholder; actual parsing needed
#         # More detailed parsing here...

#         return genre, ['Fiction', 'Adventure'], image_url
#     except Exception as e:
#         logger.error(f"Goodreads Error: {e}")
#         return 'Unknown', [], ''

# def fetch_book_data_general_search(title, author):
#     """Perform a general web search to fetch book metadata."""
#     try:
#         search_query = f"{quote(title)} {quote(author)} book genre tags cover image"
#         search_url = f"https://www.google.com/search?q={search_query}"
#         headers = {'User-Agent': 'Mozilla/5.0'}
#         logger.info(f"Performing general search: {search_url}")
#         response = requests.get(search_url, headers=headers)
#         logger.info(f"General search response status: {response.status_code}")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         logger.debug(f"General search response content: {soup}")

#         # Example parsing logic (this will need to be adapted based on actual search results)
#         genre = 'Unknown'  # Placeholder; actual parsing needed
#         tags = ['Unknown']  # Placeholder; actual parsing needed
#         image_url = ''  # Placeholder; actual parsing needed
#         # More detailed parsing here...

#         return genre, tags, image_url
#     except Exception as e:
#         logger.error(f"General Search Error: {e}")
#         return 'Unknown', [], ''

# def fetch_book_data_from_custom_site(title, author, website_url):
#     """Fetch book data from a user-specified website."""
#     try:
#         logger.info(f"Fetching data from custom site: {website_url}")
#         response = requests.get(website_url)
#         logger.info(f"Custom site response status: {response.status_code}")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         logger.debug(f"Custom site response content: {soup}")

#         # Example parsing logic (this will need to be adapted based on actual website structure)
#         genre = 'Unknown'  # Placeholder; actual parsing needed
#         tags = ['Unknown']  # Placeholder; actual parsing needed
#         image_url = ''  # Placeholder; actual parsing needed
#         # More detailed parsing here...

#         return genre, tags, image_url
#     except Exception as e:
#         logger.error(f"Custom Site Error: {e}")
#         return 'Unknown', [], ''

# def scrape_book_data(title, author, website_url=None):
#     """Attempt to scrape book data from multiple sources and consolidate results."""
#     results = []

#     # If a specific website URL is provided, use it first
#     if website_url:
#         results.append(fetch_book_data_from_custom_site(title, author, website_url))

#     # Fetch data from various sources
#     for fetch_function in [fetch_book_data_open_library, fetch_book_data_goodreads, fetch_book_data_general_search]:
#         results.append(fetch_function(title, author))
#         time.sleep(1)  # Respect rate limits between requests

#     # Consolidate results
#     final_genre = 'Unknown'
#     final_tags = []
#     final_image_url = ''

#     for genre, tags, image_url in results:
#         if genre != 'Unknown' and final_genre == 'Unknown':
#             final_genre = genre
#         final_tags.extend(tags)
#         if image_url and not final_image_url:
#             final_image_url = image_url

#     final_tags = list(set(final_tags))  # Remove duplicates
#     return final_genre, final_tags, final_image_url


import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_book_data_open_library(title, author):
    """Fetch book metadata (genre, tags, cover image) from Open Library API."""
    try:
        url = f"https://openlibrary.org/search.json?title={quote(title)}&author={quote(author)}"
        response = requests.get(url)
        data = response.json()

        if data['docs']:
            book_info = data['docs'][0]
            tags = book_info.get('subject', [])
            genre = tags[0] if tags else 'Unknown'
            cover_id = book_info.get('cover_i')
            image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else ''
            return genre, tags, image_url
        return 'Unknown', [], ''
    except Exception as e:
        logger.error(f"Open Library Error: {e}")
        return 'Unknown', [], ''

def fetch_book_data_goodreads(title, author):
    """Scrape book metadata from Goodreads."""
    try:
        search_url = f"https://www.goodreads.com/search?q={quote(title)}+{quote(author)}&search_type=books"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        genre = 'Fiction'  # Placeholder logic
        image_url = ''  # Placeholder logic
        return genre, ['Fiction', 'Adventure'], image_url
    except Exception as e:
        logger.error(f"Goodreads Error: {e}")
        return 'Unknown', [], ''

def fetch_book_data_general_search(title, author):
    """General search for book metadata."""
    try:
        search_query = f"{quote(title)} {quote(author)} book genre tags cover image"
        search_url = f"https://www.google.com/search?q={search_query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        genre = 'General'  # Placeholder
        image_url = ''  # Placeholder
        return genre, ['General'], image_url
    except Exception as e:
        logger.error(f"General Search Error: {e}")
        return 'Unknown', [], ''

def scrape_book_data(title, author, website_url=None):
    """Scrape book data from multiple sources."""
    if website_url:
        try:
            response = requests.get(website_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            genre = 'Custom'  # Placeholder
            image_url = ''  # Placeholder
            return genre, ['Custom'], image_url
        except Exception as e:
            logger.error(f"Error scraping provided URL: {e}")
    
    for fetch_function in [fetch_book_data_open_library, fetch_book_data_goodreads, fetch_book_data_general_search]:
        genre, tags, image_url = fetch_function(title, author)
        if genre != 'Unknown' or image_url:
            return genre, tags, image_url

    return 'Unknown', [], ''
