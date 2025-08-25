from datetime import datetime


class Logger:
    def log(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}]", *args, **kwargs)


logger = Logger()
