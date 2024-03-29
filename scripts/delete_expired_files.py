#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import os
import platform
import time 
import logging
import pathlib
from datetime import datetime

MAX_MINUTES_MODEL_FILE = 1410 # one day
MAX_MINUTES_ZIP_FILE = 10080  # one week

PATH_1 = str(pathlib.Path(__file__).parent.resolve()) + "/../src/restapi/static"
PATH_2 = str(pathlib.Path(__file__).parent.resolve()) + "/../src/restapi/files"
ZIP_PATH = str(pathlib.Path(__file__).parent.resolve()) + "/../src/restapi/backup"
LOG_FILE = str(pathlib.Path(__file__).parent.resolve()) + "/logs/deleted_log.log"

FILE_EXTENSIONS = ['.xml', '.html', '.xls', '.ods', '.xlsx', '.json', '.tar.gz']

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def remove_expired(folder_path, max_minutes):

    files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    for f in files:

        path = join(folder_path, f)
        print(f, creation_date(path))
    
        current = time.time()
        file_creation_minutes = int(round((current - creation_date(path)) / 60))

        _, file_extension = os.path.splitext(path)

        if file_creation_minutes > max_minutes and file_extension in FILE_EXTENSIONS \
        and "index" not in path:
            
            os.remove(path)

            current_date = datetime.fromtimestamp(current)
            logging.info("Removed file: '" + f + "' on " + str(current_date))
    

def compress_folder(folder, zip_folder):
    os.system('tar -zcvf ' + zip_folder + '/$(date +%s).tar.gz ' + folder)
    

logging.info("Executing at: " + str(datetime.fromtimestamp(time.time())))
remove_expired(PATH_1, MAX_MINUTES_MODEL_FILE)
compress_folder(PATH_2, ZIP_PATH)
remove_expired(PATH_2, MAX_MINUTES_MODEL_FILE)
remove_expired(ZIP_PATH, MAX_MINUTES_ZIP_FILE)

