"""
@author: Maria H. Sarmiento Carrión
@contact: mhsarmiento@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 16 Sep. 2020
"""

LOGIN = {
    'test_description': 'Test login into the Gaia Tap',
    'request_sent': 'Gaia.login(user=USERNAME, password=PASSWORD)',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

LOGOUT = {
    'test_description': 'Test logout from Gaia Tap',
    'request_sent': 'Gaia.logout()',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

QUERY_OBJECT = {
    'test_description': 'Test query object. This test uses SkyCoord to resolve an object by its ICRS sky position.',
    'test_expected_value': 50,
    'test_RA': 56.75,
    'test_DEC': 24.12,
    'side_size': 5,
    'test_units': 'deg',
    'test_frame': 'icrs',
    'request_sent': 'r = Gaia.query_object_async(coordinate=coord, width=width, height=height)',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

CONE_SEARCH = {
    'test_description': 'Test cone search capability. This test perform a Cone Search in the Gaia Catalogue. It also '
                        'uses SkyCoord to resolve an object by its ICRS sky position.',
    'test_expected_value': 50,
    'test_RA': 56.75,
    'test_DEC': 24.12,
    'test_radius': 5.0,
    'test_units': 'deg',
    'test_frame': 'icrs',
    'request_sent': 'j = Gaia.cone_search_async(coord, radius)',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

GET_PUBLIC_TABLES = {
    'test_description': 'This test loads only public table names. (Tap + Capability)',
    'test_expected_value': 27,
    'request_sent': 'tables = Gaia.load_tables(only_names=True)',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

LOAD_TABLE = {
    'test_description': 'This loads only a table (Tap + Capability)',
    'schema_name': 'gaiadr2',
    'gaia_table_name': 'gaia_source',
    'test_expected_value': 96,
    'request_sent': 'table = Gaia.load_table(\'@TABLE_NAME@\')',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

SYNCHRONOUS_QUERY = {
    'test_description': 'Test synchronous query. Type of request does not store the results at server side. Suitable '
                        'when the amount of data to be retrieved is "small"',
    'schema_name': 'gaiadr2',
    'gaia_table_name': 'gaia_source',
    'test_expected_value': 100,
    'request_sent': 'job = Gaia.launch_job("@QUERY_PATTERN@", dump_to_file=False)',
    'test_query': 'select top 100 solution_id,ref_epoch,ra_dec_corr,astrometric_n_obs_al,matched_observations,'
                  'duplicated_source,phot_variable_flag from @FULL_QUALIFIED_PATTERN@ order by source_id',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

SYNCHRONOUS_ON_THE_FLY_QUERY = {
    'test_description': 'Test Synchronous query on an ‘on-the-fly’ uploaded table. This test checks that the table '
                        'can be uploaded to the server in order to be used in a query.',
    'test_table': 'test_on_the_fly_table',
    'test_expected_value': 75,
    'request_sent': 'job = Gaia.launch_job(query=@QUERY_PATTERN@, '
                    'upload_resource=upload_resource, upload_table_name=@TABLE_NAME@, verbose=True)',
    'test_query': 'select * from tap_upload.@TABLE_NAME@',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

ASYNCHRONOUS_QUERY = {
    'test_description': 'Test asynchronous query. These type of queries save results at server side and can '
                        'be accessed at any time. The results can be saved in memory (default) or in a file.'
                        'At the end of the test, the code removes the job created with Gaia.remove_jobs(job.jobid)',
    'schema_name': 'gaiadr2',
    'gaia_table_name': 'gaia_source',
    'test_expected_value': 100,
    'request_sent': 'job = Gaia.launch_job_async("@QUERY_PATTERN@", dump_to_file=False)',
    'test_query': 'select top 100 solution_id,ref_epoch,ra_dec_corr,astrometric_n_obs_al,matched_observations,'
                  'duplicated_source,phot_variable_flag from @FULL_QUALIFIED_PATTERN@ order by source_id',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

LIST_SHARED_TABLES = {
    'test_description': 'This test list all tables, public and shared (Tap + Capability). For the test to be correct '
                        'the number of results returned after do login() must be major or equal to the number of '
                        'public tables',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td>Get N public tables: job = Gaia.load_tables('
                    'only_names=True)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td>Do Login(): Gaia.login(user=USERNAME, password=PASSWORD)</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td>Get N shared tables to compare: shared_tables = Gaia.load_tables('
                    'only_names=True, '
                    'include_shared_tables=True)</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td>After the test, do Logout: Gaia.logout()</table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

UPLOAD_TABLE_FROM_URL = {
    'test_description': 'This test checks the possibility of persisting a table in the private user space from URL',
    'table_description': 'This test checks the capability that enables the user to load a table from a URL',
    'test_resource': 'http://tapvizier.u-strasbg.fr/TAPVizieR/tap/sync/?REQUEST=doQuery&lang=ADQL&FORMAT=votable&QUERY'
                     '=select+*+from+TAP_SCHEMA.columns+where+table_name=\'II/336/apass9\'',
    'table_name': 'table_test_from_url',
    'test_query': 'select * from @TABLE_NAME@',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Upload table from URL: job = Gaia.upload_table('
                    'upload_resource=url, '
                    'table_name="table_test_from_url",table_description="Some description")</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Query new table: job = Gaia.launch_job(query=query)</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Delete now the table from the user schema. job_delete = '
                    'Gaia.delete_user_table( '
                    '"table_test_from_file")</td></tr>'
                    '<tr><td><b>STEP-5:</b></td><td> After the test, do logout: Gaia.logout()</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

DELETE_TABLE = {
    'test_description': 'This test checks the capability of deleting a persisting table from the private user space',
    'table_description': 'This test checks the capability that enables the user to delete a table from his/her user '
                         'space',
    'full_qualified_table_name': 'user_@LOGIN_USER@.@TABLE_NAME@',
    'table_name': 'table_test_for_delete',
    'test_query': 'select * from @TABLE_NAME@',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Upload table from URL: job = Gaia.upload_table('
                    'upload_resource=url, '
                    'table_name="table_test",table_description="Some description")</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Query new table: job = Gaia.launch_job(query=query)</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Delete now the table from the user schema. job_delete = '
                    'Gaia.delete_user_table( '
                    '"table_test_from_file")</td></tr>'
                    '<tr><td><b>STEP-5:</b></td><td> After the test, do logout: Gaia.logout()</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

UPLOAD_TABLE_FROM_FILE = {
    'test_description': 'This test checks the possibility of persisting a table in the private user space from local '
                        'file',
    'table_description': 'This test checks the capability that enables the user to load a table from a local file',
    'full_qualified_table_name': 'user_@LOGIN_USER@.@TABLE_NAME@',
    'table_name': 'test_table_from_file',
    'test_query': 'select * from @TABLE_NAME@',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Upload table from local table: job = Gaia.upload_table('
                    'upload_resource=path_to_local_resource, table_name="table_test_from_url",table_description="Some '
                    'description")</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Query new table: job = Gaia.launch_job(query=query)</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Delete now the table from the user schema. job_delete = '
                    'Gaia.delete_user_table( '
                    '"test_table_from_file")</td></tr>'
                    '<tr><td><b>STEP-5:</b></td><td> After the test, do logout: Gaia.logout()</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

UPLOAD_TABLE_FROM_JOB = {
    'test_description': 'This test checks the possibility of persisting a table in the private user space'
                        ' from the job result of a previous request',
    'table_description': 'This test checks the capability  that enables the user to load a table from a job result',
    'test_resource': '@JOB_ID@',
    'n_expected_results': 10,
    'test_query': 'select top 10 * from @FULL_QUALIFIED_PATTERN@',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Execute Query: j1 = '
                    'Gaia.launch_job_async("select top 10 * from @FULL_QUALIFIED_PATTERN@")</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Upload from job: job = Gaia.upload_table_from_job(j1)</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Query new table: job = Gaia.launch_job('
                    'query=query_to_new_table)</td></tr> '
                    '<tr><td><b>STEP-5:</b></td><td> Delete now the table from the user schema. job_delete = '
                    'Gaia.delete_user_table( '
                    '"table_from_job")</td></tr>'
                    '<tr><td><b>STEP-6:</b></td><td> After the test, do logout: Gaia.logout()</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

UPLOAD_TABLE_FROM_ASTROPY_TABLE = {
    'test_description': 'This test checks the possibility of persisting a table in the private user space from source. '
                        'In this case the source is an Astropy table',
    'table_description': 'This test checks the capability that enables the user to load an AstroPy table',
    'test_resource': '@TABLE_NAME@',
    'n_expected_results': 3,
    'table_name': 'test_table_from_astropy',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Create AstroPy table</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Upload AstroPy: Gaia.upload_table(upload_resource=table, '
                    'table_name="my_astropy_table")</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Query new table: job = Gaia.launch_job('
                    'query=query_to_new_table)</td></tr> '
                    '<tr><td><b>STEP-5:</b></td><td> Delete now the table from the user schema. job_delete = '
                    'Gaia.delete_user_table( '
                    '"my_astropy_table")</td></tr>'
                    '<tr><td><b>STEP-6:</b></td><td> After the test, do logout: Gaia.logout()</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

CROSS_MATCH = {
    'test_description': 'This test execute a cross match between tables based on distance',
    'table_description': '',
    'user_table': 'my_sources_4_test_xmatch',
    'n_expected_results': 134,
    'xmatch_table_name': 'xmatch_table_test',
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Upload table from local table: jGaia.upload_table('
                    'upload_resource=test_resource, '
                    'table_name=table_name)</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Prepare the xmatch between the table resource used for this test '
                    'and '
                    '@FULL_QUALIFIED_PATTERN@. Gaia.cross_match(full_qualified_table_name_a=full_qualified_table_name, '
                    'full_qualified_table_name_b=full_qualified_table_name_b, results_table_name=xmatch_table_name, '
                    'radius=1.0)</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Test the results obtained.  job_query = Gaia.launch_job('
                    'query=query_new_xmatch_table)</td></tr> '
                    '<tr><td><b>STEP-5:</b></td><td> Delete now the table from the user schema. job_delete = '
                    'Gaia.delete_user_table( '
                    '"test_table_from_file")</td></tr>'
                    '<tr><td><b>STEP-6:</b></td><td> After the test, do logout: Gaia.logout()</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

DATALINK = {
    'test_description': 'This test execute the @RETRIEVAL_TYPE@'
                        ' access and checks if the results returned are correct',
    'Gaia DR2': "select top 10 source_id from @FULL_QUALIFIED_PATTERN@ where has_xp_mean_spectrum = 'true' AND "
                "has_rvs_mean_spectrum = 'true' AND has_epoch_photometry='true' AND has_epoch_rad_vel = 'true' "
                "AND has_mcmc_samples_gsp_phot = 'true' AND has_mcmc_samples_msc = 'true' "
                "order by source_id asc",
    'Gaia DR2_IDS': ['Gaia DR3 3111611584415482240',
                     'Gaia DR3 933195856826668672',
                     'Gaia DR3 4713061372761394432',
                     'Gaia DR3 2794793016882937600',
                     'Gaia DR3 898874708741591808',
                     'Gaia DR3 5508064423458414464',
                     'Gaia DR3 484054844466262272',
                     'Gaia DR3 5837325962221728768',
                     'Gaia DR3 4835627163725784192',
                     'Gaia DR3 297110414310432256',
                     'Gaia DR3 3154463606997798272',
                     'Gaia DR3 5587815437801239936',
                     'Gaia DR3 4357786763279480448',
                     'Gaia DR3 4480741781382639104',
                     'Gaia DR3 5851435990641849344',
                     'Gaia DR3 2154876871561899520',
                     'Gaia DR3 3496548204413064576',
                     'Gaia DR3 2984829372516544256',
                     'Gaia DR3 259418743399412096',
                     'Gaia DR3 3323170953178591104'],
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Do Login(): Gaia.login(user=USERNAME, '
                    'password=PASSWORD)</td></tr> '
                    '<tr><td><b>STEP-2:</b></td><td> Get query to retrieve the IDs that we need: job = '
                    'Gaia.launch_job(query) where query is</td></tr> '
                    '@QUERY_PATTERN@</td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Retrieve @RETRIEVAL_TYPE@ data:  '
                    '@RETRIEVAL_TYPE@_data = Gaia.load_data(ids=ids, '
                    'retrieval_type="@RETRIEVAL_TYPE@")</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

DATALINK_COMPARE = {
    'test_description': 'This query test the latest version of the library Astroquery Gaia Datalink by comparing the'
                        ' data download through this service in astroquery vs the data download from the service '
                        ' implemented in the GACS interface. This test test the data type: @RETRIEVAL_TYPE@',
    'test_expected_value': 5,
    'Gaia DR2': "select top 10 source_id from @FULL_QUALIFIED_PATTERN@ where has_xp_mean_spectrum = 'true' AND "
                "has_rvs_mean_spectrum = 'true' AND has_epoch_photometry='true' AND has_epoch_rad_vel = 'true' "
                "AND has_mcmc_samples_gsp_phot = 'true' AND has_mcmc_samples_msc = 'true' "
                "order by source_id asc",
    'Gaia DR2_IDS': ['Gaia DR3 3111611584415482240',
                     'Gaia DR3 933195856826668672',
                     'Gaia DR3 4713061372761394432',
                     'Gaia DR3 2794793016882937600',
                     'Gaia DR3 898874708741591808',
                     'Gaia DR3 5508064423458414464',
                     'Gaia DR3 484054844466262272',
                     'Gaia DR3 5837325962221728768',
                     'Gaia DR3 4835627163725784192',
                     'Gaia DR3 297110414310432256',
                     'Gaia DR3 3154463606997798272',
                     'Gaia DR3 5587815437801239936',
                     'Gaia DR3 4357786763279480448',
                     'Gaia DR3 4480741781382639104',
                     'Gaia DR3 5851435990641849344',
                     'Gaia DR3 2154876871561899520',
                     'Gaia DR3 3496548204413064576',
                     'Gaia DR3 2984829372516544256',
                     'Gaia DR3 259418743399412096',
                     'Gaia DR3 3323170953178591104'],
    'request_sent': '<table><tr><td><b>STEP-1:</b></td><td> Define Input Parameters</td></tr>'
                    '<tr><td><b>STEP-2:</b></td><td> Launch datalink oriented query: job = Gaia.launch_job(query) '
                    'where query is '
                    '@QUERY_PATTERN@ </td></tr>'
                    '<tr><td><b>STEP-3:</b></td><td> Download all datalink products</td></tr>'
                    '<tr><td><b>STEP-4:</b></td><td> Extract Data & Compare to reference</td></tr></table>',
    'test_additional_info': 'N/A',
    'test_result': 'NOT PASSED',
    'test_finished': 'yyyy-mm-dd hh:mm:ss'
}

DR2_DATALINK_EXPECTED_RESULTS = {
    'EPOCH_PHOTOMETRY': 8
}

DATALINK_RETRIEVAL_TYPES = {
    'Gaia DR2': DR2_DATALINK_EXPECTED_RESULTS
}

DR2_DATALINK_COMPARE_EXPECTED_RESULTS = {
    'EPOCH_PHOTOMETRY': 10
}

DATALINK_COMPARE_RETRIEVAL_TYPES = {
    'Gaia DR2': DR2_DATALINK_COMPARE_EXPECTED_RESULTS
}

GAIA_RELEASES = {
    'Gaia DR2': 'dr2'
}

__all__ = ['LOGIN', 'LOGOUT', 'GET_PUBLIC_TABLES', 'LOAD_TABLE', 'SYNCHRONOUS_QUERY',
           'SYNCHRONOUS_ON_THE_FLY_QUERY', 'ASYNCHRONOUS_QUERY', 'LIST_SHARED_TABLES', 'UPLOAD_TABLE_FROM_URL',
           'DELETE_TABLE', 'UPLOAD_TABLE_FROM_FILE', 'UPLOAD_TABLE_FROM_JOB', 'UPLOAD_TABLE_FROM_ASTROPY_TABLE',
           'CROSS_MATCH', 'DATALINK', 'DATALINK_COMPARE','DR2_DATALINK_EXPECTED_RESULTS', 'DATALINK_RETRIEVAL_TYPES',
           'GAIA_RELEASES','DATALINK_COMPARE_RETRIEVAL_TYPES','DR2_DATALINK_COMPARE_EXPECTED_RESULTS']
