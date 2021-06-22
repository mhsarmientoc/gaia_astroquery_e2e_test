"""
This class contains the methods than can be re-used from any other python class
@author: Maria H. Sarmiento Carrión
@contact: mhsarmiento@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 16 Sep. 2020
"""

from src.main.tests_constants.test_common_conditions import TEST_SET
import src.main.tests_constants.test_common_conditions as common_conditions


def get_test_description(input_test_number):
    """
            This method uses TEST_SET as a switch case statement of java. It uses de get() method of 'Dictonary'
            to check the type of test to run. If the dictionary does not contain that test then it gives
            back an error.

            Parameters
            ----------
            input_test_number: string

            Returns
            -------
            The KEY_WORD of the test to run
    """

    return TEST_SET.get(input_test_number, common_conditions.TEST_NUMBER_ERROR)

# __end_of_test_utils
