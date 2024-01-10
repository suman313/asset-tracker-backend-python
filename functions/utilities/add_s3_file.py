from config import Upload_Buket
from werkzeug.utils import secure_filename
import time
import os

def add_s3_file(s3_file=None, type_of_file=None):
    try:
        if s3_file and type_of_file is None:
            return "params are needed to upload"
        filename =  f"{type_of_file}" + str(int(time.time())) + s3_file.filename
        filename_at_s3 = f'{type_of_file}/'+ filename
        filepath = os.getcwd() + f"/resoure/{type_of_file}/" + secure_filename(filename)
        s3_file.save(filepath)
        Upload_Buket.upload_file( filepath ,  filename_at_s3)
        urls = "test-2023-durbin" + ".s3.amazonaws.com/" + filename_at_s3
        os.remove(filepath)
        # print(urls)
        return urls
    except Exception as e:
        raise e

def remove_s3_file(filename):
    try:
        # Upload_Buket.delete(key=filename)
        return "not working "
    except Exception as e:
        raise e