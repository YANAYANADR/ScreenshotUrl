import os
import random
import io
from minio import Minio
# from minio.error import S3Error
import logging

# import web as w


# logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Minio connection
try:
    client = Minio("minio:9000",
                   access_key=os.environ["MINIO_KEY"],
                   secret_key=os.environ["MINIO_SECRET"], secure=False
                   )
    # client = Minio("minio:9000",
    #                access_key='F5OqGvkU1mZCzfUr',
    #                secret_key='C5BImJ4b8GKXbLfQ2QzScmN57hTYIGhD',
    #                secure=False
    #                )
except:
    log.critical('MINIO ERROR')
bucket_name = "images"


def input_file(data):
    # Create client
    # file
    file = ''.join([str(random.randint(0, 9)) for n in range(6)]) + '.png'
    log.info(f'Name decided: {file}')
    data = io.BytesIO(data)
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        log.info('Created bucket ')
    else:
        log.info('Bucket exists')

    # upload
    client.put_object(bucket_name, object_name=file,
                      data=data, length=-1, part_size=5242880)
    log.info('Image upload finished')
    return file


def delete_file(path):
    pass


def get_file(path):
    return client.get_object(bucket_name, object_name=path).read()

# if __name__ == '__main__':
#     print(get_file('108880.png'))
