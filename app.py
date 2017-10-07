from flask import Flask, render_template, request, make_response
from werkzeug import secure_filename
import pandas as pd
from autoEmail import email
from tqdm              import tqdm
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.base      import MIMEBase
from email             import encoders
import csv
import smtplib
import argparse
import io
from credentials import SENDER_EMAIL, SENDER_PASSWORD

app = Flask(__name__)

EMAIL_TEMPLATE = """
Greetings {},

You have scored {} marks out of {} in the Test: {}

All the best!
""" 


@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      f = request.files['file']

      df = pd.read_csv(f)

      smtp = smtplib.SMTP('smtp.gmail.com')
      smtp.ehlo()
      smtp.starttls()
      smtp.login(SENDER_EMAIL, SENDER_PASSWORD)

      for index, row in df.iterrows():
         name, toEmail, score, totalScore, testName = row['Name'], row['Email'], row['Marks'], row['Total'], row['TestName']
         subject = 'Test Result'
         content = EMAIL_TEMPLATE.format(name, score, totalScore, testName)

         msg = MIMEMultipart()
         msg['From'] = SENDER_EMAIL
         msg['To'] = toEmail
         msg['Subject'] = subject
         body = content
         msg.attach(MIMEText(body, 'plain'))

         # # open the file to be sent 
         # filename = "AkhileshChobey.pdf"
         # attachment = open("AkhileshChobey.pdf", "rb")
          
         # # instance of MIMEBase and named as p
         # p = MIMEBase('application', 'octet-stream')
          
         # # To change the payload into encoded form
         # p.set_payload((attachment).read())
          
         # # encode into base64
         # encoders.encode_base64(p)
         # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
          
         # # attach the instance 'p' to instance 'msg'
         # msg.attach(p)

         email_content = msg.as_string()

         smtp.sendmail(SENDER_EMAIL, toEmail, email_content)


      return df.to_html()
		
if __name__ == '__main__':
   app.run(debug = True)