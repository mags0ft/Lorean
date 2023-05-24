import logging

def create_logger(name, filepath):
    l = logging.getLogger(name)
    l.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)02d %(levelname)s: %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    handler = logging.FileHandler(filepath)

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)


    l.addHandler(handler)

    return l