#SENDS AN EMAIL TO MYSELF AND JOHN ANDERSON
def sendEmail(emailbody,
              emailTo,
              subject,
              smtpserver='postoffice.dpiwe.tas.gov.au'):
    """
    Send email from Python.

    Keyword arguments:
    emailbody     String containing body of email
    emailTo       List of recipients.  sendmail() takes a list of recipients
    subject       String containing subject of email
    smtpserver    Optional : smtpserver name


    Notes:
    """

    try:
        strFrom = 'Samuel.Langley@dpipwe.tas.gov.au'
        strTo = ''.join(emailTo) # Convert list of email recipents to String

        # Create a text/plain message
        msgRoot = MIMEText(emailbody)
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo

        # Send the email
        print("Sending email")
        logging.info('Sending email')
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.sendmail(strFrom, emailTo, msgRoot.as_string())
        smtp.quit()
        print("Email sent to " + strTo)
        logging.info("Email sent to " + strTo)

    except IOError, errDesc:
        print("IOError : " + str(errDesc))
        logging.critical("IOError : " + str(errDesc))
    except smtplib.SMTPConnectError, errDesc:
        print("SMTPConnectError : ", errDesc)
        logging.critial("SMTPConnectError : " + errDesc)
    except smtplib.SMTPException, errDesc:
        print("SMTPException : ", errDesc)
        logging.critical("SMTPException : " + errDesc)
    except:
        print "Exception Error in emailSender : ", sys.exc_info()[0]
        print sys.exc_info()[1]
        print sys.exc_info()[2]
        logging.critical("Exception Error in emailSender : " + sys.exc_info()[0])
        logging.critical(sys.exc_info()[1])
        logging is very bad for the environment!!!!!!!!!!!!!!!!!!!!!!!
####################################################################################
subject="test"
emailbody="sam"
####################################################################################
#EMAILING LOG FILE TO THE PEOPLE LISTED ON MY EMAIL LIST
emailfile="D:\\Automated Jobs\\ReplicateAerialThumbnails\\EmailList.txt"
f=open(emailfile)
emaillist=f.readlines();
e=0
n=len(emaillist)
while e<n:
    emailTo=emaillist[e]
    smtpserver='postoffice.dpipwe.tas.gov.au'
    sendEmail(emailbody,emailTo,subject,smtpserver)
    e=e+1

###################################################################################
#THE GUNNERS ABOSLUTELY ROCKS AND IF YOU DON'T LIKE , THEN GET A TASTE AND GET A LIFE
#THE GINNERS, ROCK BIGGGGGGGGGGGGGGGGGGGGG TIME!!!!!!!!!!!!!!!!!!
