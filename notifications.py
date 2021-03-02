from courses import title_get

def send_mail(recipient, subject, message):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    username = 'email address'
    password = "password"

    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message,'html'))
    
    print('sending mail to ' + recipient + ' on ' + subject)

    mailServer = smtplib.SMTP('smtp-mail.outlook.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(username, recipient, msg.as_string())
    mailServer.close()

def emailTemplate(title,para,link,button):
        msg="""\
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml" 
        xmlns:v="urn:schemas-microsoft-com:vml"
        xmlns:o="urn:schemas-microsoft-com:office:office">

        <head>
        <title></title>
        <!--[if !mso]><!-- -->
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <!--<![endif]-->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
        #outlook a {
        padding: 0;
        }

        .ReadMsgBody {
        width: 100%;
        }

        .ExternalClass {
        width: 100%;
        }

        .ExternalClass * {
        line-height: 100%;
        }

        body {
        margin: 0;
        padding: 0;
        -webkit-text-size-adjust: 100%;
        -ms-text-size-adjust: 100%;
        }

        table,
        td {
        border-collapse: collapse;
        mso-table-lspace: 0pt;
        mso-table-rspace: 0pt;
        }

        img {
        border: 0;
        height: auto;
        line-height: 100%;
        outline: none;
        text-decoration: none;
        -ms-interpolation-mode: bicubic;
        }

        p {
        display: block;
        margin: 13px 0;
        font-size: 12px;
        }
        </style>
        <!--[if !mso]><!-->
        <style type="text/css">
        @media only screen and (max-width:480px) {
        @-ms-viewport {
            width: 320px;
        }

        @viewport {
            width: 320px;
        }
        }
        </style>
        <!--<![endif]-->
        <!--[if mso]><xml>  <o:OfficeDocumentSettings>    <o:AllowPNG/>   
         <o:PixelsPerInch>96</o:PixelsPerInch>  </o:OfficeDocumentSettings></xml>
         <![endif]-->
        <!--[if lte mso 11]><style type="text/css">  
        .outlook-group-fix {    width:100% !important;  }</style><![endif]-->
        <!--[if !mso]><!-->
        <link href="https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700" 
        rel="stylesheet" type="text/css">
        <style type="text/css">
        @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700);
        </style>
        <!--<![endif]-->
        <style type="text/css">
        .hide_on_mobile {
        display: none !important;
        }

        @media only screen and (min-width: 480px) {
        .hide_on_mobile {
            display: table-row !important;
        }
        }

        [owa] .mj-column-per-100 {
        width: 100% !important;
        }

        [owa] .mj-column-per-50 {
        width: 50% !important;
        }

        [owa] .mj-column-per-33 {
        width: 33.333333333333336% !important;
        }
        </style>
        <style type="text/css">
        @media only screen and (min-width:480px) {
        .mj-column-per-100 {
            width: 100% !important;
        }
        }
        </style>
        </head>

        <body style="background: #FFFFFF;">
        <div class="mj-container" style="background-color:#FFFFFF;">
        <!--[if mso | IE]>      <table role="presentation" border="0" 
        cellpadding="0" cellspacing="0" width="600" align="center" 
        style="width:600px;">        <tr>         
         <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
               <![endif]-->
        <div style="margin:0px auto;max-width:600px;background:#FDFDFD;">
        <table role="presentation" cellpadding="0" cellspacing="0"
        style="font-size:0px;width:100%;background:#FDFDFD;" align="center" border="0">
        <tbody>
        <tr>
        <td
        style="text-align:center;vertical-align:top;direction:ltr;
        font-size:0px;padding:9px 0px 9px 0px;">
        <!--[if mso | IE]>      <table role="presentation" border="0" 
        cellpadding="0" cellspacing="0">   <tr> 
        <td style="vertical-align:top;width:600px;"> <![endif]-->
        <div class="mj-column-per-100 outlook-group-fix"
        style="vertical-align:top;display:inline-block;
        direction:ltr;font-size:13px;text-align:left;width:100%;">
        <table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;"
        width="100%" border="0">
        <tbody>
        <tr>
        <td style="word-wrap:break-word;font-size:0px;padding:26px 26px 26px 26px;"
        align="center">
        <div
        style="cursor:auto;color:#000000;font-family:Ubuntu, Helvetica, Arial, sans-serif;
        font-size:11px;line-height:1.5;text-align:center;">
        <h1
        style="font-family: &apos;Cabin&apos;, sans-serif; line-height: 100%;">
        <span style="font-size:22px;">              
        """

        msg+=title
        msg+="""\
        </span></h1>
        </div>
        </td>
        </tr>
        <tr>
        <td
        style="word-wrap:break-word;font-size:0px;padding:10px 25px;
        padding-top:10px;padding-bottom:10px;padding-right:10px;padding-left:10px;">
        <p
        style="font-size:1px;margin:0px auto;border-top:1px solid #000;width:100%;">
        </p>
        <!--[if mso | IE]><table role="presentation" align="center" border="0"
         cellpadding="0" cellspacing="0" style="font-size:1px;margin:0px auto;
         border-top:1px solid #000;width:100%;" width="600">
         <tr><td style="height:0;line-height:0;"> </td></tr></table><![endif]-->
        </td>
        </tr>
        <tr>
        <td style="word-wrap:break-word;font-size:0px;padding:15px 15px 15px 15px;"
        align="left">
        <div
        style="cursor:auto;color:#000000;font-family:Ubuntu, Helvetica, Arial, sans-serif;
        font-size:11px;line-height:1.5;text-align:left;">
        <p>
        """
        msg+=para
        msg+="""\
        </p>
        </div>
        </td>
        </tr>
        <tr>
        <td style="word-wrap:break-word;font-size:0px;padding:20px 20px 20px 20px;"
        align="center">
        <table role="presentation" cellpadding="0" cellspacing="0"
        style="border-collapse:separate;" align="center" border="0">
        <tbody>
        <tr>
        <td style="border:0px solid #000;border-radius:24px;color:#fff;
        cursor:auto;padding:10px 28px 10px 28px;"
        align="center" valign="middle" bgcolor="#344EE8"><a
        href=
        """
        msg+=link
        msg+="""\
        style="text-decoration:none;background:#344EE8;color:#fff;
        font-family:Ubuntu, Helvetica, Arial, sans-serif, Helvetica, Arial, sans-serif;
        font-size:14px;font-weight:normal;line-height:120%;text-transform:none;margin:0px;"
        target="_blank">
        """
        msg+=button
        msg+="""\
        </a></td>
        </tr>
        </tbody>
        </table>      
        <tbody>
        <tr>
        <td><img alt height="auto"
        src="https://i.imgur.com/TblwCSK.jpg"
        style="border:none;border-radius:0px;display:block;
        margin-left: auto;margin-right: auto;
        font-size:13px;outline:none;text-decoration:none;width:50%;height:auto;"
        </td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        <tr>
        <td style="word-wrap:break-word;font-size:0px;">
        <div style="font-size:1px;line-height:50px;white-space:nowrap;">&#xA0;
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        <!--[if mso | IE]>      </td></tr></table>      <![endif]-->
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        <!--[if mso | IE]>      </td></tr></table>      <![endif]-->
        </div>
        </body>

        </html>
        """

        return msg


def notify_students(email,CRN,mailType):
        #For open/closed courses
        if mailType.lower()=='new' or mailType=='0':
                sub='SCSU Wishlist: New Section'
                title='A new course has opened!'
                contents="""\
                Course: 
                """
                contents+=title_get(CRN)
                contents+=' Course Registration Number:'
                contents+=CRN
                contents+="""
                 now has a new 
                section. To view, log in below.
                """
                msg = emailTemplate(title, contents,'"/login"','Login')

        elif mailType.lower()=='open' or mailType=='1':
                sub='SCSU Wishlist: Opened seat'
                title='A new seat has opened!'
                contents="""\
                Course: 
                """
                contents+=title_get(CRN)
                contents+=' Course Registration Number:'
                contents+=CRN
                contents+=""" now has an 
                opened seat. To view, log in below.
                """
                msg = emailTemplate(title, contents,'"/login"','Login')

        elif mailType.lower()=='cancel' or mailType=='2':
                sub='SCSU Wishlist: Cancelled Course'
                title='A course has been cancelled'
                contents="""\
                Course: 
                """
                contents+=title_get(CRN)
                contents+=' Course Registration Number:'
                contents+=CRN
                contents+="""
                 has been cancelled. To view, log in below.
                """
                msg = emailTemplate(title, contents,'"/login"','Login')

        elif mailType.lower()=='risk' or mailType=='3':
                sub='SCSU Wishlist: Course at Risk'
                title='A course  on your watchlist is at risk'
                contents="""\
                Course: 
                """
                contents+=title_get(CRN)
                contents+=' Course Registration Number:'
                contents+=CRN
                contents+="""
                 may be at risk for cancellation. To view, log in below.
                """
                msg = emailTemplate(title, contents,'"/login"','Login')

        
        send_mail(email,sub,msg)

def password_reset(email,newPass):
        sub='SCSU Wishlist: Password Reset'
        title='Your password has been reset'
        contents="""\
        You have requested to reset your password. 
        Your new password is now:<b>
        """
        contents+=newPass
        contents+="""\
        </b><br>Please login below to change your password.
        """
        msg = emailTemplate(title, contents,'"/login"','Login')
        send_mail(email,sub,msg)
        

def account_email(email,mailType):
        #For account management
        if mailType.lower()=='created' or mailType=='1':
                sub='Scsu Wishlist: Account Created'
                title='Welcome to SCSU Wishlist!'
                contents="""\
                Your account has been succesfully created.
                You may now log in below using your username (email) and password.
                """
                msg = emailTemplate(title, contents,'"/login"','Login')

        elif mailType.lower()=='delete' or mailType=='2':
                sub='Scsu Wishlist: Account Deleted'
                title="We're sorry to see you go!"
                contents="""\
                Your account has been succesfully deleted.
                Thanks for joing SCSU Wishlist. If you wish to
                sign up again, click the button below.
                """
                msg = emailTemplate(title, contents,'"/signup"','Sign up')

        elif mailType.lower()=='resetpw' or mailType == '3':
                sub='Scsu Wishlist: Password Changed' 
                title='Your password has changed'
                contents="""\
                You have succesfully changed your password.
                You may now log in below using your new password.
                """
                msg = emailTemplate(title, contents,'"/login"','Login')

        send_mail(email,sub,msg)

