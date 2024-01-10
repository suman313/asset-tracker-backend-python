from config import db 
from models.photo import Photo
from functions.utilities.add_s3_file import add_s3_file , remove_s3_file


def add_photo(image, data=None):
        try:
           link = add_s3_file(image, "photo")
           if data["types"] == "asset":
               new_photo = Photo(image_uri=link, asset_id=data["asset_id"])
           elif data["types"] == "lease":
               new_photo = Photo(image_uri=link, lease_id =data["lease_id"])
           elif data["types"] == "maintenance":
                new_photo = Photo(image_uri=link, maintenance_id=data["maintenance_id"])
           elif data["types"] == "operator":
                new_photo = Photo(image_uri=link, operator_id=data["operator_id"])
           db.session.add(new_photo)
           db.session.commit()
           return new_photo
        except Exception as e:
            print (e)
            raise e


def remove_photo(id):
     print(id)
     try:
          photo = Photo.query.filter_by(id=id).first()
          filename = photo.image_uri.split("/")[1] + "/" + photo.image_uri.split("/")[2] 
          db.session.delete(photo)
          db.session.commit()
          print(filename)
          remove_s3_file(filename)
          return photo
     except Exception as e:
          raise Exception("id not found")
