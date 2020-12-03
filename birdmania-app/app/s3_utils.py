import boto3

s3 = boto3.client(
   "s3"
)
def upload_file_to_s3(file, bucket_name, object_name):
    try:
        s3.upload_file(
            file,
            bucket_name,
            object_name
        )
    except Exception as e:
        print("Something Happened: ", e)