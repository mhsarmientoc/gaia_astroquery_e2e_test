# Class to read DataLink Output products in data_structure = Individual
import glob
import matplotlib.pyplot as plt
from astropy.io.votable.tree import VOTableFile, Resource

from src.main.tests_code.compare_files import CompareVot
from src.main.tests_code.compare_files import CompareFits
from src import paths


class ReadDataLink:
    """
    Initialize the class.
    """

    def __init__(self, datalink_output, structure='individual', verbose=True):
        """
        Define Attributes
        """
        self.structure = structure
        self.datalink = datalink_output
        self.type = type(self.datalink)
        self.n_els = len(self.datalink)
        self.items = [key for key in self.datalink.keys()]
        self.items.sort()
        self.get_format()
        # self.outdir = 'Outputs'
        self.outdir = paths.path2_Datalink_test_products_outdir  # Check download date
        if verbose:
            print(f'Datalink Output is a {self.type} with {self.n_els} item(s):')
            for item in self.items:
                print(f'* {item}')

    def get_format(self, verbose=False):
        """
        Find Datalink data format (fits, votable, csv)
        """
        item = self.items[0]
        self.format = item[item.find('.') + 1:]
        if verbose:
            print(f'Data Format: {self.format}')

    def get_products(self, product='EPOCH_PHOTOMETRY', verbose=True):
        """
        "Extract Data Product - Apply Only if g.load_data(retrieval_type = 'all')"
        "product = 'EPOCH_PHOTOMETRY', 'RVS_SPECTRA', 'XP_SPECTRA', 'XP_BASIS', 'MCMC'"
        "DataLink Products are a 1-element list: Automatically Extract First element"
        """
        self.product = product
        products = [item for item in self.items if self.product in item]
        self.datalink = dict((inp, self.datalink[inp][0]) for inp in products)
        self.items = [key for key in self.datalink.keys()]
        self.items.sort()
        if verbose:
            print()
            print(f'Extracting {self.product} File(s):')
            for item in self.items:
                print(f'* {item}')

    def get_file(self, file_index=0, verbose=True):
        """
        "Extract individual file from Data Product"
        """
        if not self.items:
            error_message = "The type of file is not available through DATALINK"
            raise ValueError(error_message)
        else:
            self.item = self.items[file_index]
            self.file = self.datalink[self.item]
            self.astro_tb()
            if verbose:
                print()
                print(f'Extracting File: {self.item}')

    def astro_tb(self):
        """
        "Ensures there is an Astropy Table ready for plotting & Showing in Jupyter Cell"
        """
        if self.format == 'fits':
            self.astro_tb = self.file
        if self.format == 'xml':
            self.astro_tb = self.file.to_table()

    def write_file(self):
        """
        "Write DataLink file."
        """
        if self.format == 'fits':
            self.filename = f'{self.outdir}/{self.structure}_{self.format}/{self.item}'
            self.file.write(self.filename, overwrite=True)

        if self.format == 'xml':
            self.filename = f'{self.outdir}/{self.structure}_vot/{self.item}'
            votable = VOTableFile()  # Create a new VOTable file..
            resource = Resource()  # ...with one resource...
            resource.tables.append(self.file)
            votable.resources.append(resource)
            votable.set_all_tables_format('BINARY2')
            votable.to_xml(self.filename)
        print(f'Saving File as: {self.filename}')

    def make_canvas(self, xlabel, ylabel, figsize, fontsize):
        """
        "Canvas plotter"
        """
        fig = plt.figure(figsize=figsize)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.xlabel(xlabel, fontsize=fontsize)
        plt.ylabel(ylabel, fontsize=fontsize)

    def plot_epoch(self, fontsize=22, figsize=[30, 7]):
        """
        "Plot Epoch Photometry"
        """
        self.make_canvas('Time', 'Magnitude', figsize, fontsize)
        if self.format == 'fits':
            gband, bpband, rpband = 'G ', 'BP', 'RP'
        if self.format == 'xml':
            gband, bpband, rpband = 'G', 'BP', 'RP'
        if self.format == 'csv':
            gband, bpband, rpband = 'G', 'BP', 'RP'
        colors = iter(['go', 'bo', 'ro'])

        for band in [gband, bpband, rpband]:
            plt.plot(self.astro_tb['time'][self.astro_tb['band'] == band],
                     self.astro_tb['mag'][self.astro_tb['band'] == band],
                     next(colors))
        plt.show()

    def plot_rvs(self, fontsize=22, figsize=[30, 7]):
        """
        "RVS Spectra and XP_Spectra"
        """
        self.make_canvas('Wavelength', 'Flux', figsize, fontsize)
        plt.plot(self.astro_tb['wavelength'], self.astro_tb['flux'])
        plt.show()

    def plot_file(self, fontsize=22, figsize=[30, 6]):
        """
        "Datalink Automatic Plotter"
        """
        if self.product == 'EPOCH_PHOTOMETRY':
            self.plot_epoch(fontsize=fontsize, figsize=figsize)
        if self.product == 'RVS_SPECTRA' or self.product == 'XP_SPECTRA':
            self.plot_rvs(fontsize=fontsize, figsize=figsize)

    def compare(self, path_to_refdir):
        """
        "Compare Datalink Written file to Reference file. In order to work the DataLink file must have been
        written before"
        """
        print(f"{path_to_refdir}{self.product}*{self.format}")
        reference_file = glob.glob(f'{path_to_refdir}{self.product}*{self.format}')[0]
        if self.format == 'xml':
            comp = CompareVot(test_file=self.filename, reference_file=reference_file, verbose=True)
        if self.format == 'fits':
            comp = CompareFits(test_file=self.filename, reference_file=reference_file, verbose=True)
        comp.compare()
