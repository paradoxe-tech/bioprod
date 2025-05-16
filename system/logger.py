import logging
import sys
from typing import Dict

default = {
    "level": "INFO",
    "format": "[%(name)s] %(message)s",
    "file": "bioprod.log"
}

def setup_logger(config: Dict = default) -> logging.Logger:
     
    logger = logging.getLogger("bioprod")
    logger.setLevel(getattr(logging, config.get("level", default["level"])))
    
    formatter = logging.Formatter(
        config.get("format", default["format"]),
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if "file" in config:
        file_handler = logging.FileHandler(config["file"])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger