import logging

def init_logger(name: str="main", file: str="data/logs/main.log", level=logging.INFO) -> None:
    """
    Sets-up a logger with a specific name and file
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler
    file_handler = logging.FileHandler(file, mode='w')
    file_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(filename)s: %(message)s", datefmt='%I:%M:%S', )
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers(): # Avoid duplicate handlers
        logger.addHandler(file_handler)

    return logger