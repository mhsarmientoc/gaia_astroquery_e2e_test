# -*- coding: utf-8 -*-
"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 05 Sep. 2020
"""
import os
from datetime import datetime
from pathlib import Path

from astropy import log

import src.main.tests_code.e2e_test as e2e
import src.main.report_utils.read_write as io


def process_tests():
    """
        loads the list of test and if executed == False,
        it executes again the tes, if successful, it writes a toml and sets crawled = True
        overwrites the checklist!
    """
    # TODO: read environment from configuration
    current_environment = "DEV"
    e2e_test = e2e.End2EndTest(current_environment)
    e2e_test.init()


# _end_of_process_tests

def convert_report_to_html():
    """
        Reads the test report written in toml format and converts it into html format.
        This HTML can be used later to paste de results into a Conflucence page.

    """
    folder_in = Path(__file__).parent / '../../test_report/toml/'
    folder_out = Path(__file__).parent / '../../test_report/html/'
    logs_path = Path(__file__).parent / '../../logs'

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
    execute_e2e_and_write_results()
