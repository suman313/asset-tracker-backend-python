from config import db
from models.commercial_details import CommercialDetail


def create_details(data):
        try:
            asset_id = data.get("asset_id")
            get_new_commercial_detail = CommercialDetail.query.filter_by(asset_id=asset_id).first()
            if get_new_commercial_detail == None:
                new_commercial_detail =  CommercialDetail(
                        purchase_order_no = data.get("purchase_order_no") or "", 
                        purchase_order_date = data.get("purchase_order_date") or "", 
                        invoice_no = data.get("invoice_no") or "", 
                        invoice_date = data.get("invoice_date") or "", 
                        payment_terms = data.get("payment_terms") or "", 
                        amount_rem_to_oem = data.get("amount_rem_to_oem") or "", 
                        date_of_rem_to_oem = data.get("date_of_rem_to_oem") or "", 
                        exchange_rate_rem = data.get("exchange_rate_rem") or "", 
                        custom_duty_payment = data.get("custom_duty_payment") or "", 
                        exworks_price = data.get("exworks_price") or "", 
                        cif_charges = data.get("cif_charges") or "", 
                        total_cost = data.get("total_cost") or "", 
                        boe_no = data.get("boe_no") or "", 
                        custom_duty_value = data.get("custom_duty_value") or "", 
                        gst_amount = data.get("gst_amount") or "", 
                        exrate_boe = data.get("exrate_boe") or "", 
                        clearing_charges = data.get("clearing_charges") or "", 
                        cha_charges = data.get("cha_charges") or "", 
                        transportation_charges = data.get("transportation_charges") or "", 
                        port_of_dispatch = data.get("port_of_dispatch") or "", 
                        port_of_clearance = data.get("port_of_clearance") or "", 
                        period_of_insurance = data.get("period_of_insurance") or "", 
                        insurance_renewal = data.get("insurance_renewal") or "", 
                        total_landed_cost = data.get("total_landed_cost") or "", 
                        total_landed_cost_with_gst = data.get("total_landed_cost_with_gst") or "", 
                        asset_id = data.get("asset_id")
                )

                db.session.add(new_commercial_detail)
                db.session.commit()
            else:
                   raise Exception("one commercial_detail already exists")
            return new_commercial_detail
        except Exception as e:
            print(e)
            raise e
        


def update_details(data):
            try: 
                    commercial_detail = CommercialDetail.query.filter_by(asset_id= data.get("asset_id")).first()
                    if commercial_detail:
                        commercial_detail.purchase_order_no = data.get("purchase_order_no") or commercial_detail.purchase_order_no or "nill"
                        commercial_detail.purchase_order_date = data.get("purchase_order_date") or commercial_detail.purchase_order_date or "nill"
                        commercial_detail.invoice_no = data.get("invoice_no") or commercial_detail.invoice_no or "nill"
                        commercial_detail.invoice_date = data.get("invoice_date") or commercial_detail.invoice_date or "nill"
                        commercial_detail.payment_terms = data.get("payment_terms") or commercial_detail.payment_terms or "nill"
                        commercial_detail.amount_rem_to_oem = data.get("amount_rem_to_oem") or commercial_detail.amount_rem_to_oem or "nill"
                        commercial_detail.date_of_rem_to_oem = data.get("date_of_rem_to_oem") or commercial_detail.date_of_rem_to_oem or "nill"
                        commercial_detail.exchange_rate_rem = data.get("exchange_rate_rem") or commercial_detail.exchange_rate_rem or "nill"
                        commercial_detail.custom_duty_payment = data.get("custom_duty_payment") or commercial_detail.custom_duty_payment or "nill"
                        commercial_detail.exworks_price = data.get("exworks_price") or commercial_detail.exworks_price or "nill"
                        commercial_detail.cif_charges = data.get("cif_charges") or commercial_detail.cif_charges or "nill"
                        commercial_detail.total_cost = data.get("total_cost") or commercial_detail.total_cost or "nill"
                        commercial_detail.boe_no = data.get("boe_no") or commercial_detail.boe_no or "nill"
                        commercial_detail.custom_duty_value = data.get("custom_duty_value") or commercial_detail.custom_duty_value or "nill"
                        commercial_detail.gst_amount = data.get("gst_amount") or commercial_detail.gst_amount or "nill"
                        commercial_detail.exrate_boe = data.get("exrate_boe") or commercial_detail.exrate_boe or "nill"
                        commercial_detail.clearing_charges = data.get("clearing_charges") or commercial_detail.clearing_charges or "nill"
                        commercial_detail.cha_charges = data.get("cha_charges") or commercial_detail.cha_charges or "nill"
                        commercial_detail.transportation_charges = data.get("transportation_charges") or commercial_detail.transportation_charges or "nill"
                        commercial_detail.port_of_dispatch = data.get("port_of_dispatch") or commercial_detail.port_of_dispatch or "nill"
                        commercial_detail.port_of_clearance = data.get("port_of_clearance") or commercial_detail.port_of_clearance or "nill"
                        commercial_detail.period_of_insurance = data.get("period_of_insurance") or commercial_detail.period_of_insurance or "nill"
                        commercial_detail.insurance_renewal = data.get("insurance_renewal") or commercial_detail.insurance_renewal or "nill"
                        commercial_detail.total_landed_cost = data.get("total_landed_cost") or commercial_detail.total_landed_cost or "nill"
                        commercial_detail.total_landed_cost_with_gst = data.get("total_landed_cost_with_gst") or commercial_detail.total_landed_cost_with_gst or "nill"
                        db.session.commit()
                    else :
                          create_details(data)
                    return {
                           "id": commercial_detail.id,
                           "purchase_order_no": commercial_detail.purchase_order_no,
                           "purchase_order_date": commercial_detail.purchase_order_date,
                           "invoice_no": commercial_detail.invoice_no,
                           "invoice_date": commercial_detail.invoice_date,
                           "payment_terms": commercial_detail.payment_terms,
                           "amount_rem_to_oem": commercial_detail.amount_rem_to_oem,
                           "date_of_rem_to_oem": commercial_detail.date_of_rem_to_oem,
                           "exchange_rate_rem": commercial_detail.exchange_rate_rem,
                           "custom_duty_payment": commercial_detail.custom_duty_payment,
                           "exworks_price": commercial_detail.exworks_price,
                           "cif_charges": commercial_detail.cif_charges,
                           "total_cost": commercial_detail.total_cost,
                           "boe_no": commercial_detail.boe_no,
                           "custom_duty_value": commercial_detail.custom_duty_value,
                           "gst_amount": commercial_detail.gst_amount,
                           "exrate_boe": commercial_detail.exrate_boe,
                           "clearing_charges": commercial_detail.clearing_charges,
                           "cha_charges": commercial_detail.cha_charges,
                           "transportation_charges": commercial_detail.transportation_charges,
                           "port_of_dispatch": commercial_detail.port_of_dispatch,
                           "port_of_clearance": commercial_detail.port_of_clearance,
                           "period_of_insurance": commercial_detail.period_of_insurance,
                           "insurance_renewal": commercial_detail.insurance_renewal,
                           "total_landed_cost": commercial_detail.total_landed_cost,
                           "total_landed_cost_with_gst": commercial_detail.total_landed_cost_with_gst
                   }
            except Exception as e:
                print(e)
                raise e
            

def delete_details(asset_id):
            try: 
                   commercial_detail = CommercialDetail.query.filter_by( asset_id = asset_id).first()
                   if commercial_detail != None:
                            db.session.delete(commercial_detail)
                            db.session.commit()

            except Exception as e:
                print(e)
                raise e
            


def get_details(asset_id):
        try:
                    commercial_detail = CommercialDetail.query.filter_by(asset_id = asset_id).first()
                    if commercial_detail != None:
                         return {
                            "id": commercial_detail.id,
                            "purchase_order_no": commercial_detail.purchase_order_no,
                            "purchase_order_date": commercial_detail.purchase_order_date,
                            "invoice_no": commercial_detail.invoice_no,
                            "invoice_date": commercial_detail.invoice_date,
                            "payment_terms": commercial_detail.payment_terms,
                            "amount_rem_to_oem": commercial_detail.amount_rem_to_oem,
                            "date_of_rem_to_oem": commercial_detail.date_of_rem_to_oem,
                            "exchange_rate_rem": commercial_detail.exchange_rate_rem,
                            "custom_duty_payment": commercial_detail.custom_duty_payment,
                            "exworks_price": commercial_detail.exworks_price,
                            "cif_charges": commercial_detail.cif_charges,
                            "total_cost": commercial_detail.total_cost,
                            "boe_no": commercial_detail.boe_no,
                            "custom_duty_value": commercial_detail.custom_duty_value,
                            "gst_amount": commercial_detail.gst_amount,
                            "exrate_boe": commercial_detail.exrate_boe,
                            "clearing_charges": commercial_detail.clearing_charges,
                            "cha_charges": commercial_detail.cha_charges,
                            "transportation_charges": commercial_detail.transportation_charges,
                            "port_of_dispatch": commercial_detail.port_of_dispatch,
                            "port_of_clearance": commercial_detail.port_of_clearance,
                            "period_of_insurance": commercial_detail.period_of_insurance,
                            "insurance_renewal": commercial_detail.insurance_renewal,
                            "total_landed_cost": commercial_detail.total_landed_cost,
                            "total_landed_cost_with_gst": commercial_detail.total_landed_cost_with_gst
                        }
                    else: 
                           return {}
        except Exception as e:
                print (e)
                raise e