from datetime import datetime


def log_event(method, action, details=""):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    details = str(details).replace("\n", " ").replace("\r", " ")

    with open("forensics.log", "a", encoding="utf-8") as file:
        file.write(
            f"{timestamp} | {method} | {action} | {details}\n"
        )