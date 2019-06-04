#!/usr/bin/env python3

from Controller.utils import Start
from sys import exit
import logging

if __name__ == "__main__":
    logging.info("Main program started")
    c = Start()
    exit(c.run())
