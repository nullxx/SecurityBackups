from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def sendMail(mail, htmlContent):
	to = mail
	fromm = "security@nullxx.github.com"
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")

	message = MIMEMultipart('alternative')
	message.add_header('Subject', current_time + ' SECURITY BACKUP')
	message.add_header('To', to)
	message.add_header('From', fromm)
	message.attach(MIMEText(htmlContent, # html content
							'html'))

	# pipe the mail to sendmail
	sendmail = os.popen('/usr/sbin/sendmail ' + to, 'w')
	sendmail.write(message.as_string())
	if sendmail.close() is not None:
		print ('error: failed to send mail :-(' )


now = datetime.now()
current_time = now.strftime("%Y-%m-%d_%H:%M:%S")

PATH = "/root/backup/"

FILENAME = "SEC-COPY__" + current_time + ".tar.gz"
LOG_FILE_NAME = "SEC-COPY__" + current_time
LOGFILE_PATH = PATH + LOG_FILE_NAME + ".log"
FULLPATH = PATH + FILENAME
DESTINATION_FOLDER_ID = "<FOLDER_ID>"
MAIL = "mail@example.com"

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)


doBackup = "sudo tar -cvpzf " + FULLPATH + " --exclude=" + FULLPATH + " --one-file-system / > " + LOGFILE_PATH
os.system(doBackup)

backupFile = drive.CreateFile({'title': FILENAME, 'parents': [{'id': DESTINATION_FOLDER_ID}]})
backupFile.SetContentFile(FULLPATH)
backupFile.Upload()

backupLogFile = drive.CreateFile({'title': LOG_FILE_NAME, 'parents': [{'id': DESTINATION_FOLDER_ID}]})
backupLogFile.SetContentFile(LOGFILE_PATH)
backupLogFile.Upload()

sendMail(MAIL, "<h3>Security backup</h3></br><p>A security backup has been made on " + current_time)

print("Uploaded at " + current_time)

print("Removing file at" + FULLPATH)
os.system("rm -r " + FULLPATH)

print("Removing file at" + LOGFILE_PATH)
os.system("rm -r " + LOGFILE_PATH)
