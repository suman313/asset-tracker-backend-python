from config import F_END

forntendlocation = F_END

def cred_temp (username, password, company):
        try:
                userPassword = password
                userName = username

                temlpate_for_email = '''<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Email Template</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: flex-start;
            flex-direction: column;
        }

        h1 {
            color: #333333;
            margin: 0;
            padding: 20px 0;
            text-align: center;
            display: flex;

            justify-content: flex-start;
        }

        img {

            align-self: center;
        }

        p {
            color: #777777;
            line-height: 1.5;
            margin: 0;
            padding: 10px 0;
        }

        .username {
            color: #333333;
            font-weight: bold;
        }

        .password {
            color: #333333;
            font-weight: bold;
        }

        .button {
            display: inline-block;
            background-color: #0088cc;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 4px;
            margin-top: 20px;
            margin-left: auto;
            margin-right: auto;
        }

        .button:hover {
            background-color: #005580;
        }
    </style>
</head>

<body>
    <div class="container">
        <img src="https://mango-bay-0d036af1e.2.azurestaticapps.net/img/logo-black-text-transparent-bg.png"
            width="100px" style="align-items: center;">
        <h1>Welcome to Durbin Asset Tracker!! You are invited by''' + f"{company}" + ''' admin</h1>
        <p>Your username and password for accessing your account are:</p>
        <p><span class="username">Username:</span> <span class="value">'''+ f"{userName}" +'''</span></p>
        <p><span class="password">Password:</span> <span class="value">''' + f"{userPassword}" + '''</span></p>
        <p>Make sure to keep this information safe and secure. You can now log in to your account and start using the
            platform.</p>
        '''+ f'''<a href="{forntendlocation}/login" class="button">Log In</a>''' + '''
    </div>
</body>

</html>'''
                return temlpate_for_email
        except Exception as e: 
                raise e 


def change_password():
        return      '''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Password Change Successful</title>
                            <style>
                                body {
                                    font-family: Arial, sans-serif;
                                    background-color: #f2f2f2;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    height: 100vh;
                                }
                                
                                .container {
                                    max-width: 500px;
                                    padding: 20px;
                                    background-color: #ffffff;
                                    border-radius: 5px;
                                    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
                                }
                                
                                h1 {
                                    color: #333333;
                                    text-align: center;
                                    margin-bottom: 20px;
                                }
                                
                                p {
                                    color: #666666;
                                    line-height: 1.5;
                                    margin-bottom: 10px;
                                }
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h1>Password Change Successful</h1>
                                <p>Your password has been changed successfully.</p>
                                <p>If you did not request this change, please contact our support team immediately.</p>
                            </div>
                        </body>
                        </html>
                        '''


def on_board_company_tem(username, password):

                temp =      '''<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Company Onboard Request Approved</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            color: #333333;
            padding: 20px;
            line-height: 1.6;
        }

        h1 {
            color: #555555;
            text-align: center;
        }

        h2 {
            color: #888888;
            margin-top: 30px;
        }

        ul {
            list-style-type: none;
            padding-left: 0;
        }

        li {
            margin-bottom: 10px;
        }

        ol {
            padding-left: 20px;
        }

        p {
            margin-bottom: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .logo {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo img {
            max-width: 150px;
        }

        .contact-info {
            font-size: 14px;
        }

        .next-steps {
            margin-top: 30px;
        }
        .button {
            display: inline-block;
            background-color: #0088cc;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 4px;
            margin-top: 20px;
            margin-left: auto;
            margin-right: auto;
        }

        .button:hover {
            background-color: #005580;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="logo">
            <img src="https://mango-bay-0d036af1e.2.azurestaticapps.net/img/logo-black-text-transparent-bg.png" alt="Company Logo">
        </div>
        <h1>Company Onboard Request Approved</h1>
        <p>Congratulations! Your company's onboard request has been successfully approved by the platform.</p>


        <div class="next-steps">
            <p>Now that your onboard request has been approved, please complete the following steps:</p>
            <ol>
                <li>Review the platform's terms and conditions.</li>
                <li>Provide any additional required documentation or information.</li>
                <li>Set up your company profile and add relevant details.</li>
                <li>Start exploring the platform and its features.</li>
            </ol>
        </div>

        <div class="contact-info">
            <p>If you have any questions or need further assistance, please don't hesitate to contact our support team
                at support@durbin.live .</p>
        </div>
        <p>Your username and password for accessing your account are:</p>
        <p><span class="username">Username:</span> <span class="value">'''+ f"{username}" +'''</span></p>
        <p><span class="password">Password:</span> <span class="value">''' + f"{password}" + '''</span></p>
        <p>Make sure to keep this information safe and secure. You can now log in to your account and start using our
            services.</p>
        <p>Thank you and welcome aboard!</p>
        '''+ f'''<a href="{forntendlocation}/login" class="button">Log In</a>''' + '''
    </div>
</body>

</html> '''
                return temp


def on_request():
        temp =   '''<!DOCTYPE html>
                    <html>
                    <head>
                    <title>Company Onboard Request Submitted</title>
                    <style>
                        body {
                        font-family: Arial, sans-serif;
                        background-color: #f1f1f1;
                        padding: 20px;
                        }

                        .container {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #fff;
                        padding: 30px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        }

                        h1 {
                        color: #333;
                        font-size: 24px;
                        margin-top: 0;
                        }

                        p {
                        color: #666;
                        font-size: 16px;
                        }
                    </style>
                    </head>
                    <body>
                    <div class="container">
                        <h1>Company Onboard Request Successfully Submitted</h1>
                        <p>Thank you for submitting your company onboard request. We have received your information and it is now being reviewed by our platform administrators.</p>
                        <p>Please note that it may take some time to approve your request. We appreciate your patience and will notify you via email once the request has been processed.</p>
                        <p>If you have any urgent questions or need further assistance, please contact our support team.</p>
                    </div>
                    </body>
                    </html>
                    '''
        return temp


