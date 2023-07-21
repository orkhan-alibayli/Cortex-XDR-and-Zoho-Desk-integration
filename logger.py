from datetime import datetime


def log(text):

    with open("logs.txt","a") as file:
        file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":    " + text + "\n") 