"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 05 Sep. 2020
"""

import logging as log

import toml

import src.main.common_utils.test_utils as test_utils
import src.main.report_utils.read_write as io
import src.main.tests_code.gaia_test as mission_e2e_test
import src.main.tests_constants.test_conditions_oper as test_cond_oper
import src.main.tests_constants.test_conditions_dev as test_cond_dev
import src.main.tests_constants.test_conditions_pre as test_cond_pre
import src.main.tests_constants.test_conditions_val as test_cond_val
import src.main.tests_constants.test_common_conditions as test_common
from src import paths

from src import conf


class End2EndTest:
    """
    This class is in charge of executing the tests described in
    ../main/toml_test_description/TestDescription.toml.

    During the execution this class creates a collection with teh results for each test.
    In a second step, this collection with the results will dump into a toml file that will be
    the base to write the output report in html format.
    """

    def __init__(self):
        self.path_2_test_description = paths.path2_TestDescription
        self.test_set = io.read_toml(self.path_2_test_description)

        self.current_env = conf.CURRENT_ENV

        # Get the correct constants depending on the current environment
        self.test_const = None
        if self.current_env == test_common.ENV_DEV:
            self.test_const = test_cond_dev
        elif self.current_env == test_common.ENV_PRE:
            self.test_const = test_cond_pre
        elif self.current_env == test_common.ENV_VAL:
            self.test_const = test_cond_val
        elif self.current_env == test_common.ENV_OPE:
            self.test_const = test_cond_oper
        else:
            error_message = "Environment doesn't exist: " + self.current_env
            raise ValueError(error_message)

    def init(self):
        """
            executes all the e2e for a specific environment
        """
        self.reset_test_set()
        # collect results
        self.run_e2e_tests()

    # __end_of_init

    def reset_test_set(self):
        """
            In some cases the user will not want to start the test from the beginning,
            for example, when debugging test. This methods allows to handle whether start the e2e
            from the very first test or not.

            The result of this method is the *.toml file with the tests containing the field
            ["executed"] set to False.
        """

        if conf.RESET_TEST == "True":
            for test_info in self.test_set:
                self.test_set[test_info]["executed"] = False

        # Updates the test with the value "Executed = False"
        io.write(toml.dumps(self.test_set), self.path_2_test_description)

    # __end_of_reset_test_set

    def write_report_in_toml_format(self, collections):
        """
        This method writes a report in toml format with the results of all the e2e tests

        @param collections: List objects.
        Each item contains the result of the corresponding
            e2e test.
        """

        # Path to store results
        path_to_test_results = paths.path2_E2ETestResults

        io.create_file(path_to_test_results)

        # Update the file with the conditions for each test
        for collection in collections:
            test_title = '[' + collection['test_name'] + ']'
            io.append(test_title, path_to_test_results)

            # Convert to toml format the result of each test.
            toml_string = toml.dumps(collection)

            # Write the result into a file
            io.append(toml_string, path_to_test_results)

    # __end_of_write_report_in_toml_format

    def run_e2e_tests(self, debug=False):
        """
            This method reads a .toml file that contains the description of each test and executes it.

            @param debug: boolean, default False
            @return result_collection: contains the results for the e2e test
        """

        # Keep the results of each test performed
        result_collection = []

        # Read test description
        """if in debug, TestDescription.toml does not get overwritten"""
        for test_info in self.test_set:
            testConditions = self.test_set[test_info]
            if not testConditions["executed"]:
                test_number = testConditions["test_id_number"]
                test_name = testConditions["test_name"]
                log.debug(f'Executing test number {test_number}:{test_name}')
                log.debug(f'-----------------------------------------------')
                # Execute current test
                if test_name in [test_common.TEST_DATALINK, test_common.TEST_DATALINK_COMPARE]:
                    list_of_results = self.execute_test(testConditions)
                    for current_test_dict in list_of_results:
                        result_collection.append(current_test_dict)
                else:
                    current_test_dict = self.execute_test(testConditions)
                    result_collection.append(current_test_dict)

                self.test_set[test_info]["executed"] = True

            # __end_if_not_executed
        # __end_for_loop

        # Write results into a report file
        if result_collection:
            self.write_report_in_toml_format(result_collection)

        if not debug:
            # Updates the test with the value "Executed = true"
            io.write(toml.dumps(self.test_set), self.path_2_test_description)

    # end of run_e2e_test

    def execute_test(self, test_info):
        """
            Identifies the current test and gets the necessary parameters to execute it.
            @param test_info: object, mandatory
            @return:
        """
        # Initialize Test Class
        e2e_test = mission_e2e_test.GaiaTest(self.test_const)

        test_id_number = test_info['test_id_number']
        test_name = test_info['test_name']

        test_results = {'test_name': test_name, 'test_id_number': test_id_number}

        # Get current test
        current_test = test_utils.get_test_description(test_id_number)

        if current_test == test_common.TEST_LOGIN:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.LOGIN)
            test_results = e2e_test.test_login(test_results)
        elif current_test == test_common.TEST_LOGOUT:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.LOGOUT)
            test_results = e2e_test.test_logout(test_results)
        elif current_test == test_common.TEST_QUERY_OBJECT:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.QUERY_OBJECT)
            test_results = e2e_test.test_query_object(test_results)
        elif current_test == test_common.TEST_CONE_SEARCH:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.CONE_SEARCH)
            test_results = e2e_test.test_cone_search(test_results)
        elif current_test == test_common.TEST_GET_PUBLIC_TABLES:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.GET_PUBLIC_TABLES)
            test_results = e2e_test.test_get_public_tables(test_results)
        elif current_test == test_common.TEST_LOAD_TABLE:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.LOAD_TABLE)
            test_results = e2e_test.test_load_table(test_results)
        elif current_test == test_common.TEST_SYNCHRONOUS_QUERY:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.SYNCHRONOUS_QUERY)
            test_results = e2e_test.test_synchronous_query(test_results)
        elif current_test == test_common.TEST_SYNCHRONOUS_ON_THE_FLY_QUERY:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.SYNCHRONOUS_ON_THE_FLY_QUERY)
            test_results = e2e_test.test_synchronous_on_the_fly_query(test_results)
        elif current_test == test_common.TEST_ASYNCHRONOUS_QUERY:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.ASYNCHRONOUS_QUERY)
            test_results = e2e_test.test_asynchronous_query(test_results)
        elif current_test == test_common.TEST_LIST_SHARED_TABLES:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.LIST_SHARED_TABLES)
            test_results = e2e_test.test_shared_table(test_results)
        elif current_test == test_common.TEST_DELETE_TABLE:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.DELETE_TABLE)
            # Basically in order to test the delete we need to perform the same steps as for upload a table into
            # a user schema. For this reason we will re-use one of this methods but filling the test_results obj
            # with the proper content.
            test_results = e2e_test.test_upload_table_from_source(test_results, current_test)
        elif current_test == test_common.TEST_UPLOAD_TABLE_FROM_URL:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.UPLOAD_TABLE_FROM_URL)
            test_results = e2e_test.test_upload_table_from_source(test_results, current_test)
        elif current_test == test_common.TEST_UPLOAD_TABLE_FROM_FILE:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.UPLOAD_TABLE_FROM_FILE)
            test_results = e2e_test.test_upload_table_from_source(test_results, current_test)
        elif current_test == test_common.TEST_UPLOAD_TABLE_FROM_JOB:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.UPLOAD_TABLE_FROM_JOB)
            test_results = e2e_test.test_upload_table_from_job(test_results)
        elif current_test == test_common.TEST_UPLOAD_TABLE_FROM_ASTROPY_TABLE:
            test_results = e2e_test.get_basic_info_from_test_description(test_results,
                                                                         self.test_const.UPLOAD_TABLE_FROM_ASTROPY_TABLE)
            test_results = e2e_test.test_upload_table_from_astropy_table(test_results)
        elif current_test == test_common.TEST_CROSS_MATCH:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.CROSS_MATCH)
            test_results = e2e_test.test_cross_match(test_results)
        elif current_test == test_common.TEST_DATALINK:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.DATALINK)
            test_results = e2e_test.test_datalink(test_results, self.test_const.DATALINK)
        elif current_test == test_common.TEST_DATALINK_COMPARE:
            test_results = e2e_test.get_basic_info_from_test_description(test_results, self.test_const.DATALINK_COMPARE)
            test_results = e2e_test.test_datalink_compare(test_results, self.test_const.DATALINK_COMPARE)
        elif current_test is test_common.TEST_NUMBER_ERROR:
            error_message = f'Test id {test_id_number}:{test_name}, does not exist. Aborting E2E Test'
            raise ValueError(error_message)
        else:
            error_message = f'Not valid option. Aborting E2E Test'
            raise ValueError(error_message)
        # end_if
        # return
        return test_results
    # _end_of_execute_test

# end class
