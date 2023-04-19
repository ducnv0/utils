from datetime import timedelta
from io import BytesIO

from minio import Minio
from minio.error import S3Error


class CustomMinio(Minio):
    def __init__(
        self,
        endpoint,
        access_key=None,
        secret_key=None,
        session_token=None,
        secure=True,
        region=None,
        http_client=None,
        credentials=None,
        default_bucket=None,
    ):
        super().__init__(endpoint, access_key, secret_key, session_token, secure, region, http_client, credentials)
        self.default_bucket = default_bucket
            
    def get_object(self, object_name, bucket_name=None, offset=0, length=0, request_headers=None, ssec=None, version_id=None, extra_query_params=None):
        if not bucket_name:
            bucket_name = self.default_bucket
        
        data = None
        try:
            response = super().get_object(bucket_name, object_name, offset, length, request_headers, ssec, version_id, extra_query_params)
            data = response.data
        finally:
            response.close()
            response.release_conn()
        
        return data

    
    def put_object(self, object_name, data, bucket_name=None, length=None, content_type="application/octet-stream", metadata=None, sse=None, progress=None, part_size=0, num_parallel_uploads=3, tags=None, retention=None, legal_hold=False):
        if not bucket_name:
            bucket_name = self.default_bucket
        if isinstance(data, bytes):
            if not length:
                length = len(data)
            data = BytesIO(data)
        if not length:
            length = len(data.read())

        return super().put_object(bucket_name, object_name, data, length, content_type, metadata, sse, progress, part_size, num_parallel_uploads, tags, retention, legal_hold)

    def fget_object(self, object_name, file_path, bucket_name=None, request_headers=None, ssec=None, version_id=None, extra_query_params=None, tmp_file_path=None, progress=None):
        if not bucket_name:
            bucket_name = self.default_bucket
        return super().fget_object(bucket_name, object_name, file_path, request_headers, ssec, version_id, extra_query_params, tmp_file_path, progress)
    
    def fput_object(self, object_name, file_path, bucket_name=None, content_type="application/octet-stream", metadata=None, sse=None, progress=None, part_size=0, num_parallel_uploads=3, tags=None, retention=None, legal_hold=False):
        if not bucket_name:
            bucket_name = self.default_bucket
        return super().fput_object(bucket_name, object_name, file_path, content_type, metadata, sse, progress, part_size, num_parallel_uploads, tags, retention, legal_hold)

    def presigned_get_object(self, object_name, bucket_name=None, expires=timedelta(days=7), response_headers=None, request_date=None, version_id=None, extra_query_params=None):
        if not bucket_name:
            bucket_name = self.default_bucket
        return super().presigned_get_object(bucket_name, object_name, expires, response_headers, request_date, version_id, extra_query_params)
    
    def presigned_put_object(self, object_name, bucket_name=None, expires=timedelta(days=7)):
        if not bucket_name:
            bucket_name = self.default_bucket
        return super().presigned_put_object(bucket_name, object_name, expires)
    
    def create_default_bucket(self):
        if not self.bucket_exists(self.default_bucket):
            self.make_bucket(self.default_bucket)

    def object_exists(self, object_name, bucket_name=None):
        exists = False
        if not bucket_name:
            bucket_name = self.default_bucket
        try:
            stat = self.stat_object(bucket_name=bucket_name, object_name=object_name)
            exists = True
        except S3Error as ex:
            pass
        finally:
            pass
            
        return exists
