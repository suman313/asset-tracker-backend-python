from flask_mail import Mail, Message
from functions.utilities.emailtemp import cred_temp, change_password, on_board_company_tem, on_request

mailer = Mail()

    





def send_email(username=None, password=None, email=None, topic_type=None, company=None): 
        try:    
                if topic_type == 'add_employee':
                        print(topic_type)
                        inboxmgs = cred_temp(username, password, company)
                        subject = "Welcome to Durbin Asset Tracker!!"
                        msg = Message(subject=subject, sender="admin@quinch.co.in", recipients=[email], html=inboxmgs)
                        mailer.send(msg)
                        return "success"
                elif topic_type == 'change_password':
                        print(topic_type)
                        inboxmgs = change_password()
                        subject = "Your password successfully changed"
                        msg = Message(subject=subject, sender="admin@quinch.co.in", recipients=[email], html=inboxmgs)
                        mailer.send(msg)
                        return "success"
                elif topic_type == 'signup':
                        print(topic_type)
                        inboxmgs = on_request()
                        subject = "Company Onboard Request Successfully Submitted"
                        msg = Message(subject=subject, sender="admin@quinch.co.in", recipients=[email], html=inboxmgs)
                        mailer.send(msg)
                        return "success"
                elif topic_type == 'approve_company':
                        print(topic_type)
                        inboxmgs = on_board_company_tem(username, password)
                        subject = "Company Onboard Request Approved"
                        msg = Message(subject=subject, sender="admin@quinch.co.in", recipients=[email], html=inboxmgs)
                        mailer.send(msg)
                        return "success"
                        

        except Exception as e:
                print(e)
                raise e
