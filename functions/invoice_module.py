from models.invoice import Invoice
from config import db
from functions.utilities.add_s3_file import add_s3_file


def create_invoice(company_id, data, document):
        try: 
            link = add_s3_file(document, type_of_file="invoice")
            new_invoice = Invoice(
                    invoice_no= data['invoice_no'],
                    invoice_date = data["invoice_date"],
                    invoice_name = data["invoice_name"],
                    operator_name = data["operator_name"],
                    documents_link = link,
                    lease_id = data["lease_id"],
                    company_id = company_id,
            )
            db.session.add(new_invoice)
            db.session.commit()
            return {
                    "id": new_invoice.id,
                    "invoice_no": new_invoice.invoice_no,
                    "invoice_date": new_invoice.invoice_date,
                    "invoice_name": new_invoice.invoice_name,
                    "operator_name": new_invoice.operator_name,
                    "documents_link": new_invoice.documents_link,
                    "lease_id": new_invoice.lease_id,
                    }
        except Exception as e:
                raise e

def get_invoice(company_id, lease_id):
    try:
        list_invoice = []
        if lease_id is None:
              invoices = Invoice.query.filter_by(company_id=company_id).all()
              for invoice in invoices:
                    list_invoice.append({
                    "id": invoice.id,
                    "invoice_no": invoice.invoice_no,
                    "invoice_date": invoice.invoice_date,
                    "invoice_name": invoice.invoice_name,
                    "operator_name": invoice.operator_name,
                    "documents_link": invoice.documents_link,
                    "lease_id": invoice.lease_id,
                    })
        else: 
            invoices = Invoice.query.filter(Invoice.company_id==company_id, Invoice.lease_id==lease_id).all()
            for invoice in invoices:
                    list_invoice.append({
                    "id": invoice.id,
                    "invoice_no": invoice.invoice_no,
                    "invoice_date": invoice.invoice_date,
                    "invoice_name": invoice.invoice_name,
                    "operator_name": invoice.operator_name,
                    "documents_link": invoice.documents_link,
                    "lease_id": invoice.lease_id,
                    })
        return list_invoice
    except Exception as e:
          raise e
def update_invoice(company_id, data):
        try:
                invoice_id = data["id"]
                invoice = Invoice.query.filter_by(company_id=company_id).filter_by(id=invoice_id).first()
                # invoice.id = data.id or  invoice.id
                invoice.invoice_no = data.get("invoice_no") or  invoice.invoice_no
                invoice.invoice_date = data.get("invoice_date") or  invoice.invoice_date
                invoice.invoice_name = data.get("invoice_name") or  invoice.invoice_name
                invoice.operator_name = data.get("operator_name") or  invoice.operator_name
                # invoice.documents_link = data.documents_link or  invoice.documents_link
                # invoice.lease_id = data.lease_id or  invoice.lease_id
                db.session.commit()
                return {
                    "id": invoice.id,
                    "invoice_no": invoice.invoice_no,
                    "invoice_date": invoice.invoice_date,
                    "invoice_name": invoice.invoice_name,
                    "operator_name": invoice.operator_name,
                    "documents_link": invoice.documents_link,
                    "lease_id": invoice.lease_id,
                    }
        except Exception as e:
              raise e


def delete_invoice(company_id, invoice_id):
        try:
                invoice = Invoice.query.filter_by(id = invoice_id).filter_by(company_id = company_id).first()
                db.session.delete(invoice)
                db.session.commit()
                return f"{invoice.id} deleted successfully"
        except Exception as e:
              raise e
        
       