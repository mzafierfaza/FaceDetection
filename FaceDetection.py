import cv2              # Import library opencv untuk Pengolahan Citra di Python
import time, threading             # Import Time untuk library waktu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

face = cv2.CascadeClassifier('/home/pi/IPCAM/facial_recognition_model.xml')
video = cv2.VideoCapture("rtsp://192.168.43.75:554/unicast")

email = 'xxxxxxxxx@gmail.com'
password = 'xxxxxxxxx'
send_to_email = 'xxxxxxxxx@gmail.com'
subject = 'Wajah terdeteksi!'
message = 'Hai xxxxxx, Wajah telah terdeteksi. berikut gambarnya'
file_location = '/home/pi/IPCAM/face.jpg'

last = time.perf_counter()
current = last

def setup_email():
    global msg
    global filename
    global attachment
    global part
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    #Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

def kirim_email():
    global server
    global text
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()

while True:
    current = time.perf_counter()
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    muka = face.detectMultiScale(gray, 1.1, 4)
    for (mx, my, mw, mh) in muka:           
        cv2.rectangle(frame, (mx, my), (mx+mw, my+mh), (0,255,0), 2)
        cv2.putText(frame, "Number of faces detected: " + str(muka.shape[0]), (0,frame.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.7,  (0,255,0), 1)
        cv2.imwrite('/home/pi/IPCAM/face.jpg',frame)
        setup_email()
        if current - last > 10.:
            last = current        
            print('Gambar Telah di Capture')
            kirim_email()
            print('Email Telah di Kirim---')
            
    cv2.imshow('FACE DETECTION', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
