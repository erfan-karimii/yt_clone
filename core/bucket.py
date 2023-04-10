import boto3
from django.conf import settings


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
        bucket = self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        return bucket.objects.all()

    def delete_object(self,object_name):
        bucket = self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        object = bucket.Object(object_name)
        object.delete()
        return True
    
    def download_object(self,object_name):
        bucket = self.s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        download_path =  settings.AWS_LOCAL_STORAGE +  object_name
        bucket.download_file(
            object_name,
            download_path
        )
        return True

bucket = Bucket()