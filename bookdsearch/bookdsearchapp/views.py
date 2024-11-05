# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
# from .forms import UploadFileForm
# import logging
# from django.views.decorators.csrf import csrf_exempt
# from .scraping_utils import scrape_book_data
# traceback
# import traceback
# import pandas as pd

# logger = logging.getLogger(__name__)

# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Handle file upload here
#             pass
#     else:
#         form = UploadFileForm()
#     return render(request, 'bookdsearchapp/upload.html', {'form': form})


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import UploadFileForm
import logging
from django.views.decorators.csrf import csrf_exempt
from .scraping_utils import scrape_book_data
import traceback
import pandas as pd

logger = logging.getLogger(__name__)

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Read and process the uploaded Excel file
                excel_file = request.FILES['file']
                df = pd.read_excel(excel_file)

                # Extract book data
                book_data = []
                website_url = request.POST.get('website_url', '')

                for _, row in df.iterrows():
                    title = row.get('Title', '').strip()
                    author = row.get('Author', '').strip()

                    if title and author:
                        genre, tags, image_url = scrape_book_data(title, author, website_url)
                        book_data.append({
                            'title': title,
                            'author': author,
                            'genre': genre,
                            'tags': ', '.join(tags),
                            'image_url': image_url
                        })

                # Render the results
                return render(request, 'bookdsearchapp/results.html', {'book_data': book_data})
            except Exception as e:
                logger.error(f"Error processing uploaded file: {e}")
                logger.error(traceback.format_exc())
                return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        form = UploadFileForm()
    return render(request, 'bookdsearchapp/upload.html', {'form': form})
