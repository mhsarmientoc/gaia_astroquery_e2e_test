# -*- coding: utf-8 -*-
"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 05 Sep. 2020
"""
import os
import logging

from datetime import datetime
from astropy import log
from src import paths, conf

import src.main.tests_code.e2e_test as e2e
import src.main.report_utils.read_write as io


def process_tests():
    """
        loads the list of test and if executed == False,
        it executes again the tes, if successful, it writes a toml and sets crawled = True
        overwrites the checklist!
    """
    e2e_test = e2e.End2EndTest()
    e2e_test.init()


# _end_of_process_tests

def convert_report_to_html():
    """
        Reads the test report written in toml format and converts it into html format.
        This HTML can be used later to paste de results into a Confluence page.

    """
    folder_in = paths.folder_in
    folder_out = paths.folder_out

    collection = io.get_all_files(folder_in)

    if not collection:
        error_message = "No files to parse. Aborting conversion to HTML"
        log.error(error_message)
        raise ValueError(error_message)
    else:
        for exp in collection:
            # CREATE CONTENT
            html = io.create_html(exp)

            # OUT FILE & LOG
            # Get current timestamp
            time = datetime.now()
            time_str = time.strftime("%Y%m%d-%H%M%S")
            report_name = f'gaia_astroquery_e2e_results_{time_str}.html'
            io.ensure_write_safety(folder_out)
            output_path = os.path.join(folder_out, report_name)
            io.write(html, output_path)
        # __end if


# _end_of_convert_report_to_html

def execute_e2e_and_write_results():
    # run the e2e designed for this mission
    process_tests()
    # convert the report written in toml format to html format
    convert_report_to_html()


# _end_of_execute_e2e_and_write_results


if __name__ == '__main__':

    # Configure log file plus log level
    time = datetime.now()
    time_str = time.strftime('%Y-%m-%d %H:%M:%S')

    config_level = None

    # loggin level
    if conf.LOG_LEVEL == "DEBUG":
        config_level = logging.DEBUG
    elif conf.LOG_LEVEL == "INFO":
        config_level = logging.INFO
    elif conf.LOG_LEVEL == "ERROR":
        config_level = logging.ERROR
    elif conf.LOG_LEVEL == "WARN":
        config_level = logging.WARN
    else:
        # it has not been defined by the configuration env properties. Setting logging level as DEBUG by default
        config_level = logging.DEBUG

    log_filename = os.path.join(paths.path2_to_logs, 'GaiaE2E_4_Astroquery_' + time_str + '.log')
    logging.basicConfig(filename=log_filename, level=config_level)

    # Execute tests
    execute_e2e_and_write_results()
