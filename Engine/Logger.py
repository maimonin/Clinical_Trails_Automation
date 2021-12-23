def log(message):
    f = open("Logger.txt", "a")
    f.write(message + '\n')
    f.close()