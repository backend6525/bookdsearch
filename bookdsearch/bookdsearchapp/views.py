from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
import pandas as pd
import logging
import traceback



logger = logging.getLogger(__name__)

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 # Read the uploaded Excel file
#                 excel_file = request.FILES['file']
#                 df = pd.read_excel(excel_file)

#                 # Validate columns
#                 if 'Title' not in df.columns or 'Author' not in df.columns:
#                     return JsonResponse({'error': 'Invalid file format. Columns "Title" and "Author" are required.'}, status=400)

#                 # Extract book titles and authors
#                 book_data = []
#                 for _, row in df.iterrows():
#                     title = row['Title']
#                     author = row['Author']
#                     book_data.append({
#                         'title': title,
#                         'author': author
#                     })

#                 # Pass data to template
#                 return render(request, 'bookdsearchapp/display.html', {'book_data': book_data})
#             except Exception as e:
#                 # Log the full traceback
#                 logger.error(f"Error processing file: {e}")
#                 logger.error(traceback.format_exc())
#                 return JsonResponse({'error': 'An error occurred while processing the file.'}, status=500)
#     else:
#         form = UploadFileForm()
#     return render(request, 'bookdsearchapp/upload.html', {'form': form})


# bookdsearchapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
import pandas as pd
import logging
import traceback

logger = logging.getLogger(__name__)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Read the uploaded Excel file
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
                    book_data.append({
                        'title': title,
                        'author': author
                    })

                # Pass data to template
                return render(request, 'bookdsearchapp/display.html', {'book_data': book_data})
            except Exception as e:
                # Log the full traceback
                logger.error(f"Error processing file: {e}")
                logger.error(traceback.format_exc())
                return JsonResponse({'error': 'An error occurred while processing the file.'}, status=500)
    else:
        form = UploadFileForm()
    return render(request, 'bookdsearchapp/upload.html', {'form': form})
