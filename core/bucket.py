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

    # def __init__(self):
    #     # session = boto3.Session()
    #     self.conn = boto3.client(
    #         settings.AWS_SERVICE_NAME,
    #         endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    #     )

    def get_objects(self):
        print(settings.AWS_STORAGE_BUCKET_NAME)
        try:
            # S3 resource
            s3_resource = boto3.resource(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        except Exception as exc:
            logging.error(exc)
        else:
            try:
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                bucket = s3_resource.Bucket(bucket_name)

                for obj in bucket.objects.all():
                    logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")

            except ClientError as e:
                logging.error(e)

bucket = Bucket()