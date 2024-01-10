from os import environ, path, getcwd
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import boto3

load_dotenv(path.join(getcwd(), '.env'))

SECRET_KEY = environ.get('SECRET_KEY')
DB_URI = environ.get('DB_URI')
F_END = environ.get('F_END')
PRODUCTION = int(environ.get('PRODUCTION'))
MONGO_URL = environ.get('MONGODB_URI')
MONGODB_NAME = environ.get('MONGODB_NAME')
MONGO_COLLECTION = environ.get('MONGODB_COLLECTION')
WSOCKET_TOKEN = "platform-uqid b88772783831487a7a6456b495e6005e7fcf14500c0bf9f1af09ec132846f5e13b1da0b5bc64de6a1e85e5ad3f4d80ce5a1b2edb9832b40e2865c8d38c9e06d3"
COMPANY = environ.get('COMPANY')
SOCKET_URI = environ.get('SOCKET_URI')
db = SQLAlchemy()

S3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id="AKIAZFX75JLG3FOUJE5C",
    aws_secret_access_key="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"
)

Upload_Buket =  S3.Bucket('test-2023-durbin')

s3_client = boto3.client(
            "s3",
            aws_access_key_id="AKIAZFX75JLG3FOUJE5C",
            aws_secret_access_key="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",
)
bucket = "test-2023-durbin"
def get_file(item=None):       
    try:
        if item:    
            presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket, "Key": item},
                    ExpiresIn=100000,
                )
            # print(presigned_url)
            return presigned_url
        else:
            raise Exception("pass somthing")
    except Exception as e:
            raise Exception(e)