from astropy.io import fits
from astropy.io.votable import parse
from astropy.io.votable.tree import VOTableFile, Resource, Table, Field
from astropy.table import QTable


class CompareFits:
    """
    Initialize the class.
    """

    def __init__(self, test_file='', reference_file='', verbose=True):
        """
        Define Attributes
        """
        self.file_test = CompareFits.read_fits(test_file)
        self.file_ref = CompareFits.read_fits(reference_file)
        if verbose:
            print(f'Reference File: {reference_file}')

    def compare(self):
        comp = CompareFits.header_comp(self.file_ref['header'], self.file_test['header'])

    def read_fits(self, fits_file):
        hdu = fits.open(fits_file)
        data = QTable(hdu[1].data)
        header = hdu[1].header
        return {'data': data, 'header': header}

    def header_comp(self, header_ref, header_test):
        for key in header_ref.keys():
            if header_ref[key] != header_test[key]:
                error_message = f'WARNING! REF HEADER: {key} = {header_ref[key]} ; TEST HEADER: {header_test[key]}'
                print(error_message)
                raise ValueError(error_message)


class CompareVot:
    """
    Initialize the class.
    """

    def __init__(self, test_file='', reference_file='', verbose=True):
        """
        Define Attributes
        """
        self.file_test = parse(test_file)
        self.file_ref = parse(reference_file)
        if verbose:
            print(f'Reference File: {reference_file}')

    def compare(self):
        names_1 = [self.file_test.get_field_by_id_or_name(inpfield.name).name for inpfield in
                   self.file_test.iter_fields_and_params()]
        names_2 = [self.file_ref.get_field_by_id_or_name(inpfield.name).name for inpfield in
                   self.file_ref.iter_fields_and_params()]

        if len(names_1) != len(names_2):
            x = set(names_1)
            y = set(names_2)
            diff = x.difference(y)
            print()
            error_message = f'WARNING! MISSING FIELDS: {diff}'
            print(error_message)
            raise ValueError(error_message)
        else:
            for inpfield in self.file_ref.iter_fields_and_params():
                field_1 = self.file_ref.get_field_by_id_or_name(inpfield.name)  # Reference File
                field_2 = self.file_test.get_field_by_id_or_name(inpfield.name)
                message = f'WARNING! Field {field_1.ID}'

                if field_1.datatype != field_2.datatype:
                    error_message = f'{message}: DATATYPE = {field_2.datatype} VS. {field_1.datatype}'
                    print(error_message)
                    raise ValueError(error_message)
                if field_1.name != field_2.name:
                    error_message = f'{message}: NAME = {field_2.name} VS. {field_1.name}'
                    print(error_message)
                    raise ValueError(error_message)
                if field_1.ucd != field_2.ucd:
                    error_message = f'{message}: UCD = {field_2.ucd} VS. {field_1.ucd}'
                    print(error_message)
                    raise ValueError(error_message)
                if field_1.utype != field_2.utype:
                    error_message = f'{message}: wUTYPE = {field_2.utype} VS. {field_1.utype}'
                    print(error_message)
                    raise ValueError(error_message)
                if field_1.unit != field_2.unit:
                    error_message = f'{message}: UNIT = {field_2.unit} VS. {field_1.unit}'
                    print(error_message)
                    raise ValueError(error_message)
