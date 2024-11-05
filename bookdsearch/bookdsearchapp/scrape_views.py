from django.views.decorators.csrf import csrf_exempt
from .scraping_utils import scrape_book_data
import logging
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse,HttpResponse
import traceback
import pandas as pd
import json
import time
logger = logging.getLogger(__name__)



def scrape_data(request):
    if request.method == 'POST':
        try:
            book_data = request.POST.getlist('book_data[]')
            website_url = request.POST.get('website_url')

            def stream():
                for book in book_data:
                    try:
                        parts = book.split('|', 1)
                        if len(parts) != 2:
                            yield json.dumps({'error': f'Invalid book data format: {book}'})
                            continue
                        
                        title, author = parts
                        genre, tags, image_url = scrape_book_data(title, author, website_url)
                        
                        yield json.dumps({
                            'title': title,
                            'author': author,
                            'genre': genre,
                            'tags': tags,
                            'image_url': image_url
                        })
                    except Exception as e:
                        logger.error(f"Error processing book data: {e}")
                        logger.error(traceback.format_exc())
                        yield json.dumps({
                            'title': book.split('|', 1)[0],
                            'author': book.split('|', 1)[1] if len(book.split('|', 1)) > 1 else '',
                            'error': str(e)
                        })

            return StreamingHttpResponse(stream(), content_type="application/json")
        except Exception as e:
            logger.error(f"Error scraping data: {e}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': f'An error occurred while scraping the data: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



# @csrf_exempt
# def scrape_data(request):
#     if request.method == 'POST':
#         try:
#             book_data = request.POST.getlist('book_data[]')
#             website_url = request.POST.get('website_url')
#             batch_size = 10  # Number of books to process in each batch

#             def stream():
#                 for i in range(0, len(book_data), batch_size):
#                     batch = book_data[i:i + batch_size]
#                     batch_results = []

#                     for book in batch:
#                         try:
#                             parts = book.split('|', 1)
#                             if len(parts) != 2:
#                                 batch_results.append({'error': f'Invalid book data format: {book}'})
#                                 continue

#                             title, author = parts
#                             genre, tags, image_url = scrape_book_data(title, author, website_url)

#                             batch_results.append({
#                                 'title': title,
#                                 'author': author,
#                                 'genre': genre,
#                                 'tags': tags,
#                                 'image_url': image_url
#                             })
#                         except Exception as e:
#                             logger.error(f"Error processing book data: {e}")
#                             logger.error(traceback.format_exc())
#                             batch_results.append({
#                                 'title': book.split('|', 1)[0],
#                                 'author': book.split('|', 1)[1] if len(book.split('|', 1)) > 1 else '',
#                                 'error': str(e)
#                             })

#                     yield json.dumps(batch_results) + '\n'  # Ensure each batch is followed by a newline
#                     time.sleep(1)  # Sleep to manage load and memory usage

#             return StreamingHttpResponse(stream(), content_type="application/json")
#         except Exception as e:
#             logger.error(f"Error scraping data: {e}")
#             logger.error(traceback.format_exc())
#             return JsonResponse({'error': f'An error occurred while scraping the data: {str(e)}'}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=400)



@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        try:
            scraped_data = request.POST.getlist('scraped_data[]')
            data = []

            for book in scraped_data:
                parts = book.split('|', 4)
                if len(parts) != 5:
                    raise ValueError(f"Invalid scraped data format: {book}")
                title, author, genre, tags, image_url = parts
                data.append({
                    'Title': title,
                    'Author': author,
                    'Genre': genre,
                    'Tags': tags,
                    'Image URL': image_url
                })

            df = pd.DataFrame(data)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=scraped_data.xlsx'
            df.to_excel(response, index=False, engine='openpyxl')

            return response
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': f'An error occurred while saving the data: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
