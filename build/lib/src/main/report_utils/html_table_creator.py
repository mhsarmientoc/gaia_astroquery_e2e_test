import pandas as pd
import copy
import src.main.report_utils.read_write as io


class HTMLTableCreator:
    """
    creates the title, table, and logo html code.
    expects the template data as a dict as provided by the toml metadata entity.
    if you set strict_mode to True, only white-listed attributes will be included.
    thus, you can add as much data as you want to the template, only a
    subset will be included in the resulting table and therefore on the html page
    """

    def __init__(self, list_of_test, strict_mode=True):
        self.list_of_test = copy.deepcopy(list_of_test)
        self.bodyList = []
        self.strict_mode = strict_mode

    def make(self):
        """
        quasi-main, calls all functions in correct order
        """
        body = None
        for test in self.list_of_test:
            if test != "filepath":
                test_description = self.list_of_test[test]
                test_description = self.make_fields_human_readable(test_description)
                test_description = self.format_keys(test_description)
                self.add_table(test_description)
                body = self.join_data()
            # __end_of_if
        print("Created HTML body containing the meta data")
        return body

    def make_fields_human_readable(self, input_test):
        """
        converts raw string links to html links,
        replaces properties written in 'camelCase' to 'camel case'
        removes python list syntax to comma-seperated values
        """
        replace_after_iteration = []
        test = copy.deepcopy(input_test)

        for key in test:

            if type(test[key]) == str:
                test[key] = io.regex_remove(
                    "_", test[key])
                test[key] = test[key].replace("\n", "<br/>")

            # MAKE LISTS COMMA-SEPARATED FOR HUMANS:
            if type(test[key]) == list:
                list_as_string = "".join(test[key]).replace("\n", "<br/>").replace("&", "&amp;")
                test[key] = list_as_string

            # ADD SPACES TO CAMEL CASE FOR HUMANS:
            if self.is_camel_case(key):
                human_readable_form = self.camel_case2human_readable(key)
                replace_after_iteration.append(
                    (key, human_readable_form, test[key]))

        for key, human_readable_form, value in replace_after_iteration:
            test[human_readable_form] = value
            test.pop(key)
        return test

    # __end_of_make_fields_human_readable

    def format_keys(self, test):
        """
        @param test: dict
            contains the keys that will act as titles of the rows in the results test of the main report
        @return: a dict with the keys formatted
        """
        test_copy = dict()
        for key in test:
            # preserve the old value
            old_key = key

            # remove "_"
            if "_" in old_key:
                old_key = old_key.replace("_", " ")
            # Change to upper-case
            old_key = old_key.upper()
            # Now we are going to put the key font in 'bold'
            old_key = f'<b>{old_key}</b>'

            # finally replace the old key by the new one
            test_copy[old_key] = test[key]

        return test_copy

    # __end_of_format_keys

    def is_camel_case(self, string):
        """helper func. that returns true if the given string is in camel keys
        but NOT if it is all caps or contains spaces already
        """
        if " " in string:
            return False
        elif string.isupper():  # all caps suggests the string is an acronym
            return False
        else:
            for cha in string[1:]:
                if cha.isupper():
                    return True
            return False

    def camel_case2human_readable(self, string):
        indexes = self.find_indexes(string)
        readable = self.add_spaces(string.lower(), indexes)
        return readable

    def find_indexes(self, string):
        indexes = []
        for i, cha in enumerate(string):
            if cha.isupper():
                indexes.append(i)
        return indexes

    def add_spaces(self, string, indexes):
        list_string = [char for char in string]
        already_added = 0
        for upper_index in indexes:
            list_string.insert(upper_index + already_added, " ")
            already_added += 1
        return "".join(list_string)

    def add_table(self, input_test):
        sorted_df = self.sort_fields_as_df(input_test)
        table = sorted_df.to_html(
            classes="table", header=False, escape=False, index=False)
        # to_html() includes obsolete table styling, removing:
        table = table.replace('border="1" class="dataframe table"', '')
        self.bodyList.append(table)

    def join_data(self):
        return "\n</br>".join(self.bodyList)

    def sort_fields_as_df(self, test):
        # todo this should be an entity and NOT be dependent on the writing after the corrections..
        order = {'<b>TEST NAME</b>': 1,
                 '<b>TEST ID NUMBER</b>': 2,
                 '<b>TEST RESULT</b>': 3,
                 '<b>TEST DESCRIPTION</b>': 4,
                 '<b>REQUEST SENT</b>': 5,
                 '<b>TEST ADDITIONAL INFO</b>': 6,
                 '<b>TEST STARTED</b>': 7,
                 '<b>TEST FINISHED</b>': 8,
                 '<b>EXECUTED</b>': 9}
        list_key_value = [[k, v] for k, v in test.items()]
        existing_fields = []
        for i, key_value in enumerate(list_key_value):
            wanted_index = order.get(key_value[0], None)
            if wanted_index:
                existing_fields.append([key_value[0], i, wanted_index])
        # the wanted index is at index 2
        sorted = self.sublist_sort(existing_fields, 2)
        for field in sorted:
            field[1] = test[field[0]]
            field.pop()
        df = pd.DataFrame(sorted)
        return df

    def sublist_sort(self, sub_list, index):
        sub_list.sort(key=lambda x: x[index])
        return sub_list
