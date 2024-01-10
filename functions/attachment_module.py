from config import db 
from models.attachment import Attachment
from functions.utilities.add_s3_file import add_s3_file

def add_attachment(attachment, data=None):
    try:
        new_attachment = {}
        if data is None:
            return "plese send data parameter"
        link = add_s3_file(attachment, "attachment")
        if data["types_section"] == "asset":
               new_attachment = Attachment(    
                    serial_no = data["serial_no"],
                    types = data["doc_types"],
                    doc_uri = link,
                    doc_expiry_date = data["doc_expiry_date"],
                    archive_flag = False,
                    asset_id = data["asset_id"]
                    )
        elif data["types_section"] == "lease":
               new_attachment = Attachment(    
                    serial_no = data["serial_no"],
                    types = data["doc_types"],
                    doc_uri = link,
                    doc_expiry_date = data["doc_expiry_date"],
                    archive_flag = False,
                    lease_id = data["lease_id"]
                    )
        elif data["types_section"] == "maintenance":
                new_attachment = Attachment(    
                    serial_no = data["serial_no"],
                    types = data["doc_types"],
                    doc_uri = link,
                    doc_expiry_date = data["doc_expiry_date"],
                    archive_flag = False,
                    maintenance_id = data["maintenance_id"]
                    )
        
        db.session.add(new_attachment)
        db.session.commit()
        return new_attachment
    except Exception as e:
        raise e


def remove_attachment(id):
     try:
          attachments = Attachment.query.filter_by(id=id).first()
          print(attachments)
          filename = attachments.doc_uri.split("/")[1] + "/" + attachments.doc_uri.split("/")[2] 
          db.session.delete(attachments)
          db.session.commit()
        #   print(filename)
        #   remove_s3_file(filename)
          return attachments
     except Exception :
          raise Exception("id not found")


def update_attachment(data):
     try:
          attachment = Attachment.query.filter_by(id=data["id"]).first()
          attachment.serial_no = data.get("serial_no") or attachment.serial_no  
          attachment.types = data.get("types") or attachment.types 
          attachment.doc_uri = data.get("doc_uri") or attachment.doc_uri 
          attachment.doc_expiry_date = data.get("doc_expiry_date") or attachment.doc_expiry_date 
          attachment.asset_id = data.get("asset_id") or attachment.asset_id 
          attachment.lease_id = data.get("lease_id") or attachment.lease_id 
          attachment.maintenance_id = data.get("maintenance_id") or attachment.maintenance_id 
          if attachment.archive_flag is not None:
               attachment.archive_flag = data.get("archive_flag") 
          db.session.commit()
          return {
               "id": attachment.id,
               "serial_no": attachment.serial_no,
               "types": attachment.types,
               "doc_uri": attachment.doc_uri,
               "doc_expiry_date": attachment.doc_expiry_date
          }
     except Exception as e:
          raise Exception("Please check all fildes")