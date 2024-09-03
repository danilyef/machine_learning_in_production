'''
Before starting the script, create a virtual environment:

1. cd /path/to/your/project
2. python -m venv env
3. source env/bin/activate
4. pip install -r requirements.txt

After these steps start script from cmd:
5. python main.py
'''


from minio import Minio
from minio.error import S3Error
import io
import os


class MinIOClient:
    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )


    def make_bucket(self, bucket_name):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")

    def upload_file(self, bucket_name, destination_file, source_file):
        self.client.fput_object(bucket_name, destination_file, source_file)
        print(f"File '{source_file}' uploaded to bucket '{bucket_name}' as '{destination_file}'.")

    def download_file(self, bucket_name, source_file, destination_file):
        self.client.fget_object(bucket_name, source_file, destination_file)
        print(f"File '{source_file}' downloaded to '{destination_file}'.")

    def delete_file(self, bucket_name, file_name):
        self.client.remove_object(bucket_name, file_name)
        print(f"File '{file_name}' deleted from bucket '{bucket_name}'.")

    def list_files(self, bucket_name):
        files = self.client.list_objects(bucket_name)
        for file in files:
            print(file.object_name)



if __name__ == "__main__":
    client = MinIOClient(
        endpoint="play.min.io",
        access_key=os.getenv("MINIO_ACCESS_KEY", "Q3AM3UQ867SPQQA43P2F"),  
        secret_key=os.getenv("MINIO_SECRET_KEY", "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"), 
        secure=True
    )

    client.make_bucket("my-bucket")
    print("-"*10)
    client.upload_file("my-bucket", "hello.txt", "hello.txt")
    print("-"*10)
    client.list_files("my-bucket")
    print("-"*10)
    client.download_file("my-bucket", "hello.txt", "hello.txt")
    print("-"*10)
    client.list_files("my-bucket")
    print("-"*10)
    client.delete_file("my-bucket", "hello.txt")
    print("-"*10)
    client.list_files("my-bucket")

    
