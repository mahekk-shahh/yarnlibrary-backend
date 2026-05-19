from datetime import datetime

from django.conf import settings
from .utils import generate_presigned_url
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def get_presigned_url(request):
    file_name = request.data.get('file_name')
    file_type = request.data.get('file_type')
    folder = request.data.get('folder')

    unique_file_name = f"{folder}/{file_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    url = generate_presigned_url(unique_file_name, file_type)

    return Response({'upload_url': url, 'file_url': unique_file_name})
