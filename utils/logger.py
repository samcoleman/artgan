import logging
import sys


def create_logger(filename: str):
    """Creates a logger obj using logging library with a typical setup

    Args:
        filename (str): filename which logger dumps logs to

    Returns:
        Logger: Logger object from logging
    """
    # Initiating the logger object
    logger = logging.getLogger(__name__)

    # Set the level of the logger. This is SUPER USEFUL since it enables you to decide what to save in the logs file.
    # Explanation regarding the logger levels can be found here - https://docs.python.org/3/howto/logging.html
    logger.setLevel(logging.DEBUG)

    # Create the logs.log file
    handler = logging.FileHandler(filename+'.log')

    # Format the logs structure so that every line would include the time, name, level name and log message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Adding the format handler
    logger.addHandler(handler)

    # And printing the logs to the console as well
    logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger