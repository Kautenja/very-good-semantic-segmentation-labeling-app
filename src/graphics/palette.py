"""A palette for working with semantic segmentation labeling."""
import pandas as pd
from appJar import gui
from copy import deepcopy


class Palette(object):
    """A palette for working with semantic segmentation labeling."""

    # the width of the window
    WIDTH = 500
    # the height of the window
    HEIGHT = 700
    # the height per label entry
    LABEL_HEIGHT = 10
    # the default arguments for the view controller
    DEFAULTS = {
        'felzenszwalb': {
            'scale': 100,
            'sigma': 0.5,
            'min_size': 50,
        },
        'slic': {
            'n_segments': 250,
            'compactness': 10,
            'sigma': 1,
        },
        'quickshift': {
            'kernel_size': 3,
            'max_dist': 6,
            'ratio': 0.5,
        },
        'watershed': {
            'markers': 250,
            'compactness': 0.001,
        },
    }

    def __init__(self, metadata: pd.DataFrame) -> None:
        """
        .

        Args:
            metadata

        Returns:
            None

        """
        self.metadata = metadata
        self.segmentation_args = deepcopy(self.DEFAULTS)
        # create an application window
        height = self.LABEL_HEIGHT * len(metadata) + self.HEIGHT
        dims = '{}x{}'.format(self.WIDTH, height)
        self._app = gui(self.__class__.__name__, dims)
        self._window_did_load(self._app)
        self._view_did_load(self._app)

    # MARK: View Hierarchy

    def _window_did_load(self, app) -> None:
        """Perform global window decoration."""
        app.setFont(14)

    def _view_did_load(self, app) -> None:
        """Setup the sub-views after the view is loaded into memory."""
        # setup the paint style
        app.startLabelFrame("Paint Style")
        app.addRadioButton("paint", "Brush")
        app.addRadioButton("paint", "Super Pixel")
        app.setRadioButtonChangeFunction('paint', self._did_change_paint)
        app.setRadioButton('paint', 'Brush')
        app.stopLabelFrame()
        # setup the brush size slider
        app.addLabelScale('Brush Size')
        app.setScaleRange('Brush Size', 0, 50)
        app.showScaleIntervals('Brush Size', 5)
        app.showScaleValue('Brush Size', show=True)
        app.setScaleChangeFunction('Brush Size', self._did_change_brush_size)
        app.setScale('Brush Size', 5)
        # setup the super pixel algorithm picker
        app.startLabelFrame("Super Pixel Algorithm")
        app.addRadioButton("super_pixel", "Felzenszwalb")
        app.addRadioButton("super_pixel", "SLIC")
        app.addRadioButton("super_pixel", "Quickshift")
        app.addRadioButton("super_pixel", "Watershed")
        app.setRadioButtonChangeFunction('super_pixel', self._did_change_super_pixel)
        app.setRadioButton('super_pixel', 'Felzenszwalb')
        app.stopLabelFrame()
        # super pixel algorithm parameters
        app.startTabbedFrame("SuperPixel")
        # Felzenszwalb
        #     Scale
        app.startTab("Felzenszwalb")
        app.startLabelFrame("Scale")
        app.addValidationEntry("felzenszwalb_scale")
        app.stopLabelFrame()
        app.setEntryDefault('felzenszwalb_scale', self.segmentation_args['felzenszwalb']['scale'])
        app.setEntryChangeFunction("felzenszwalb_scale", self._did_change_felzenszwalb_scale)
        #     Sigma
        app.startLabelFrame("Sigma")
        app.addValidationEntry("felzenszwalb_sigma")
        app.stopLabelFrame()
        app.setEntryDefault('felzenszwalb_sigma', self.segmentation_args['felzenszwalb']['sigma'])
        app.setEntryChangeFunction("felzenszwalb_sigma", self._did_change_felzenszwalb_sigma)
        #     Minimum Size
        app.startLabelFrame("Minimum Size")
        app.addValidationEntry("felzenszwalb_min_size")
        app.stopLabelFrame()
        app.setEntryDefault('felzenszwalb_min_size', self.segmentation_args['felzenszwalb']['min_size'])
        app.setEntryChangeFunction("felzenszwalb_min_size", self._did_change_felzenszwalb_min_size)
        app.stopTab()
        # SLIC
        #     Number of Segments
        app.startTab("SLIC")
        app.startLabelFrame("Number of Segments")
        app.addValidationEntry("slic_n_segments")
        app.stopLabelFrame()
        app.setEntryDefault('slic_n_segments', self.segmentation_args['slic']['n_segments'])
        app.setEntryChangeFunction("slic_n_segments", self._did_change_slic_num_segments)
        #     Compactness
        app.startLabelFrame("Compactness ")
        app.addValidationEntry("slic_compactness")
        app.stopLabelFrame()
        app.setEntryDefault('slic_compactness', self.segmentation_args['slic']['compactness'])
        app.setEntryChangeFunction("slic_compactness", self._did_change_slic_compactness)
        #     Sigma
        app.startLabelFrame("Sigma ")
        app.addValidationEntry("slic_sigma")
        app.stopLabelFrame()
        app.setEntryDefault('slic_sigma', self.segmentation_args['slic']['sigma'])
        app.setEntryChangeFunction("slic_sigma", self._did_change_slic_sigma)
        app.stopTab()
        # Quickshift
        #     Kernel Size
        app.startTab("Quickshift")
        app.startLabelFrame("Kernel Size")
        app.addValidationEntry("quickshift_kernel_size")
        app.stopLabelFrame()
        app.setEntryDefault('quickshift_kernel_size', self.segmentation_args['quickshift']['kernel_size'])
        app.setEntryChangeFunction("quickshift_kernel_size", self._did_change_quickshift_kernel_size)
        #     Maximum Distance
        app.startLabelFrame("Maximum Distance")
        app.addValidationEntry("quickshift_max_dist")
        app.stopLabelFrame()
        app.setEntryDefault('quickshift_max_dist', self.segmentation_args['quickshift']['max_dist'])
        app.setEntryChangeFunction("quickshift_max_dist", self._did_change_quickshift_max_distance)
        #     Ratio
        app.startLabelFrame("Ratio")
        app.addValidationEntry("quickshift_ratio")
        app.stopLabelFrame()
        app.setEntryDefault('quickshift_ratio', self.segmentation_args['quickshift']['ratio'])
        app.setEntryChangeFunction("quickshift_ratio", self._did_change_quickshift_ratio)
        app.stopTab()
        # Watershed
        #     Markers
        app.startTab('Watershed')
        app.startLabelFrame('Makers')
        app.addValidationEntry('watershed_markers')
        app.stopLabelFrame()
        app.setEntryDefault('watershed_markers', self.segmentation_args['watershed']['markers'])
        app.setEntryChangeFunction('watershed_markers', self._did_change_watershed_markers)
        #     Compactness
        app.startLabelFrame('Compactness')
        app.addValidationEntry('watershed_compactness')
        app.stopLabelFrame()
        app.setEntryDefault('watershed_compactness', self.segmentation_args['watershed']['compactness'])
        app.setEntryChangeFunction('watershed_compactness', self._did_change_watershed_compactness)
        app.stopTab()
        app.stopTabbedFrame()
        # add a list box for selecting the labels
        app.addListBox('labels', self.metadata['label'])
        for idx, color in enumerate(self.metadata['rgb']):
            app.setListItemAtPosBg('labels', idx, '#%02x%02x%02x' % color)
            app.setListItemAtPosFg('labels', idx, '#FFFFFF')
        app.setListBoxChangeFunction('labels', self._did_change_label)
        app.selectListItem('labels', self.metadata['label'][0])

    # MARK: Callbacks

    def _did_change_paint(self, _) -> None:
        selected = self._app.getRadioButton('paint')
        print(selected)

    def _did_change_brush_size(self, _) -> None:
        selected = self._app.getScale('Brush Size')
        print(selected)

    def _did_change_super_pixel(self, _) -> None:
        selected = self._app.getRadioButton('super_pixel')
        print(selected)

    def _did_change_felzenszwalb_scale(self, _) -> None:
        if self._app.getEntry('felzenszwalb_scale') == "":
            default = self.DEFAULTS['felzenszwalb']['scale']
            self.segmentation_args['felzenszwalb']['scale'] = default
            self._app.setEntryWaitingValidation('felzenszwalb_scale')
            return
        try:
            selected = int(self._app.getEntry('felzenszwalb_scale'))
            self.segmentation_args['felzenszwalb']['scale'] = selected
            self._app.setEntryValid('felzenszwalb_scale')
        except ValueError:
            self._app.setEntryInvalid('felzenszwalb_scale')

    def _did_change_felzenszwalb_sigma(self, _) -> None:
        if self._app.getEntry('felzenszwalb_sigma') == "":
            default = self.DEFAULTS['felzenszwalb']['sigma']
            self.segmentation_args['felzenszwalb']['sigma'] = default
            self._app.setEntryWaitingValidation('felzenszwalb_sigma')
            return
        try:
            selected = float(self._app.getEntry('felzenszwalb_sigma'))
            self.segmentation_args['felzenszwalb']['sigma'] = selected
            self._app.setEntryValid('felzenszwalb_sigma')
        except ValueError:
            self._app.setEntryInvalid('felzenszwalb_sigma')

    def _did_change_felzenszwalb_min_size(self, _) -> None:
        if self._app.getEntry('felzenszwalb_min_size') == "":
            default = self.DEFAULTS['felzenszwalb']['min_size']
            self.segmentation_args['felzenszwalb']['min_size'] = default
            self._app.setEntryWaitingValidation('felzenszwalb_min_size')
            return
        try:
            selected = int(self._app.getEntry('felzenszwalb_min_size'))
            self.segmentation_args['felzenszwalb']['min_size'] = selected
            self._app.setEntryValid('felzenszwalb_min_size')
        except ValueError:
            self._app.setEntryInvalid('felzenszwalb_min_size')

    def _did_change_slic_num_segments(self, _) -> None:
        if self._app.getEntry('slic_n_segments') == "":
            default = self.DEFAULTS['slic']['n_segments']
            self.segmentation_args['slic']['n_segments'] = default
            self._app.setEntryWaitingValidation('slic_n_segments')
            return
        try:
            selected = int(self._app.getEntry('slic_n_segments'))
            self.segmentation_args['slic']['n_segments'] = selected
            self._app.setEntryValid('slic_n_segments')
        except ValueError:
            self._app.setEntryInvalid('slic_n_segments')

    def _did_change_slic_compactness(self, _) -> None:
        if self._app.getEntry('slic_compactness') == "":
            default = self.DEFAULTS['slic']['compactness']
            self.segmentation_args['slic']['compactness'] = default
            self._app.setEntryWaitingValidation('slic_compactness')
            return
        try:
            selected = float(self._app.getEntry('slic_compactness'))
            self.segmentation_args['slic']['compactness'] = selected
            self._app.setEntryValid('slic_compactness')
        except ValueError:
            self._app.setEntryInvalid('slic_compactness')

    def _did_change_slic_sigma(self, _) -> None:
        if self._app.getEntry('slic_sigma') == "":
            default = self.DEFAULTS['slic']['sigma']
            self.segmentation_args['slic']['sigma'] = default
            self._app.setEntryWaitingValidation('slic_sigma')
            return
        try:
            selected = float(self._app.getEntry('slic_sigma'))
            self.segmentation_args['slic']['sigma'] = selected
            self._app.setEntryValid('slic_sigma')
        except ValueError:
            self._app.setEntryInvalid('slic_sigma')

    def _did_change_quickshift_kernel_size(self, _) -> None:
        if self._app.getEntry('quickshift_kernel_size') == "":
            default = self.DEFAULTS['quickshift']['kernel_size']
            self.segmentation_args['quickshift']['kernel_size'] = default
            self._app.setEntryWaitingValidation('quickshift_kernel_size')
            return
        try:
            selected = int(self._app.getEntry('quickshift_kernel_size'))
            self.segmentation_args['quickshift']['kernel_size'] = selected
            self._app.setEntryValid('quickshift_kernel_size')
        except ValueError:
            self._app.setEntryInvalid('quickshift_kernel_size')

    def _did_change_quickshift_max_distance(self, _) -> None:
        if self._app.getEntry('quickshift_max_dist') == "":
            default = self.DEFAULTS['quickshift']['max_dist']
            self.segmentation_args['quickshift']['max_dist'] = default
            self._app.setEntryWaitingValidation('quickshift_max_dist')
            return
        try:
            selected = int(self._app.getEntry('quickshift_max_dist'))
            self.segmentation_args['quickshift']['max_dist'] = selected
            self._app.setEntryValid('quickshift_max_dist')
        except ValueError:
            self._app.setEntryInvalid('quickshift_max_dist')

    def _did_change_quickshift_ratio(self, _) -> None:
        if self._app.getEntry('quickshift_ratio') == "":
            default = self.DEFAULTS['quickshift']['ratio']
            self.segmentation_args['quickshift']['ratio'] = default
            self._app.setEntryWaitingValidation('quickshift_ratio')
            return
        try:
            selected = float(self._app.getEntry('quickshift_ratio'))
            self.segmentation_args['quickshift']['ratio'] = selected
            self._app.setEntryValid('quickshift_ratio')
        except ValueError:
            self._app.setEntryInvalid('quickshift_ratio')

    def _did_change_watershed_markers(self, _) -> None:
        if self._app.getEntry('watershed_markers') == "":
            default = self.DEFAULTS['watershed']['markers']
            self.segmentation_args['watershed']['markers'] = default
            self._app.setEntryWaitingValidation('watershed_markers')
            return
        try:
            selected = int(self._app.getEntry('watershed_markers'))
            self.segmentation_args['watershed']['markers'] = selected
            self._app.setEntryValid('watershed_markers')
        except ValueError:
            self._app.setEntryInvalid('watershed_markers')

    def _did_change_watershed_compactness(self, _) -> None:
        if self._app.getEntry('watershed_compactness') == "":
            default = self.DEFAULTS['watershed']['compactness']
            self.segmentation_args['watershed']['compactness'] = default
            self._app.setEntryWaitingValidation('watershed_compactness')
            return
        try:
            selected = float(self._app.getEntry('watershed_compactness'))
            self.segmentation_args['watershed']['compactness'] = selected
            self._app.setEntryValid('watershed_compactness')
        except ValueError:
            self._app.setEntryInvalid('watershed_compactness')

    def _did_change_label(self, _) -> None:
        selected = self._app.getListBox('labels')[0]
        print(selected)

    # MARK: Execution Stack

    def run(self) -> None:
        """Start the application."""
        self._app.go()
