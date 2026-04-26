import boto3
from django.conf import settings

def generate_presigned_url(file_name, file_type):
    s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    try:
        response = s3.generate_presigned_url('put_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_name, 'ContentType': file_type}, ExpiresIn=3600)
    except Exception as error:
        print('errorrrrrrr', error)
        return None

    return response


def get_file_url(file_path):
    s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    url = s3.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file_path}, ExpiresIn=3600)
    
    return url