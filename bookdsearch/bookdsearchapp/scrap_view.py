from django.views.decorators.csrf import csrf_exempt
from .scraping_utils import scrape_book_data
import pandas as pd
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
                title, author = book.split('|')
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
            return JsonResponse({'error': 'An error occurred while scraping the data.'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
