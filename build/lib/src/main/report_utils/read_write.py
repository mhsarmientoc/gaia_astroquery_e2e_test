"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on  16 Sep. 2020
"""

import os
import re
import src.main.report_utils.html_wrapper as html_wrapper
import src.main.report_utils.html_table_creator as html_table_creator
import src.main.report_utils.misc as misc
import src.main.tests_constants.test_conditions_oper as common_const
from os import listdir
from os.path import isfile, join


def read(path):
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def create_file(path):

    my_f = open(path, "w+", encoding="utf-8")
    my_f.close()
    print("Created file", path)


def write(content, filepath):
    my_f = open(filepath, "w", encoding="utf-8")
    my_f.write(content)
    my_f.close()
    print("Wrote the file to", filepath)


def append(content, filepath):
    print("Append content to file: ", filepath)
    my_f = open(filepath, "a", encoding="utf-8")
    my_f.write(content+"\n")
    my_f.close()


def read_toml(path):
    print("Reading toml data")
    raw_data = misc.Misc(read(path)).data
    return raw_data


def get_all_files(path):
    """
    use with output of get_all_file_files to read all toml files of the base path
    """
    file_list = [f for f in listdir(path) if isfile(join(path, f))]

    documents = []
    for file in file_list:
        file_path = os.path.join(path, file)
        raw_data = misc.Misc(read(file_path)).data
        raw_data["filepath"] = file_path
        documents.append(raw_data)
    return documents


def ensure_write_safety(mypath):
    if not path_exist(mypath):
        make_path(mypath)


def path_exist(mypath):
    return os.path.isdir(mypath)


def make_path(mypath):
    os.mkdir(mypath)


def create_html(raw_data):
    html_table = create_html_table(raw_data)

    # CREATE VALID HTML, COMBINING SCRIPT AND TABLE:
    html = html_wrapper.HTMLWrapper(html_table, common_const.E2E_REPORT_TITLE,
                                    common_const.ASTROQUERY_VERSION)
    return html.make()


def create_html_table(raw_data):
    """returns an html table containing the attributes of the experiment"""
    html_table = html_table_creator.HTMLTableCreator(
        raw_data, strict_mode=True)
    return html_table.make()


def regex_remove(pattern, string):
    return re.sub(pattern, " ", string)
