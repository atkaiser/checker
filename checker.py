import time

from checkers import RandomChecker
from checkers import TooManyProcessesChecker

OUTPUT_DIR = "/home/akaiser/checker"

GMAIL_USR = ""
GMAIL_PWD = ""
CREDENTIALS_FILE = "/home/akaiser/dev/checker/credentials.txt"
with open(CREDENTIALS_FILE, "r") as f:
    lines = f.readlines()
    GMAIL_USR = lines[0].strip()
    GMAIL_PWD = lines[1].strip()


def send_email(recipient, subject, body):
    import smtplib

    FROM = GMAIL_USR
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(GMAIL_USR, GMAIL_PWD)
        server.sendmail(FROM, TO, message)
        server.close()
        print("successfully sent the mail")
    except e:
        print(e)
        print("Failed to send mail.")


if __name__ == "__main__":

    checks = []
    checks.append([TooManyProcessesChecker(), False])

    while True:
        print("Starting check loop")
        for check_tuple in checks:
            check = check_tuple[0]
            name = check.get_name()
            check_output = check.run_check()
            if not check_output[0]:
                print("Check failed: {}".format(check_output[1]))
                if not check_tuple[1]:
                    send_email("alextkaiser@gmail.com",
                               "{} check failed".format(name),
                               check_output[1])
                    check_tuple[1] = True
            else:
                if check_tuple[1]:
                    send_email("alextkaiser@gmail.com",
                               "{} check recovered".format(name),
                               "{} is back to normal.".format(name))
                    check_tuple[1] = False
        time.sleep(10)
