import logging
import sys
import json_logging
from os import environ

if environ.get("ENVIRONMENT") == "prod":
    # log is initialized without a web framework name
    json_logging.ENABLE_JSON_LOGGING = True
    json_logging.init_non_web()
    
    logging.basicConfig(
            level=logging.INFO, 
            filename="/var/log/sainos.log", 
            filemode='w'
            )
    
    logger = logging.getLogger("test logger")
    # logger.setLevel(logging.DEBUG)
    # logger.addHandler(logging.StreamHandler(sys.stdout))

    logger.info("test log statement")
    logger.info("test log statement with extra props", extra={'props': {"extra_property": 'extra_value'}})
else:
    logging.basicConfig(
            filename='filename.log',
            filemode='w',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.INFO
            ) # INFO level records everything above DEBUG`
    logger = logging.getLogger(__name__)

