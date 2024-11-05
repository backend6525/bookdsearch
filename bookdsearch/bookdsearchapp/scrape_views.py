
# from django.views.decorators.csrf import csrf_exempt
# from .scraping_utils import scrape_book_data
# import logging
# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
# import traceback
# import pandas as pd

# logger = logging.getLogger(__name__)

# @csrf_exempt
# def scrape_data(request):
#     if request.method == 'POST':
#         try:
#             book_data = request.POST.getlist('book_data[]')
#             website_url = request.POST.get('website_url')
#             scraped_data = []

#             def stream():
#                 for book in book_data:
#                     try:
#                         parts = book.split('|', 1)
#                         if len(parts) != 2:
#                             raise ValueError(f"Invalid book data format: {book}")
#                         title, author = parts
#                         for genre, tags, image_url in scrape_book_data(title, author, website_url):
#                             yield f"Title: {title}, Author: {author}, Genre: {genre}, Tags: {', '.join(tags)}, Image URL: {image_url}\n"
#                     except Exception as e:
#                         logger.error(f"Error processing book data: {e}")
#                         logger.error(traceback.format_exc())
#                         yield f"Error: An error occurred while processing the book data: {str(e)}\n"

#             return StreamingHttpResponse(stream(), content_type="text/plain")
#         except Exception as e:
#             logger.error(f"Error scraping data: {e}")
#             logger.error(traceback.format_exc())
#             return JsonResponse({'error': f'An error occurred while scraping the data: {str(e)}'}, status=500)
#     return JsonResponse({'error': 'Invalid request method.'}, status=400)

# @csrf_exempt
# def save_data(request):
#     if request.method == 'POST':
#         try:
#             scraped_data = request.POST.getlist('scraped_data[]')
#             data = []

#             for book in scraped_data:
#                 parts = book.split('|', 4)
#                 if len(parts) != 5:
#                     raise ValueError(f"Invalid scraped data format: {book}")
#                 title, author, genre, tags, image_url = parts
#                 data.append({
#                     'Title': title,
#                     'Author': author,
#                     'Genre': genre,
#                     'Tags': tags,
#                     'Image URL': image_url
#                 })

#             df = pd.DataFrame(data)
#             response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename=scraped_data.xlsx'
#             df.to_excel(response, index=False, engine='openpyxl')

#             return response
#         except Exception as e:
#             logger.error(f"Error saving data: {e}")
#             logger.error(traceback.format_exc())
#             return JsonResponse({'error': f'An error occurred while saving the data: {str(e)}'}, status=500)
#     return JsonResponse({'error': 'Invalid request method.'}, status=400)


from django.views.decorators.csrf import csrf_exempt
from .scraping_utils import scrape_book_data
import logging
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse,HttpResponse
import traceback
import pandas as pd

logger = logging.getLogger(__name__)

@csrf_exempt
# def scrape_data(request):
#     if request.method == 'POST':
#         try:
#             book_data = request.POST.getlist('book_data[]')
#             website_url = request.POST.get('website_url')
#             scraped_data = []

#             def stream():
#                 for book in book_data:
#                     try:
#                         parts = book.split('|', 1)
#                         if len(parts) != 2:
#                             raise ValueError(f"Invalid book data format: {book}")
#                         title, author = parts
#                         genre, tags, image_url = scrape_book_data(title, author, website_url)
#                         yield f"Title: {title}, Author: {author}, Genre: {genre}, Tags: {', '.join(tags)}, Image URL: {image_url}\n"
#                     except Exception as e:
#                         logger.error(f"Error processing book data: {e}")
#                         logger.error(traceback.format_exc())
#                         yield f"Error: An error occurred while processing the book data: {str(e)}\n"

#             return StreamingHttpResponse(stream(), content_type="text/plain")
#         except Exception as e:
#             logger.error(f"Error scraping data: {e}")
#             logger.error(traceback.format_exc())
#             return JsonResponse({'error': f'An error occurred while scraping the data: {str(e)}'}, status=500)
#     return JsonResponse({'error': 'Invalid request method.'}, status=400)





def scrape_data(request):
    if request.method == 'POST':
        try:
            book_data = request.POST.getlist('book_data[]')
            website_url = request.POST.get('website_url')
            scraped_results = []

            for book in book_data:
                try:
                    parts = book.split('|', 1)
                    if len(parts) != 2:
                        raise ValueError(f"Invalid book data format: {book}")
                    title, author = parts
                    genre, tags, image_url = scrape_book_data(title, author, website_url)
                    scraped_results.append({
                        'title': title,
                        'author': author,
                        'genre': genre,
                        'tags': ', '.join(tags),
                        'image_url': image_url
                    })
                except Exception as e:
                    logger.error(f"Error processing book data: {e}")
                    logger.error(traceback.format_exc())
                    scraped_results.append({
                        'title': book.split('|', 1)[0],
                        'author': book.split('|', 1)[1] if len(book.split('|', 1)) > 1 else '',
                        'error': str(e)
                    })

            # Return the scraped results as JSON
            return JsonResponse({'scraped_data': scraped_results})

        except Exception as e:
            logger.error(f"Error scraping data: {e}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': f'An error occurred while scraping the data: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


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
