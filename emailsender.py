# 
# A small tool to check if data is generated and if yes -> zip it and send via e-mail.
# 
# I have used it on a test cluster environment for my PhD work compuataion that sometimes 
# could take 4-5 hours of calculation. Thus it have helped me to automate part of the work and save some time for coffee.  
# 
# @madbitloman aka Oleks 


from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

import smtplib
import os, os.path 
import tarfile
import zipfile
import shutil
import time

def make_tarfile(output_filename, source_dir):
	# Data can be tar.gz insted of zip with this method 
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def email_sender(name):
	zip_f = open('%s.zip' % name,'rb')
	msg = MIMEMultipart()
	part = MIMEBase('application', 'zip')
	part.set_payload(zip_f.read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % name)
	msg.attach(part)
	
	fromaddr = '@gmail.com'
	toaddrs  = '@gmail.com'
	msg = 'Please find beauty of all data attached!'
	
	# Credentials for gmail
	username = 'avecbardan@gmail.com'
	password = ''
	
	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()

def main():
	# Here we assume that all generated data is stored in folder data_out 
	path, dirs, files = os.walk("/home/bardan/path_to_folder/data_out").next()
	# I only checked if there are 5 files in the folder, if so -> zip and send it. 
	file_count = len(files)
	if file_count==5:
		# Added timestamp to the output file to recognize when it was generated. 
		# Although data files had their own specific parametrized names as well 
		name = 'results_%s' % time.strftime("%H:%M:%S")
		
		shutil.make_archive(name, 'zip', '/home/bardan/path_to_folder/data_out')
		
		email_sender(name)

main()		

