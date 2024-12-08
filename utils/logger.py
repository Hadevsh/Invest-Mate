import logging

def init(name: str="main") -> None:
    """
    Sets-up the logging library - save logs to a file
    """
    logging.basicConfig(encoding='UTF-8', level=logging.INFO,
                       format="%(asctime)s %(name)s %(levelname)s: %(message)s", datefmt='%I:%M:%S',
                       handlers=[logging.FileHandler(f"data/logs/{name}.log", mode='w', encoding='UTF-8')])
    logging.info("Set-up logging successfully")