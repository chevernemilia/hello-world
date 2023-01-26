#!/usr/bin/env python
# coding: utf-8

# In[8]:


import time
import datetime
import os
from os.path import exists


# import smtplib
import email, smtplib, ssl

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

import sys
sys.path.append('/Users/eli/Python/personal_projects/')


# In[9]:


current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_datetime_name = datetime.datetime.now().strftime("%Y-%m-%d_%I:%M%p")

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p")


output_dir = '/Users/eli/Python/personal_projects/testing/testResultOutput/'
# output_txt = output_dir + 'TestResult-' + current_date + '.txt'
output_txt = output_dir + 'TestResult-' + current_datetime_name + '.txt'

output_txt_name = output_txt.split('/')[-1]
output_txt_name

if exists(output_txt):
    with open (output_txt, 'r+') as f:
        f.truncate(0)  

tfile = open(output_txt, 'a')



# In[10]:


start_time = time.time()

tstring = 'current_datetime:  ' + current_datetime
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')

tstring = 'Hello World! This is ECL. \nThis is a test for scheduling automation.'
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')

tstring = "--- %s seconds " % float( '%.5g' % (time.time() - start_time)) + 'to complete current task. --------'

print(tstring)
tfile.write(tstring)
tfile.write('\n\n')

print("output_txt_name: " , output_txt_name)
# print("--- %s mintsues " % float( '%.5g' % ((time.time() - start_time)/60)) + 'to complete Sending Emails --------')
tfile.close()


# In[4]:





def send_email(subject, body, sender, recipients, password, output_pdf = None, output_xlsx = None, output_txt = None):
    # msg is an MIMEMultipart object that can include both txt and attachments
    msg = MIMEMultipart()
    # msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    # msg['Bcc'] = sender
    msg.attach(MIMEText(body, "plain"))

#     below could possibly attach all three files only if they are provided in this func
    ############## Encoding binary data PDF into ASCII characters thru base64 and attach ot the msg obj #########################
    # Open PDF file in binary mode
    if output_pdf is not None:
        with open(output_pdf, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part_pdf = MIMEBase("application", "octet-stream")
            part_pdf.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part_pdf)
        # Add header as key/value pair to attachment part
        part_pdf.add_header(
            "Content-Disposition",
            f"attachment; filename= {output_pdf_name}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part_pdf)
    #########################################end of PDF attach ################################################################
    ############## Encoding binary data EXCEL into ASCII characters thru base64 and attach ot the msg obj #########################
    # Open PDF file in binary mode
    if output_xlsx is not None:
        with open(output_xlsx, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part_xlsx = MIMEBase("application", "octet-stream")
            part_xlsx.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part_xlsx)
        # Add header as key/value pair to attachment part
        part_xlsx.add_header(
            "Content-Disposition",
            f"attachment; filename= {output_xlsx}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part_xlsx)
    #########################################end of XLSX attach ################################################################
    ############## Encoding binary data TXT/LOG  into ASCII characters thru base64 and attach ot the msg obj #########################
    # Open PDF file in binary mode
    
    if output_txt is not None:
        with open(output_txt, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part_txt = MIMEBase("application", "octet-stream")
            part_txt.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part_txt)
        # Add header as key/value pair to attachment part
        part_txt.add_header(
            "Content-Disposition",
            f"attachment; filename= {output_txt_name}",
        )
        # Add attachment to message and convert message to string
        msg.attach(part_txt)
    #########################################end of TXT/LOG attach ################################################################

    msg_w_attachments = msg.as_string()

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg_w_attachments)
    smtp_server.quit()


# In[11]:



################## Define all necesary elements for email #############
# subject = "ECL Email Test"
# subject = "ECL Email Test: " + " " + depart_destinations  + "--" + return_destinations

subject = "ECL Email Test: Cronjob Scheduler" 

# body = "Testing to see if target account receive email"
# body = "Testing to see if target accounts receive email w/ PDF & EXCEL Attachments, multiple emails, multile domains"
body = """Testing to see if Cronjob Scheduler work as expected. """


os.chdir('/Users/eli/Python/personal_projects/')
print(os.getcwd())

import user_config as uc
sender = uc.sender
# this is the app password associate with sender gmail account, only app password available for gmail app after May 2022
password = uc.password
# recipients_eli =uc.recipients_eli
general_recipients = uc.general_recipients 

print('sender: ', sender)
print('password: ', password)
print('general_recipients: ', general_recipients)


# In[6]:


start_time = time.time()
send_email(subject, body, sender, general_recipients, password, None, None, output_txt)
print("--- %s seconds " % float( '%.5g' % (time.time() - start_time)) + 'to complete Sending Emails --------')


# In[ ]:




