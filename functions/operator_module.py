from config import db
from models.operator import Operator
from models.phone import Phone
from models.bank_details import BankDetails
from models.photo import Photo

def create_operator(data=None, company_id=None):
    try:
        new_operator = Operator(
            name=data.get("name"),
            aadhar_no=data.get("aadhar_no"),
            joining_date=data.get("joining_date"),
            termination_date=data.get("termination_date"),
            net_inhand_salary=data.get("net_inhand_salary"),
            pf_account_no=data.get("pf_account_no"),
            company_id=company_id,
        )
        db.session.add(new_operator)
        db.session.commit()
        Operator_id = new_operator.id
        new_phone = Phone(
            phone_no=data.get("phone_no"),
            types=data.get("phone_code"),
            operator_id=Operator_id,
        )
        db.session.add(new_phone)
        new_bank_details = BankDetails(
            ifsc_code=data.get("ifsc_code"),
            account_no=data.get("account_no"),
            operator_id=Operator_id,
        )
        db.session.add(new_bank_details)
        db.session.commit()
        return {
            "id": new_operator.id,
            "joining_date": new_operator.joining_date,
            "name": new_operator.name,
            "aadhar_no": new_operator.aadhar_no,
            "phone": {
                "id": new_phone.id,
                "phone_no": new_phone.phone_no,
                "types": new_phone.types,
            },
            "bank_details": {
                "id": new_bank_details.id,
                "ifsc_code": new_bank_details.ifsc_code,
                "account_no": new_bank_details.account_no,
            },
        }
    except Exception as e:
        # print(e)
        raise e


def get_operator_list(company_id=None, limit=None, offset=None, aadhar_no=None, name=None, pf_account=None):
    try:
        operators = None
        if company_id:
            operators = Operator.query.with_entities(
                Operator.id,
                Operator.joining_date,
                Operator.pf_account_no,
                Operator.name,
                Operator.aadhar_no,
                Operator.termination_date
            ).filter_by(company_id=company_id)
        else:
            raise Exception("you must provide company_id")
        if aadhar_no:
            operators = operators.filter(Operator.aadhar_no == aadhar_no)
        elif name:
            operators = operators.filter(Operator.name == name)
        elif pf_account:
            operators = operators.filter(Operator.pf_account_no == pf_account)
        else:
            operators = Operator.query.with_entities(
                Operator.id,
                Operator.joining_date,
                Operator.pf_account_no,
                Operator.name,
                Operator.aadhar_no,
                Operator.termination_date
            )

        data_count = len(operators.all())

        if limit != None and offset != None:
            operators = operators.limit(limit).offset(offset)
        elif limit != None:
            operators = operators.limit(limit)
        else:
            operators = operators.all()

        operator_list = []
        for operator in operators:
            bankDetails = (
                BankDetails.query.with_entities(
                    BankDetails.id, BankDetails.account_no, BankDetails.ifsc_code
                )
                .filter_by(operator_id=operator.id)
                .first()
            )
            operator_list.append(
                {
                    "id": operator.id,
                    "joining_date": operator.joining_date,
                    "name": operator.name,
                    "aadhar_no": operator.aadhar_no,
                    "pf_account_no": operator.pf_account_no,
                    "account_no": bankDetails.account_no,
                    "leaving_date": operator.termination_date,
                    "total_data": data_count,
                }
            )
        return operator_list
    except Exception as e:
        print(e)
        raise e


def get_operator_by_id(id):
    operator = Operator.query.filter_by(id=id).first()
    bankDetails = (
        BankDetails.query.with_entities(
            BankDetails.id, BankDetails.ifsc_code, BankDetails.account_no
        )
        .filter_by(operator_id=id)
        .first()
    )
    phone = (
        Phone.query.with_entities(Phone.id, Phone.phone_no, Phone.types)
        .filter_by(operator_id=id)
        .first()
    )
    photo_list = Photo.query.filter_by(operator_id = id).all()
    file_Links = []
    for photo in photo_list:
        file_Links.append({"id":photo.id, "file_link": photo.image_uri})
    # print(operator, bankDetails, phone)
    try:
        return {
            "id": operator.id,
            "joining_date": operator.joining_date,
            "name": operator.name,
            "aadhar_no": operator.aadhar_no,
            "net_inhand_salary": operator.net_inhand_salary,
            "leaving_date": operator.termination_date,
            "pf_account_no": operator.pf_account_no,
            "odoo_employee_no": operator.odoo_employee_no,
            "phone": {"id": phone.id, "phone_no": phone.phone_no, "types": phone.types},
            "bank_details": {
                "id": bankDetails.id,
                "ifsc_code": bankDetails.ifsc_code,
                "account_no": bankDetails.account_no,
            },
            "file_Links": file_Links,
        }

    except Exception as e:
        print(e)
        raise e


def update_operator(id, data):
    try:
        operator = Operator.query.filter_by(id=id).first()
        operator.joining_date = data.get("joining_date") or operator.joining_date
        operator.name = data.get("name") or operator.name
        operator.aadhar_no = data.get("aadhar_no") or operator.aadhar_no
        operator.net_inhand_salary = (
            data.get("net_inhand_salary") or operator.net_inhand_salary
        )
        operator.odoo_employee_no = data.get("odoo_employee_no") or operator.odoo_employee_no
        operator.pf_account_no = data.get("pf_account_no") or operator.pf_account_no
        operator.termination_date = (
            data.get("leaving_date") or operator.termination_date
        )
        if data.get("phone"):
            phone = Phone.query.filter_by(operator_id=id).first()
            phone.phone_no = data.get("phone").get("phone_no") or phone.phone_no
            phone.types = data.get("phone").get("phone_code") or phone.types
        if data.get("bank_details"):
            bankDetails = BankDetails.query.filter_by(operator_id=id).first()
            bankDetails.ifsc_code = data.get("bank_details").get("ifsc_code") or bankDetails.ifsc_code
            bankDetails.account_no = data.get("bank_details").get("account_no") or bankDetails.account_no

        db.session.commit()
        return {
            "id": operator.id,
            "joining_date": operator.joining_date,
            "name": operator.name,
            "aadhar_no": operator.aadhar_no,
            "net_inhand_salary": operator.net_inhand_salary,
            "leaving_date": operator.termination_date,
            "pf_account_no": operator.pf_account_no,
            "phone": {"id": phone.id, "phone_no": phone.phone_no, "types": phone.types},
            "bank_details": {
                "id": bankDetails.id,
                "ifsc_code": bankDetails.ifsc_code,
                "account_no": bankDetails.account_no,
            },
        }
    except Exception as e:
        raise e


def delete_operator(id):
    try:
        operator = Operator.query.filter_by(id=id).first()
        phone = Phone.query.filter_by(operator_id=id).first()
        bankDetails = BankDetails.query.filter_by(operator_id=id).first()

        db.session.delete(operator)
        db.session.delete(phone)
        db.session.delete(bankDetails)

        db.session.commit()
        return operator

    except Exception as e:
        raise e


def get_all_data_operator_company_id(company_id):
    try:
        all_opertors = (
            Operator.query.filter_by(company_id=company_id)
            .join(Phone)
            .join(BankDetails)
            .all()
        )
        all_opertor_list = []
        for operator in all_opertors:
            all_opertor_list.append(
                {
                    "id": operator.id,
                    "joining_date": operator.joining_date,
                    "name": operator.name,
                    "aadhar_no": operator.aadhar_no,
                    "net_inhand_salary": operator.net_inhand_salary,
                    "pf_account_no": operator.pf_account_no,
                    "id": operator.phone[0].id,
                    "phone_no": operator.phone[0].phone_no,
                    "types": operator.phone[0].types,
                    "ifsc_code": operator.bank_details[0].ifsc_code,
                    "account_no": operator.bank_details[0].account_no,
                }
            )
        return all_opertor_list
    except Exception as e:
        raise e

def search_operator_list(company_id):
    try:
        all_opertor_list = Operator.query.filter(Operator.company_id == company_id).all()
        name = {}
        aadhar = {}
        pf_account_no = {}
        for opertor in all_opertor_list:
            name[opertor.name] = name.get(opertor.name) + 1 if name.get(opertor.name) else 1
            aadhar[opertor.aadhar_no] = aadhar.get(opertor.aadhar_no) + 1 if aadhar.get(opertor.aadhar_no) else 1
            pf_account_no[opertor.pf_account_no] = pf_account_no.get(opertor.pf_account_no) + 1 if pf_account_no.get(opertor.pf_account_no)  else 1
        return {"name":name, "aadhar": aadhar, "pf_account_no":pf_account_no}
    except Exception as e:
        raise e
    