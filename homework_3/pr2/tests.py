from minio import Minio
from minio.error import S3Error
import pytest
from main import MinIOClient
import os

@pytest.fixture
def minio_client():
    return MinIOClient(
        "play.min.io",
        os.getenv("MINIO_ACCESS_KEY", "Q3AM3UQ867SPQQA43P2F"),
        os.getenv("MINIO_SECRET_KEY", "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"),
        secure=True
    )

@pytest.fixture
def test_bucket(minio_client):
    bucket_name = "test-bucket"
    minio_client.make_bucket(bucket_name)
    yield bucket_name
    
    # Remove all objects and delete the bucket
    objects = minio_client.client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        minio_client.client.remove_object(bucket_name, obj.object_name)
    minio_client.client.remove_bucket(bucket_name)

def test_make_bucket(minio_client):
    bucket_name = "test-make-bucket"
    minio_client.make_bucket(bucket_name)
    assert minio_client.client.bucket_exists(bucket_name)
    minio_client.client.remove_bucket(bucket_name)

def test_upload_and_download_file(minio_client, test_bucket, tmp_path):
    # Create a temporary file
    source_file = tmp_path / "test_file.txt"
    source_file.write_text("Hello, MinIO!")
    
    # Upload the file
    minio_client.upload_file(test_bucket, "test_file.txt", str(source_file))
    
    # Download the file
    destination_file = tmp_path / "downloaded_file.txt"
    minio_client.download_file(test_bucket, "test_file.txt", str(destination_file))
    
    # Check if the file is downloaded correctly
    assert destination_file.read_text() == "Hello, MinIO!"

def test_delete_file(minio_client, test_bucket, tmp_path):
    # Create and upload a file
    source_file = tmp_path / "to_delete.txt"
    source_file.write_text("Delete me")
    minio_client.upload_file(test_bucket, "to_delete.txt", str(source_file))
    
    # Delete the file
    minio_client.delete_file(test_bucket, "to_delete.txt")
    
    # Check if the file is deleted
    objects = list(minio_client.client.list_objects(test_bucket))
    assert not any(obj.object_name == "to_delete.txt" for obj in objects)

def test_list_files(minio_client, test_bucket, tmp_path):
    # Create and upload multiple files
    for i in range(3):
        source_file = tmp_path / f"file_{i}.txt"
        source_file.write_text(f"Content {i}")
        minio_client.upload_file(test_bucket, f"file_{i}.txt", str(source_file))
    
    # Capture the printed output
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    minio_client.list_files(test_bucket)
    
    sys.stdout = sys.__stdout__  # Reset redirect
    
    # Check if all files are listed
    output = captured_output.getvalue()
    assert "file_0.txt" in output
    assert "file_1.txt" in output
    assert "file_2.txt" in output

def test_error_handling(minio_client):
    with pytest.raises(S3Error):
        minio_client.download_file("non-existent-bucket", "non-existent-file.txt", "output.txt")

if __name__ == "__main__":
    pytest.main([__file__])

