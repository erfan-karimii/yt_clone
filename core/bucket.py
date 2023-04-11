import boto3
from django.conf import settings


class Bucket:
    """CDN Bucket manager
    init method creates connection.
    """

    def __init__(self):
        s3_resource = boto3.resource(
            settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


    def get_objects(self):
        return self.bucket.objects.all()

    def delete_object(self,object_name):
        object = self.bucket.Object(object_name)
        object.delete()
        return True
    
    def download_object(self,object_name):
        download_path =  settings.AWS_LOCAL_STORAGE +  object_name
        self.bucket.download_file(
            object_name,
            download_path
        )
        return True
    
    # def upload_object(self,object_name,file_path):
    #     with open(file_path, "rb") as file:
    #         self.bucket.put_object(
    #             ACL='private',
    #             Body=file,
    #             Key=object_name
    #         )
    #     return True

bucket = Bucket()