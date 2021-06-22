"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 05 Sep. 2020
"""

from time import sleep
import logging as log
from astroquery.gaia import GaiaClass
from requests import HTTPError
from datetime import datetime
from astropy.coordinates import SkyCoord
from astropy.table import Table
from src.main.tests_code.e2e_test_4_datalink import ReadDataLink
from src import conf, credentials
from src import paths
from pathlib import Path

import copy
import astropy.units as u
import src.main.tests_constants.test_common_conditions as test_common_cons

PASSED = "<span class='passed'><b>PASSED</b></span>"
NOT_PASSED = "<span class='notPassed'><b>NOT_PASSED</b></span>"
TEST_NAME = "<span class='testTitle'><b>@TEST_TITLE@</b></span>"
TEST_NAME_PATTERN = "@TEST_TITLE@"
TABLE_LENGTH = "<Table length="


class GaiaTest:
    def __init__(self, test_conditions_4_current_env):
        """
        This class receives the conditions for the test set that depend on the environment.
        For example, the results expected when the test is executed for dev environment (geadev server)
        """
        # Init Gaia Class
        self.test_conditions_4_current_env = test_conditions_4_current_env
        self.gaia = GaiaClass(gaia_tap_server=conf.HOST_URL, gaia_data_server=conf.HOST_URL)

    # __end_of_init

    def get_basic_info_from_test_description(self, test_results, test_description):
        """
        @param test_results: dict
            Holds the basic info of the current test plus the results from the execution of that test
        @param test_description: dict
            Contains the basic information for the current test
        @return: dict
            test_results updated
        """
        test_info = copy.deepcopy(test_results)
        test_info.update(test_description)

        # Init 'test started'
        time = datetime.now()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        test_info['test_started'] = f'{time_str} CET'

        return test_info

    # __end_of_get_basic_info_from_test_description

    def test_login(self, test_results):
        """
            @param test_results
            Basic content for the current test
            @return test_login:
            Dict with the results of the current test
        """

        # prepare test results object for LOGIN test
        test_login = test_results

        # Execute Test
        try:
            # Get the path to the credentials file
            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)
            test_login['test_result'] = PASSED

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_login['test_finished'] = f'{time_str} CET'
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_login['test_finished'] = f'{time_str} CET'
            test_login['test_result'] = NOT_PASSED
            test_login['test_additional_info'] = error_message + "," + str(err)

            log.debug('Test - #1 "Login" Done')
            return test_login
        log.debug('Test - #1 "Login" Done')
        return test_login

    # __end_of_login

    def test_logout(self, test_results):
        """
            @param test_results: dict
            Basic content for the current test
            @return test_logout: Dict with the results of the current test

        """

        test_logout = test_results

        # Execute test
        try:

            self.gaia.logout()
            test_logout['test_result'] = PASSED

            log.debug("Test PASSED")

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_logout['test_finished'] = f'{time_str} CET'
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_logout['test_finished'] = f'{time_str} CET'
            test_logout['test_result'] = NOT_PASSED
            test_logout['test_additional_info'] = error_message + "," + str(err)
            return test_logout

        return test_logout

    # __end_of_logout

    def test_query_object(self, test_info):
        """
            This test sends a request to the gaia Tap with the coordinates of the object. For this, the
            test uses SkyCoord in first place in order to resolve an object by its ICRS sky position.

            @param test_info: dict
                Contains the basic info for the test to be performed
            @return: test_results, dict
                Returns a dict with the information resulting from the test run
        """

        test_results = test_info

        # Prepare the test
        input_ra = test_results['test_RA']
        input_dec = test_results['test_DEC']
        input_units = test_results['test_units']
        input_frame = test_results['test_frame']
        input_size = int(test_results['side_size'])

        # Launch the test
        try:
            coord = SkyCoord(ra=input_ra, dec=input_dec, unit=(input_units, input_units), frame=input_frame)
            width = u.Quantity(input_size, input_units)
            height = u.Quantity(input_size, input_units)
            r = self.gaia.query_object_async(coordinate=coord, width=width, height=height)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # Store additional info
            test_results['test_additional_info'] = str(r)

            # Get num of results returned, if it is the expected then the test has been passed.
            log.debug(f'Num rows returned: {len(r)}')

            n_expected_results = test_results['test_expected_value']
            if len(r) == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of rows returned: {len(r)} differs from the expected {n_expected_results}'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)
        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results
        # if everything is correct then we will return the results of the test
        return test_results

    # __end_of_test_query_object

    def test_cone_search(self, test_info):
        """
            This test sends a request to the gaia Tap with the coordinates of the object. For this, the
            test uses SkyCoord in first place in order to resolve an object by its ICRS sky position.

            @param test_info: dict
                Contains the basic info for the test to be performed
            @return: test_results, dict
                Returns a dict with the information resulting from the test run
        """

        test_results = test_info

        # Prepare the test
        input_ra = test_results['test_RA']
        input_dec = test_results['test_DEC']
        input_units = test_results['test_units']
        input_frame = test_results['test_frame']
        input_radius = int(test_results['test_radius'])

        try:
            # Launch the test
            coord = SkyCoord(ra=input_ra, dec=input_dec, unit=(input_units, input_units), frame=input_frame)
            radius = u.Quantity(input_radius, input_units)
            j = self.gaia.cone_search_async(coord, radius)
            r = j.get_results()

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # Store additional info
            test_results['test_additional_info'] = str(r)

            # Get num of results returned, if it is the expected then the test has been passed.
            log.debug(f'Num rows returned: {len(r)}')

            n_expected_results = test_results['test_expected_value']
            if len(r) == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of rows returned: {len(r)} differs from the expected {n_expected_results}'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)
        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results

        # if everything is correct then we will return the results of the test
        return test_results

    # __end_of_test_cone_search

    def test_get_public_tables(self, test_info):
        """
        Send Request to the gaia tap to retrieve the list of public tables

        @param test_info: dict
            Contains the basic info for the test to be performed
        @return: test_results, dict
            Returns a dict with the information resulting from the test run
        """

        list_of_public_tables = ['This is the list of public tables:']
        test_results = test_info

        # Execute the test
        try:
            tables = self.gaia.load_tables(only_names=True)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            for table in tables:
                list_of_public_tables.append(str(table.get_qualified_name() + ",\n"))
                log.debug(table.get_qualified_name())
            test_results['test_additional_info'] = list_of_public_tables

            # Get num of results returned, if it is the expected then the test has been passed.
            log.debug(f'Num tables returned: {len(tables)}')

            n_expected_results = test_results['test_expected_value']
            if len(tables) == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of tables returned: {len(tables)} differs from the expected' \
                                f' {n_expected_results}'
                log.error(error_message)
                test_results['test_additional_info'] = error_message
                raise ValueError(error_message)

            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results
        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results

    # __end_of_test_get_public_tables

    def test_load_table(self, test_info):
        """
        Test the TAP+ capability that enables the user to load only one table.

        @param test_info: dict
            Contains the basic info for the test to be performed
        @return: test_results, dict
            Returns a dict with the information resulting from the test run
        """

        test_results = test_info

        # STEP-1:  get table selected for the test from the dict of conditions for this test
        # -------------------------------------------------------------------------------------

        full_qualified_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN. \
            replace(test_common_cons.SCHEMA_PATTERN, test_results['schema_name'])
        full_qualified_name = full_qualified_name.replace(test_common_cons.TABLE_NAME_PATTERN,
                                                          test_results['gaia_table_name'])
        # execute request
        try:
            tables = self.gaia.load_table(full_qualified_name)

            # STEP-2: Update the info of the request sent for the test with the table selected.
            # -------------------------------------------------------------------------------------
            test_results['request_sent'] = test_results['request_sent'].replace(test_common_cons.TABLE_NAME_PATTERN,
                                                                                full_qualified_name)
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            test_results['test_additional_info'] = str(tables)

            # STEP-3: Get num of results returned, if it is the expected then the test has been passed.
            # -------------------------------------------------------------------------------------
            log.debug(f'Num tables returned: {len(tables.columns)}')

            n_expected_results = test_results['test_expected_value']
            if len(tables.columns) == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of columns returned: {len(tables.columns)} differs from the expected' \
                                f' {n_expected_results}'
                log.error(error_message)
                test_results['test_additional_info'] = error_message
                raise ValueError(error_message)
            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results

    # __end_of_test_load_table

    def test_synchronous_query(self, test_info):
        """
        Test synchronous query. Type of request does not store the results at server side.
        Suitable when the amount of data to be retrieved is 'small'

        @param test_info: dict
            Contains the basic info for the test to be performed
        @return: test_results, dict
            Returns a dict with the information resulting from the test run
        """

        test_results = test_info

        # STEP-1: get table selected for the test from the dict of conditions for this test
        # -------------------------------------------------------------------------------------
        full_qualified_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN \
            .replace(test_common_cons.SCHEMA_PATTERN, test_results['schema_name'])
        full_qualified_name = full_qualified_name.replace(test_common_cons.TABLE_NAME_PATTERN,
                                                          test_results['gaia_table_name'])

        # execute request
        test_query = test_results['test_query'].replace(test_common_cons.FULL_QUALIFIED_PATTERN, full_qualified_name)
        # Update the template query with the real query that is going to be used to execute this test.
        test_results['test_query'] = test_query

        try:
            job = self.gaia.launch_job(test_query, dump_to_file=False)

            # Update the info of the request sent for the test with the table selected.
            test_results['request_sent'] = test_results['request_sent']. \
                replace(test_common_cons.QUERY_PATTERN, test_query)
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')
            test_results['test_finished'] = f'{time_str} CET'

            # Get num of results returned, if it is the expected then the test has been passed.
            r = job.get_results()
            n_rows_returned = len(job.get_results())

            # Save the additional info
            test_results['test_additional_info'] = str(r['solution_id'])

            log.debug(f'Num rows returned: {n_rows_returned}')

            n_expected_results = test_results['test_expected_value']
            if n_rows_returned == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of rows returned: {n_rows_returned} differs from the expected ' \
                                f'{n_expected_results}'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)
        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results

        return test_results

    # __end_of_test_synchronous_query

    def test_synchronous_on_the_fly_query(self, test_info):

        """
        Test synchronous_on_the_fly_query.
        This test shows how a table can be uploaded to the server in order to be used in a query.

        @param test_info: dict
            Contains the basic info for the test to be performed
        @return: test_results, dict
            Returns a dict with the information resulting from the test run
        """
        test_results = test_info

        # get table selected for the test from the dict of conditions for this test
        table_name = test_results['test_table']

        # Prepare the query for the test
        test_query = test_results['test_query'] \
            .replace(test_common_cons.TABLE_NAME_PATTERN, table_name)
        # Update the template query with the real query that is going to be used to execute this test.
        test_results['test_query'] = test_query

        upload_resource = paths.path2_example_tb_4_onthefly

        # Update the info of the request sent for the test with the table selected.
        test_results['request_sent'] = test_results['request_sent']. \
            replace(test_common_cons.QUERY_PATTERN, test_query)
        test_results['request_sent'] = test_results['request_sent']. \
            replace(test_common_cons.TABLE_NAME_PATTERN, table_name)

        # Execute test
        try:
            job = self.gaia.launch_job(query=test_query, upload_resource=upload_resource,
                                       upload_table_name=table_name, verbose=True)
            results = job.get_results()
            results.pprint()

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # Get num of results returned, if it is the expected then the test has been passed.
            n_rows_returned = len(results)

            # Save the additional info
            test_results['test_additional_info'] = str(results)

            log.debug(f'Num rows returned: {n_rows_returned}')

            n_expected_results = test_results['test_expected_value']
            if n_rows_returned == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of rows returned: {n_rows_returned} differs from the expected' \
                                f' {n_expected_results}'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)
        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results

        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results

        return test_results

    # __end_of_test_synchronous_on_the_fly_query

    def test_asynchronous_query(self, test_results):
        """
        Test asynchronous query. These type of queries save results at server
        side and can be accessed at any time. The results can be saved in memory (default) or in a file.'

        @param test_results: dict
            Contains the basic info for the test to be performed
        @return: test_results, dict
            Returns a dict with the information resulting from the test run
        """

        test_results = test_results

        # get table selected for the test from the dict of conditions for this test
        full_qualified_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN \
            .replace(test_common_cons.SCHEMA_PATTERN, test_results['schema_name'])
        full_qualified_name = full_qualified_name.replace(test_common_cons.TABLE_NAME_PATTERN,
                                                          test_results['gaia_table_name'])

        # execute request
        test_query = test_results['test_query'].replace(test_common_cons.FULL_QUALIFIED_PATTERN, full_qualified_name)

        # Update the template query with the real query that is going to be used to execute this test.
        test_results['test_query'] = test_query

        # Update the info of the request sent for the test with the table selected.
        test_results['request_sent'] = test_results['request_sent']. \
            replace(test_common_cons.QUERY_PATTERN, test_query)

        # we declare here job because we will use it to add more info to the error message
        job = None
        try:
            job = self.gaia.launch_job_async(test_query, dump_to_file=False)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')
            test_results['test_finished'] = f'{time_str} CET'

            # Get num of results returned, if it is the expected then the test has been passed.
            r = job.get_results()

            # Get number of results returned
            n_rows_returned = len(job.get_results())

            # Save the additional info
            test_results['test_additional_info'] = str(r['solution_id'])

            log.debug(f'Num rows returned: {n_rows_returned}')

            n_expected_results = test_results['test_expected_value']
            if n_rows_returned == n_expected_results:
                # Test passed
                test_results['test_result'] = PASSED
                log.debug("Test PASSED")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of rows returned: {n_rows_returned} differs from the expected ' \
                                f'{n_expected_results}'
                log.error(error_message)
                test_results['test_additional_info'] = error_message
                raise ValueError(error_message)

            # Finally remove the job that we just created with the asynchronous query.
            self.gaia.remove_jobs(job.jobid)
        except ValueError as err:

            # Finally remove the job that we just created with the asynchronous query.
            self.gaia.remove_jobs(job.job_id)
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            return test_results
        except HTTPError as err:
            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            return test_results

        # Everything is OK, returning results
        return test_results

    # __end_of_test_asynchronous_query

    def test_shared_table(self, test_info):
        """
            This test list all tables, public and shared (Tap + Capability). For the test to be correct
            the number of results returned must be major or equal to the number of public tables.

        @param test_info: dict
            Contains the basic info for the test to be performed
        @return: test_results, dict
            Returns a dict with the information resulting from the test run
        """

        test_results = test_info

        # execute request
        try:

            # Step 1: Get the list of public tables
            tables = self.gaia.load_tables(only_names=True)
            # Now we will keep the number of results returned
            n_public_tables = len(tables)
            log.debug(f'N public tables is {n_public_tables}')

            # Step 2: Now we need to do login in to de Gaia Tap.

            # Now we can do the login()
            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)

            # Step 3: Now we are going to execute again 'load_tables' but now specifying that we also want to list
            # the tables that we are sharing with other users from our user_schema.
            all_tables = self.gaia.load_tables(only_names=True, include_shared_tables=True)
            # Let's keep now the number of results returned
            n_shared_tables = len(all_tables)
            log.debug(f'N all tables is {n_shared_tables}')

            # Step 4: Finally we will do a logout from the system.
            self.gaia.logout()

            # Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # Now let's have a look at the results for our test. If the number of tables returned as this second step
            # is equal or higher than the number of public tables the test is correct.
            if n_public_tables <= n_shared_tables:
                # Test passed
                test_results['test_result'] = PASSED
                debug_message = f'The number of shared tables: {n_shared_tables} is major or equal than the number ' \
                                f'of public tables: {n_public_tables}'
                log.debug(debug_message)
                test_results['test_additional_info'] = debug_message + " Test PASSED!"
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f'The number of shared tables: {n_shared_tables} is less than the number ' \
                                f'of public tables: {n_public_tables}'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)
            self.gaia.logout()
            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            self.gaia.logout()
            return test_results
        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return test_results

    # __end_of_test_shared_table

    def test_upload_table_from_source(self, test_info, current_test):
        """
            This test checks the possibility of persisting a table in the private user space from source.
            this source can be an url or a local file.

            @param test_info: dict
                Contains the basic info for the test to be performed
            @param current_test: boolean
                in order to test the feature of deleting a table we need to execute the same workflow
                as for the test of the upload capability. Only changes the info to display at the end of
                the test. For this reason we made this method re-usable by using a boolean that tell us
                when to change the info returned.
            @return: test_results, dict
                Returns a dict with the information resulting from the test run
        """

        test_results = test_info

        if current_test == 'DELETE_TABLE':
            log.debug('Executing Test - "Delete table from user area"')
        else:
            log.debug('Executing Test - "Upload table on the fly and query it"')

        # execute request
        try:

            # Step 1: Read user name from credentials file. (we will use it later) and do Login()
            # -----------------------------------------------------------------------------------

            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)

            # Step 2: Check if table already exist. If it does, then deleted it before run the script
            # -----------------------------------------------------------------------------------------
            table_name = test_results['table_name']

            try:
                self.gaia.delete_user_table(table_name)
            except:
                log.warning(f"Table {table_name}  didn't exist. Continuing...")

            # Step 3: Upload table from resource
            # -----------------------------------------------------------------------------------------
            test_resource = paths.path2_example_tb_4_onthefly
            table_description = test_results['table_description']
            self.gaia.upload_table(upload_resource=test_resource, table_name=table_name,
                                   table_description=table_description)
            sleep(int(conf.TIME_OUT))

            # Step 4: Query the new table
            # -----------------------------------------------------------------------------------------

            # Use the user name that we obtained before to replace the pattern in
            # 'user_@LOGIN_USER@.table_test_from_url'

            full_qualified_table_name = test_common_cons.FULL_QUALIFIED_USER_TABLE_NAME_PATTERN. \
                replace(test_common_cons.LOGIN_USER_PATTERN, credentials.USERNAME)
            full_qualified_table_name = full_qualified_table_name.replace(test_common_cons.TABLE_NAME_PATTERN,
                                                                          table_name)

            # Now replace the pattern in Query with its correct value
            query = test_results['test_query'].replace(test_common_cons.TABLE_NAME_PATTERN, full_qualified_table_name)

            # Now we are ready to query the new table
            job2 = self.gaia.launch_job(query=query)
            results = job2.get_results()

            log.debug(str(results))

            n_results = len(results)
            log.debug(f'N results from the table upload from URL is {n_results}')

            # Step 5: Delete now the table from the user schema.
            # -----------------------------------------------------------------------------------------
            job_delete = None
            try:
                job_delete = self.gaia.delete_user_table(table_name)
            except:
                log.warning(f"Table {table_name}  didn't exist. Continuing...")

            # Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            if current_test == 'DELETE_TABLE':
                try:
                    error_message = "Ooops! Something went wrong. Table still exist in user space."
                    job = self.gaia.launch_job(query=query)
                    job.get_results()
                    log.debug(str(job_delete) + "_:" + error_message)
                    test_results['test_result'] = NOT_PASSED
                    test_results['test_additional_info'] = error_message + "," + str(job_delete)

                except HTTPError as err:

                    # if the table does not exist. TAP gives back an http error. In order to check if the test of the
                    # delete table is correct, we are going to check the content of that HTTPError.
                    error_message = f'Query did not give back any result because {full_qualified_table_name} does ' \
                                    f'not exist in the user space '

                    if table_name in str(err):
                        log.debug(error_message)
                        test_results['test_result'] = PASSED
                        test_results['test_additional_info'] = error_message

                    else:
                        test_results['test_result'] = NOT_PASSED
                        test_results['test_additional_info'] = error_message + "," + str(err)
                        log.debug(error_message)

                    # Step 6: Finally we will do a logout from the system before returning the results after the
                    # exception.
                    # -----------------------------------------------------------------------------------------

                    self.gaia.logout()
                    return test_results
            else:
                # We are not testing the delete of the tables so we will focus on the results returned in order to check
                # if the test is correct or not.

                if n_results > 0:
                    # Test passed
                    test_results['test_result'] = PASSED
                    debug_message = f' Number of results from the table upload from the url provided is {n_results}'
                    test_results['test_additional_info'] = debug_message + str(results)
                    log.debug(debug_message + " TEST PASSED!!!")
                else:
                    test_results['test_result'] = NOT_PASSED
                    error_message = f' Number of results from the table upload from the url provided is {n_results}' \
                                    f' or something happened. FAILED TEST'
                    test_results['test_additional_info'] = error_message
                    log.debug(error_message)
                    raise ValueError(error_message)

            # Step 6: Finally we will do a logout from the system.
            # -----------------------------------------------------------------------------------------
            self.gaia.logout()
            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            self.gaia.logout()
            return test_results

        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return test_results

    # __end_of_test_upload_table_from_resource

    def test_upload_table_from_job(self, test_info):
        """
             This test checks the possibility of persisting a table in the private user space from source.
             this source can be an url or a local file.

             @param test_info: dict
                 Contains the basic info for the test to be performed
             @return: test_results, dict
                 Returns a dict with the information resulting from the test run
         """

        test_results = test_info

        # execute request
        try:

            # Step 1: Read user name from credentials file. (we will use it later) and do Login()
            # -----------------------------------------------------------------------------------

            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)

            # Step 2: Execute query, we will keep the job_id returned.
            # --------------------------------------------------------

            # get query from dictionary of constants
            full_qualified_name_gaia = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN. \
                replace(test_common_cons.SCHEMA_PATTERN, conf.DB_SCHEMA_NAME)
            full_qualified_name_gaia = full_qualified_name_gaia. \
                replace(test_common_cons.TABLE_NAME_PATTERN, conf.GAIA_SOURCE_DB_NAME)

            query = test_results['test_query'].replace(test_common_cons.FULL_QUALIFIED_PATTERN,
                                                       full_qualified_name_gaia)
            test_results['request_sent'] = test_results['request_sent'] \
                .replace(test_common_cons.FULL_QUALIFIED_PATTERN, full_qualified_name_gaia)

            # Step 3: Upload table form job_id. we will keep the job_id returned
            # ------------------------------------------------------------------
            j1 = self.gaia.launch_job_async(query)

            # we will keep the jobId for later. We will identify the table with it so we can remove it
            # from the user space after the test is run.
            table_from_job_id = j1.jobid
            table_from_job_id = 't' + table_from_job_id

            # now we will proceed to upload the table from the job
            job = self.gaia.upload_table_from_job(j1)
            log.debug(str(job))

            # Step 4: Query the table that we have just upload.
            # --------------------------------------------------------
            full_qualified_user_table_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_JOB_ID_PATTERN. \
                replace(test_common_cons.LOGIN_USER_PATTERN, credentials.USERNAME)
            full_qualified_user_table_name = full_qualified_user_table_name. \
                replace(test_common_cons.JOB_ID_PATTERN, table_from_job_id)

            query_new_table = 'select * from ' + full_qualified_user_table_name
            job_query = self.gaia.launch_job(query=query_new_table)
            results = job_query.get_results()

            log.debug(str(results))

            n_results = len(results)
            log.debug(f'N results from the table upload from jobId is {n_results}')

            # Step 5: Delete now the table from the user schema.
            try:
                self.gaia.delete_user_table(table_from_job_id)
            except:
                log.warning(f"Table {table_from_job_id} didn't exist. Continuing...")

            # Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # We are not testing the delete of the tables so we will focus on the results returned in order to check
            # if the test is correct or not.

            if n_results >= test_results['n_expected_results']:
                # Test passed
                test_results['test_result'] = PASSED
                debug_message = f' Number of results from the table upload from the job is {n_results}'
                test_results['test_additional_info'] = debug_message + str(results)
                log.debug(debug_message + " TEST PASSED!!!")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f' Number of results from the table upload from the job is {n_results}' \
                                f' or something happened. FAILED TEST'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)

            # Step 5: Finally we will do a logout from the system.
            self.gaia.logout()
            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            self.gaia.logout()
            return test_results

        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return test_results

    # __end_of_test_upload_table_from_job

    def test_upload_table_from_astropy_table(self, test_info):
        """
             This test checks the possibility of persisting a table in the private user space from source.
             In this case the source is an Astropy table.

             @param test_info: dict
                 Contains the basic info for the test to be performed
             @return: test_results, dict
                 Returns a dict with the information resulting from the test run
         """

        test_results = test_info

        # execute request
        try:

            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)

            # Step 1: create an astroquery table. We will upload this table later
            # --------------------------------------------------------
            a = [1, 2, 3]
            b = ['a', 'b', 'c']
            table_name = test_results['table_name']
            table = Table([a, b], names=['col1', 'col2'], meta={'meta': table_name})

            # Step 0 Check if the table exist in the user schema from previous tests. If it does. Delete it.
            try:
                self.gaia.delete_user_table(table_name)
            except:
                log.warning(f"Table {table_name} didn't exist. Continuing...")

            # Step 2: Upload AstroPy table
            # ------------------------------------------------------------------
            self.gaia.upload_table(upload_resource=table, table_name=table_name)

            # Step 3: Query the table that we have just upload..
            # --------------------------------------------------------

            full_qualified_user_table_name = test_common_cons.FULL_QUALIFIED_USER_TABLE_NAME_PATTERN. \
                replace(test_common_cons.LOGIN_USER_PATTERN, credentials.USERNAME)
            full_qualified_user_table_name = full_qualified_user_table_name. \
                replace(test_common_cons.TABLE_NAME_PATTERN, table_name)

            query_new_table = 'select * from ' + full_qualified_user_table_name
            job_query = self.gaia.launch_job(query=query_new_table)
            results = job_query.get_results()

            log.debug(str(results))

            n_results = len(results)
            log.debug(f'N results from the table upload from AstroPy is {n_results}')

            # STEP-4: Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # We are not testing the delete of the tables so we will focus on the results returned in order to check
            # if the test is correct or not.

            if n_results >= test_results['n_expected_results']:
                # Test passed
                test_results['test_result'] = PASSED
                debug_message = f' Number of results from the table upload from AstroPy is {n_results}'
                test_results['test_additional_info'] = debug_message + str(results)
                log.debug(debug_message + " TEST PASSED!!!")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f' Number of results from the table upload from AstroPy is {n_results}' \
                                f' something happened. FAILED TEST'
                test_results['test_additional_info'] = error_message
                log.debug(error_message)
                raise ValueError(error_message)

            # Step 5: Finally we will do a logout from the system.
            self.gaia.logout()
            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            self.gaia.logout()
            return test_results

        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return test_results

    # __end_of_test_upload_table_from_astropy_table

    def test_cross_match(self, test_info):
        """
             This tests execute a cross match between tables based on distance

             @param test_info: dict
                 Contains the basic info for the test to be performed
             @return: test_results, dict
                 Returns a dict with the information resulting from the test run
         """

        test_results = test_info

        # execute request
        try:
            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)
            # -----------------------------
            # Step 1: Delete previous tables
            # -------------------------------
            try:
                self.gaia.delete_user_table(test_results['user_table'])
            except:
                log.warning("Table user_table didn't exist. Continuing...")
                log.warning(f"Error message: {test_results['user_table']}")
            try:
                self.gaia.delete_user_table(test_results['xmatch_table_name'])
            except:
                log.warning("Table user_table didn't exist. Continuing...")
                log.warning(f"Error message: {test_results['xmatch_table_name']}")

            # --------------

            # Step 2: Upload table from resource
            test_resource = paths.path2_example_table_for_tests
            table_name = test_results['user_table']

            self.gaia.upload_table(upload_resource=test_resource, table_name=table_name)
            # we add a sleep(conf.TIME_OUT) here to give time to the tap server to upload the table
            # sleep(int(conf.TIME_OUT))

            # Prepare the qualified name with the table that we have just upload and the user schema name
            # of the user that we are using for this test.

            full_qualified_table_name_b = test_common_cons.FULL_QUALIFIED_USER_TABLE_NAME_PATTERN. \
                replace(test_common_cons.LOGIN_USER_PATTERN, credentials.USERNAME)
            full_qualified_table_name_b = full_qualified_table_name_b. \
                replace(test_common_cons.TABLE_NAME_PATTERN, table_name)

            # Get full_qualified_table_name (e.g: gaiadr2.gaia_source)
            full_qualified_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN. \
                replace(test_common_cons.SCHEMA_PATTERN, conf.DB_SCHEMA_NAME)
            full_qualified_name = full_qualified_name. \
                replace(test_common_cons.TABLE_NAME_PATTERN, conf.GAIA_SOURCE_DB_NAME)

            # Update the info of the test that we will provide in the report result
            test_results['request_sent'] = test_results['request_sent'] \
                .replace(test_common_cons.FULL_QUALIFIED_PATTERN, full_qualified_name)

            # Now we need to define which are the ra/dec columns of my new table

            self.gaia.set_ra_dec_columns(table_name=table_name, ra_column_name='ra',
                                         dec_column_name='dec')

            # the table will be uploaded into the user private space into the database
            # the table can be referenced as <database user schema>.<table_name>

            # Step 3: Prepare the xmatch between the table resource used for this test and
            # gaiadr2.gaia_source.
            # ---------------------------------------------------------------------------------

            # Get the table name that we want to use for the xmatch
            xmatch_table_name = test_results['xmatch_table_name']

            # With all that information we can launch now the Xmatch
            self.gaia.cross_match(full_qualified_table_name_a=full_qualified_name,
                                  full_qualified_table_name_b=full_qualified_table_name_b,
                                  results_table_name=xmatch_table_name, radius=1.0)

            # STEP 4 - Test the results obtained.
            # ------------------------------------------------------------------------------------------------------
            # Once you have your cross match finished, you can obtain the results. For this first we need to prepare
            # the query.

            xmatch_qualified_table_name = test_common_cons.FULL_QUALIFIED_USER_TABLE_NAME_PATTERN. \
                replace(test_common_cons.LOGIN_USER_PATTERN, credentials.USERNAME)
            xmatch_qualified_table_name = xmatch_qualified_table_name.replace(test_common_cons.TABLE_NAME_PATTERN,
                                                                              xmatch_table_name)

            # Replace Values in query

            query_new_xmatch_table = f' SELECT c."dist", a.*, b.* FROM {full_qualified_name} AS a, ' \
                                     f' {full_qualified_table_name_b} AS b,' \
                                     f' {xmatch_qualified_table_name} AS c ' \
                                     f' WHERE (c.gaia_source_source_id = a.source_id ' \
                                     f'AND c.{table_name}_{table_name}_oid ' \
                                     f'= b.{table_name}_oid)'

            log.debug(f'query xmatch table {query_new_xmatch_table}')

            job_query = self.gaia.launch_job(query=query_new_xmatch_table)
            results = job_query.get_results()

            log.debug(str(results))

            n_results = len(results)
            log.debug(f'N results from xmatch table is {n_results}')

            # Step 5: Delete now the table from the user schema.
            # -----------------------------
            try:
                self.gaia.delete_user_table(test_results['user_table'])
            except:
                log.warning("Table user_table didn't exist. Continuing...")
                log.warning(f"Error message: {test_results['user_table']}")
            try:
                self.gaia.delete_user_table(test_results['xmatch_table_name'])
            except:
                log.warning("Table user_table didn't exist. Continuing...")
                log.warning(f"Error message: {test_results['xmatch_table_name']}")

            # Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            test_results['test_finished'] = f'{time_str} CET'

            # We are not testing the delete of the tables so we will focus on the results returned in order to check
            # if the test is correct or not.

            if n_results >= test_results['n_expected_results']:
                # Test passed
                test_results['test_result'] = PASSED
                debug_message = f' Number of results from the xmatch table is {n_results}'
                test_results['test_additional_info'] = str(debug_message)
                log.debug(debug_message + " TEST PASSED!!!")
            else:
                test_results['test_result'] = NOT_PASSED
                error_message = f' Number of results from the xmatch table is {n_results}' \
                                f' or something happened. FAILED TEST'
                test_results['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)

            # Step 5: Finally we will do a logout from the system.
            self.gaia.logout()
            return test_results

        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = str(err)
            self.gaia.logout()
            return test_results

        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            test_results['test_finished'] = f'{time_str} CET'
            test_results['test_result'] = NOT_PASSED
            test_results['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return test_results

    # __end_of_test_cross_match

    def test_datalink(self, test_info, basic_datalink_info_4_test):
        """
             This tests execute a cross match between tables based on distance

             @param test_info: dict
                 Contains the basic info for the test to be performed
             @param basic_datalink_info_4_test: str
                name of the data_type that is being tested
             @return: return list of dict
                 Returns a list of dicts with the information resulting from the test run
         """

        test_results = test_info
        list_of_results = []

        test_number = test_results['test_id_number'].replace('#', '')

        for data_release in self.test_conditions_4_current_env.GAIA_RELEASES:

            dict_retrieval_types = self.test_conditions_4_current_env.DATALINK_RETRIEVAL_TYPES[data_release]
            # execute request
            for data_retrieval_type in dict_retrieval_types.keys():
                new_item = self.execute_datalink_4_current_data_type(data_retrieval_type, test_results,
                                                                     dict_retrieval_types, basic_datalink_info_4_test,
                                                                     data_release)
                new_item['test_id_number'] = f'#{test_number}'
                my_new_item = new_item.copy()
                list_of_results.append(my_new_item)
                test_number = int(test_number) + 1
            print(len(list_of_results))
        return list_of_results

    # __end_of_test_datalink

    def execute_datalink_4_current_data_type(self, data_retrieval_type, test_results, dict_retrieval_types,
                                             basic_datalink_info_4_test, current_gaia_data_release):
        """

        :param data_retrieval_type:
        :param test_results:
        :param dict_retrieval_types:
        :param basic_datalink_info_4_test:
        :param current_gaia_data_release:
        :return:
        """
        # copy test
        new_item = self.get_basic_info_from_test_description(test_results, basic_datalink_info_4_test)

        # get current user_schema
        current_user_schema = self.test_conditions_4_current_env.GAIA_RELEASES[current_gaia_data_release]
        try:
            # update test name
            new_item['test_name'] = 'DATALINK_' + current_gaia_data_release.replace(" ",
                                                                                    "_") \
                                    + "_" + data_retrieval_type.upper()

            # update test description
            new_item['test_description'] = new_item['test_description'] \
                .replace(test_common_cons.RETRIEVAL_TYPE_PATTERN, data_retrieval_type)

            # Execute
            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)

            # STEP 1 - Get query to retrieve the IDs that we need
            # -----------------------------------------------------
            n_results_expected = dict_retrieval_types[data_retrieval_type]

            # get gaia_data_source table. eg. gaiadr2.gaia_source
            full_qualified_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN. \
                replace(test_common_cons.SCHEMA_PATTERN, current_user_schema)
            full_qualified_name = full_qualified_name. \
                replace(test_common_cons.TABLE_NAME_PATTERN, conf.GAIA_SOURCE_DB_NAME)

            # Update query with current retrieval type
            query = new_item[current_gaia_data_release].replace(test_common_cons.FULL_QUALIFIED_PATTERN,
                                                                full_qualified_name)

            # Update request_sent description
            new_item['request_sent'] = new_item['request_sent'].replace(test_common_cons.QUERY_PATTERN, query)
            new_item['request_sent'] = new_item['request_sent'].replace(test_common_cons.RETRIEVAL_TYPE_PATTERN,
                                                                        data_retrieval_type)

            # -----------------------------------------------------------------------------
            # TODO: Execute these code to get new set of IDS per Gaia Release. With them
            # update the tests conditions of 'DATALINK_COMPARE' stored in the file
            # 'test_conditions_<env>.py'
            # -----------------------------------------------------------------------------
            # job = self.gaia.launch_job(query)
            # results = job.get_results()
            # ids = results['source_id']
            # if len(results) <= 0:
            #       new_item['test_result'] = NOT_PASSED
            #       error_message = f' Number of results from the {data_retrieval_type} request is 0. FAILED TEST'
            #       new_item['test_additional_info'] = error_message
            #       log.error(error_message)
            #       raise ValueError(error_message)
            # -----------------------------------------------------------------------------
            ids = test_results[f'{current_gaia_data_release}_IDS']
            # -----------------------------------------------------------------------------

            # STEP 3 - Retrieve epoch photometry data
            data_release = current_gaia_data_release

            # data_retrieval_type = "XP_CONTINUOUS"

            test_data_link = self.gaia.load_data(ids=ids, data_release=data_release,
                                                 retrieval_type=data_retrieval_type)

            n_results = len(test_data_link)

            log.debug(f'N results from {data_retrieval_type} query is {n_results}')

            # Step 4: Check results

            # Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            new_item['test_finished'] = f'{time_str} CET'

            # We are not testing the delete of the tables so we will focus on the results returned in order to check
            # if the test is correct or not.

            if n_results == n_results_expected:
                # Test passed
                new_item['test_result'] = PASSED
                debug_message = f' Number of results from the xmatch table is {n_results}'
                new_item['test_additional_info'] = debug_message

                log.debug(debug_message + " TEST PASSED!!!")
            else:
                new_item['test_result'] = NOT_PASSED
                error_message = f' Number of results from the {data_retrieval_type} request is {n_results}' \
                                f' but the number of the results expected is {n_results_expected}. FAILED TEST'
                new_item['test_additional_info'] = error_message

                log.error(error_message)
                raise ValueError(error_message)

            # Step 5: Finally save the results and we do a logout from the system.
            self.gaia.logout()
            return new_item
        except ValueError as err:
            log.error(str(err))
            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            new_item['test_finished'] = f'{time_str} CET'
            new_item['test_result'] = NOT_PASSED
            new_item['test_additional_info'] = str(err)
            self.gaia.logout()
            return new_item

        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            new_item['test_finished'] = f'{time_str} CET'
            new_item['test_result'] = NOT_PASSED
            new_item['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return new_item

    # __end_of_execute_datalink_4_current_data_type

    def test_datalink_compare(self, test_info, basic_datalink_compare_info_4_test):
        """
             This tests execute a cross match between tables based on distance

             @param test_info: dict
                 Contains the basic info for the test to be performed
             @current_test: str
                name of the data_type that is being tested
             @return: test_results, dict
                 Returns a dict with the information resulting from the test run
         """

        test_results = test_info
        list_of_results = []

        test_number = test_results['test_id_number'].replace('#', '')

        for data_release in self.test_conditions_4_current_env.GAIA_RELEASES:

            dict_retrieval_types = self.test_conditions_4_current_env.DATALINK_COMPARE_RETRIEVAL_TYPES[data_release]
            # execute request
            for data_retrieval_type in dict_retrieval_types.keys():
                new_item = None
                new_item = self.execute_datalink_compare_4_current_data_type(data_retrieval_type, test_results,
                                                                             basic_datalink_compare_info_4_test,
                                                                             data_release)
                new_item['test_id_number'] = f'#{test_number}'
                my_new_item = new_item.copy()
                list_of_results.append(my_new_item)
                test_number = int(test_number) + 1
            print(len(list_of_results))
        return list_of_results

    # __end_of_test_datalink_compare

    def execute_datalink_compare_4_current_data_type(self, data_retrieval_type, test_results,
                                                     basic_datalink_info_4_test, current_gaia_data_release):
        """

        :param data_retrieval_type:
        :param test_results:
        :param basic_datalink_info_4_test:
        :param current_gaia_data_release:
        :return:
        """

        result_Files = ""

        # copy test
        new_item = self.get_basic_info_from_test_description(test_results, basic_datalink_info_4_test)

        # get current user_schema
        current_user_schema = self.test_conditions_4_current_env.GAIA_RELEASES[current_gaia_data_release]

        # execute request
        try:

            # STEP-1: Define Input Parameters
            # -----------------------------------------------------------------------------------

            log.debug("STEP-1: Define Input Parameters")
            log.debug("================================")

            path_ref = None

            # From conf'
            data_format = conf.CURRENT_DATA_FORMAT  # fits/votable
            data_structure = conf.CURRENT_DATA_STRUCTURE  # Combined/Individual/Raw

            # From paths'
            data_example = paths.path2_Datalink_test_products  # Check download date

            # From parameters
            data_release = current_gaia_data_release  # Current Gaia release
            retrieval_type = data_retrieval_type  # Current retrieval type

            # Path To Ref Files
            # ===================================================================
            if data_format == 'votable':
                path_ref = f'{data_example}/{data_structure}_vot/'
            if data_format == 'fits':
                path_ref = f'{data_example}/{data_structure}_fits/'
            if data_format == 'csv':
                path_ref = f'{data_example}/{data_structure}_csv/'

            # Check if the path exist, if not create it!!!
            Path(path_ref).mkdir(parents=True, exist_ok=True)

            # Starting with the tests for the format/structure selected
            log.debug('=' * 77)
            log.debug(f'Running Data Link Test for Data Format/Structure = {data_format}/{data_structure}')
            log.debug('=' * 77)

            log.debug("Define Input Parameters OK")

            log.debug("Doing log-in... ")
            self.gaia.login(user=credentials.USERNAME, password=credentials.PASSWORD)

            # STEP-2: Launch datalink oriented query
            # -----------------------------------------------------------------------------------
            log.debug("STEP-2: Launch datalink oriented query ")
            log.debug("=======================================")

            # get gaia_data_source table. eg. gaiadr2.gaia_source
            full_qualified_name = test_common_cons.FULL_QUALIFIED_TABLE_NAME_PATTERN. \
                replace(test_common_cons.SCHEMA_PATTERN, current_user_schema)
            full_qualified_name = full_qualified_name. \
                replace(test_common_cons.TABLE_NAME_PATTERN, conf.GAIA_SOURCE_DB_NAME)

            # Update query with current retrieval type
            query = new_item[current_gaia_data_release].replace(test_common_cons.FULL_QUALIFIED_PATTERN,
                                                                full_qualified_name)
            # update test description
            new_item['test_description'] = new_item['test_description'] \
                .replace(test_common_cons.RETRIEVAL_TYPE_PATTERN, data_retrieval_type)

            # Update request_sent description
            new_item['request_sent'] = new_item['request_sent'].replace(test_common_cons.QUERY_PATTERN, query)

            # Update test name
            new_item['test_name'] = 'DATALINK_COMPARE_' + current_gaia_data_release.replace(" ",
                                                                                            "_") + "_" + \
                                    data_retrieval_type.upper()

            # -----------------------------------------------------------------------------
            # TODO: Execute these code to get new set of IDS per Gaia Release. With them
            # update the tests conditions of 'DATALINK_COMPARE' stored in the file
            # 'test_conditions_<env>.py'
            # -----------------------------------------------------------------------------
            # job = self.gaia.launch_job(query)
            # results = job.get_results()
            # ids = results['source_id']
            # if len(results) <= 0:
            #       new_item['test_result'] = NOT_PASSED
            #       error_message = f' Number of results from the {data_retrieval_type} request is 0. FAILED TEST'
            #       new_item['test_additional_info'] = error_message
            #       log.error(error_message)
            #       raise ValueError(error_message)
            # -----------------------------------------------------------------------------
            ids = test_results[f'{current_gaia_data_release}_IDS']
            # -----------------------------------------------------------------------------

            log.debug(f"current list of IDS is: {ids}")

            log.debug("Launch datalink oriented query: OK ")

            # STEP-3: Download all datalink products
            # -----------------------------------------------------------------------------------
            log.debug("STEP-3: Download all datalink products ")
            log.debug("=======================================")

            datalink = self.gaia.load_data(ids=ids, format=data_format, data_release=data_release,
                                           data_structure=data_structure,
                                           retrieval_type=retrieval_type)  # TODO to be changed
            # for the current retrieval type

            if len(datalink) <= 0:
                new_item['test_result'] = NOT_PASSED
                error_message = f' Number of downloaded products from Datalink is 0. FAILED TEST'

                new_item['test_additional_info'] = error_message
                log.error(error_message)
                raise ValueError(error_message)

            log.debug("Download all datalink products: OK ")

            # STEP-4: Extract Data & Compare to reference
            # -----------------------------------------------------------------------------------
            log.debug("STEP-4: Extract Data & Compare to reference ")
            log.debug("============================================")

            dl_out = ReadDataLink(datalink, structure=data_structure, verbose=True)
            dl_out.get_products(product=retrieval_type)
            result_Files = str(dl_out.datalink)
            dl_out.get_file(file_index=0)
            dl_out.write_file()
            dl_out.compare(path_ref)

            # Get current time to complete our result object
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            new_item['test_finished'] = f'{time_str} CET'
            new_item['test_result'] = PASSED
            new_item['test_additional_info'] = "Both " + retrieval_type + " are equal"
            log.debug("Both " + retrieval_type + "are equal. TEST PASSED!!!")

            log.debug("Extract Data & Compare to reference: OK")
            self.gaia.logout()
            return new_item

        except ValueError as err:

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            new_item['test_finished'] = f'{time_str} CET'
            new_item['test_result'] = NOT_PASSED
            if TABLE_LENGTH in result_Files:
                # We need to check if the error message contains the patter <Table length=1>, and if it does
                # removed because it can cause problems when the report is converted to HTML format.
                result_Files = result_Files.replace(TABLE_LENGTH, "n_results=")
                result_Files = result_Files.replace(">", "")
                new_item['test_additional_info'] = str(err) + "\n" + result_Files
            else:
                new_item['test_additional_info'] = str(err) + "\n" + result_Files
            log.error(str(err) + "\n" + result_Files)
            self.gaia.logout()
            return new_item

        except HTTPError as err:

            error_message = "Error connecting TAP server"
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            new_item['test_finished'] = f'{time_str} CET'
            new_item['test_result'] = NOT_PASSED
            new_item['test_additional_info'] = error_message + "," + str(err)
            self.gaia.logout()
            return new_item
        except Exception as e:
            error_message = f'ERROR IN THE FORMAT OF THE FILES: {str(e)}'
            log.error(error_message)

            # Get current time
            time = datetime.now()
            time_str = time.strftime('%Y-%m-%d %H:%M:%S')
            # fill result object with the info from the http error
            new_item['test_finished'] = f'{time_str} CET'
            new_item['test_result'] = NOT_PASSED
            new_item['test_additional_info'] = error_message
            self.gaia.logout()
            return new_item

    # __end_of_execute_datalink_compare_4_current_data_type
