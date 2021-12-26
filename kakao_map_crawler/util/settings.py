import os
from sys import platform as p_os
from os.path import abspath, dirname, join


BASE_DIR = abspath(dirname(__file__))
OS_ENV = "windows" if p_os == "win32" else "osx" if p_os == "darwin" else "linux"


class Settings:
    log_output_toconsole = True
    log_output_tofile = True
    log_file_per_run = False
    log_location = join(BASE_DIR, 'logs')

    loggers = {}

    # chromedriver
    chromedriver_min_version = 2.36
    specific_chromedriver = f"chromedriver_{OS_ENV}"
    chromedriver_location = os.path.join(BASE_DIR, "assets", specific_chromedriver)

    if not os.path.exists(chromedriver_location):
        chromedriver_location = os.path.join(BASE_DIR, 'assets', 'chromedriver')
