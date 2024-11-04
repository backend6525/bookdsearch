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

def fetch_book_data_general_search(title, author):
    """Perform a general web search to fetch book metadata."""
    try:
        search_query = f"{title} {author} book genre tags cover image"
        search_url = f"https://www.google.com/search?q={search_query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example parsing logic (this will need to be adapted based on actual search results)
        genre = 'Unknown'  # Placeholder; actual parsing needed
        tags = ['Unknown']  # Placeholder; actual parsing needed
        image_url = ''  # Placeholder; actual parsing needed
        # More detailed parsing here...

        return genre, tags, image_url
    except Exception as e:
        print(f"General Search Error: {e}")
        return 'Unknown', [], ''

def scrape_book_data(title, author):
    """Attempt to scrape book data from multiple sources."""
    # Priority order: Open Library -> Goodreads -> General Web Search
    for fetch_function in [fetch_book_data_open_library, fetch_book_data_goodreads, fetch_book_data_general_search]:
        genre, tags, image_url = fetch_function(title, author)
        if genre != 'Unknown' and image_url:  # Check if valid data is returned
            return genre, tags, image_url
        time.sleep(1)  # Respect rate limits between requests
    return 'Unknown', [], ''  # Default return if all sources fail
