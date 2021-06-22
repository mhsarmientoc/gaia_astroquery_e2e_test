"""
@author: Maria H. Sarmiento Carrión
@contact: mhsarmiento@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 17 Sep. 2020
"""

import requests
import json
import logging


def get_single_value_from_request(requested_url):
    """

    @rtype: basestring
    @param requested_url:
    """

    req_value = requests.get(requested_url)
    value_list = json.loads(req_value.text)["data"]
    if not value_list:
        error_message = "WARNING!!! NO results to return from request_url: " + requested_url
        logging.error(error_message)
        raise ValueError(error_message)

    string_to_return = value_list[0][0]
    return string_to_return

    # end_of_get_single_value_from_request


def get_list_of_values_from_request(requested_url):
    """

    @rtype: List
    @param requested_url:
    """
    req_value = requests.get(requested_url)

    value_list = json.loads(req_value.text)["data"]
    if not value_list:
        error_message = "WARNING!!! NO results to return from request_url: " + requested_url
        logging.error(error_message)
        raise ValueError(error_message)
    return value_list


# end_of_get_list_of_values_from_request


def get_where_condition_from_list(base_url, list_of_values, db_field_name, operator):
    """

    @param base_url:
    @param list_of_values:
    @param db_field_name:
    @param operator:
    @return:
    """
    where_condition = ""

    if not list_of_values:
        error_message = "No results returned!!!!!"
        logging.error(error_message)
        raise ValueError(error_message)

    i = 0
    for value in list_of_values:
        # Build where condition to get the list of instruments
        replace_value = value[0].replace("&", "%26")
        where_condition = where_condition + db_field_name + "%27" + replace_value + "%27"  # OJJJOOOO
        if i < len(list_of_values) - 1:
            where_condition = where_condition + "+" + operator + "+"
        i = i + 1

    request_url = base_url + where_condition
    return request_url

# end_of_get_where_condition_from_list
