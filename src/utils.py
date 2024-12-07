import logging

def init_logging(name="main"):
    """
    Sets-up the logging library - save logs to a file
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=f"{name}.log", encoding='UTF-8', level=logging.INFO, filemode='w',
                        format="%(asctime)s %(levelname)s: %(message)s", datefmt='%I:%M:%S')
    logger.info("Set-up logging successfully")