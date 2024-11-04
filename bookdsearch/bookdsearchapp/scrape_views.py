from django.views.decorators.csrf import csrf_exempt
from .scraping_utils import scrape_book_data
import logging
from django.http import JsonResponse
import traceback

logger = logging.getLogger(__name__)

@csrf_exempt
def scrape_data(request):
    if request.method == 'POST':
        try:
            book_data = request.POST.getlist('book_data[]')
            scraped_data = []

            for book in book_data:
                # Split only at the first occurrence of '|'
                parts = book.split('|', 1)
                if len(parts) != 2:
                    raise ValueError(f"Invalid book data format: {book}")
                title, author = parts
                genre, tags, image_url = scrape_book_data(title, author)
                scraped_data.append({
                    'title': title,
                    'author': author,
                    'genre': genre,
                    'tags': ', '.join(tags),
                    'image_url': image_url
                })

            return JsonResponse({'scraped_data': scraped_data})
        except Exception as e:
            logger.error(f"Error scraping data: {e}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': f'An error occurred while scraping the data: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
