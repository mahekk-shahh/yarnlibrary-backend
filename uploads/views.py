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
    print('unique file name', unique_file_name)

    url = generate_presigned_url(unique_file_name, file_type)
    print('presigned url', url)

    upload_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{unique_file_name}"
    print('upload url', upload_url)

    return Response({'upload_url': url, 'file_url': unique_file_name})
