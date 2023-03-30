import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)


# S3 resource
s3_resource = boto3.resource(
    's3',
    endpoint_url='https://django-video.s3.ir-thr-at1.arvanstorage.ir',
    aws_access_key_id='4b742de1-1a24-4840-8780-a6b64c8d976e',
    aws_secret_access_key='956f1099eacb79723f9a2b97d56a68208bf3ae8e'
)

try:
    bucket_name = 'django-video'
    bucket = s3_resource.Bucket(bucket_name)
    print(bucket.objects.all())
    # print(type(bucket.objects.all()))


    for obj in bucket.objects.all():
        print('test')
        # logging.info(f"object_name: {obj.key}, last_modified: {obj.last_modified}")

except ClientError as e:
    logging.error(e)



