import boto3
from django.conf import settings
import logging 
from botocore.exceptions import ClientError
# Configure logging
logging.basicConfig(level=logging.INFO)



class Bucket:
    """CDN Bucket manager
    init method creates connection.
    """

    def __init__(self):
        self.s3_resource = boto3.resource(
            settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def get_objects(self):
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        bucket = self.s3_resource.Bucket(bucket_name)
        return bucket.objects.all()

    def delete_object(self,object_name):
        bucket = self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        object = bucket.Object(object_name)
        object.delete()
        return True

bucket = Bucket()