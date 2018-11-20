"""A palette for working with semantic segmentation labeling."""
from copy import deepcopy
from threading import Thread
from multiprocessing import Process
from appJar import gui
import pandas as pd


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
        'paint': 'brush',
        'brush_size': 5,
        'super_pixel': 'felzenszwalb',
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
        'label': None,
    }

    def __init__(self, metadata: pd.DataFrame, callback=None) -> None:
        """
        Initialize a new palette.

        Args:
            metadata: the label metadata for the palette
            callback: a callback method for getting updates from the palette

        Returns:
            None

        """
        self.metadata = metadata
        self._callback = callback if callable(callback) else lambda x: x
        self.segmentation_args = deepcopy(self.DEFAULTS)
        self.segmentation_args['label'] = self.metadata['label'][0]
        # create the application window
        height = self.LABEL_HEIGHT * len(metadata) + self.HEIGHT
        self._app = gui(
            title=self.__class__.__name__,
            geom='{}x{}'.format(self.WIDTH, height),
            handleArgs=False,
            showIcon=False,
        )
        self._view_did_load(self._app)

    def callback(self) -> None:
        """Call the callback on a background thread."""
        # create a thread for the callback and start it. this process is
        # already a daemon so this thread cant – and need not – be a daemon
        Thread(target=self._callback, args=(self.segmentation_args,)).start()

    @classmethod
    def thread(cls, metadata: pd.DataFrame, callback=None):
        """
        Initialize and start a palette on a background thread.

        Args:
            metadata: the label metadata for the palette
            callback: a callback method for getting updates from the palette

        Returns:
            a tuple of:
            - the instance of palette
            - the background thread running the palette

        """
        # instantiate a palette with the standard arguments
        def run():
            cls(metadata, callback).run()
        # create the background thread (process in Python abstract) as a daemon
        Process(target=run, daemon=True).start()

    def _view_did_load(self, app) -> None:
        """Setup the sub-views after the view is loaded into memory."""
        app.setFont(14)
        # setup the paint style
        app.startLabelFrame("Paint Style")
        app.addRadioButton("paint", "Brush")
        app.addRadioButton("paint", "Super Pixel")
        app.setRadioButtonChangeFunction('paint', self._did_change_paint)
        app.setRadioButton('paint', 'Brush')
        app.stopLabelFrame()
        # setup the brush size slider
        app.addLabelScale('Brush Size')
        app.setScaleRange('Brush Size', 5, 50)
        app.showScaleIntervals('Brush Size', 5)
        app.showScaleValue('Brush Size', show=True)
        app.setScaleChangeFunction('Brush Size', self._did_change_brush_size)
        app.setScale('Brush Size', 5)
        # super pixel algorithm parameters
        app.startTabbedFrame("super_pixel")
        # Felzenszwalb
        #     Scale
        app.startTab("Felzenszwalb")
        app.startLabelFrame("Scale")
        app.addValidationEntry("felzenszwalb_scale")
        app.stopLabelFrame()
        app.setEntryDefault(
            'felzenszwalb_scale',
            self.segmentation_args['felzenszwalb']['scale']
        )
        app.setEntryChangeFunction(
            "felzenszwalb_scale",
            self._did_change_felzenszwalb_scale
        )
        #     Sigma
        app.startLabelFrame("Sigma")
        app.addValidationEntry("felzenszwalb_sigma")
        app.stopLabelFrame()
        app.setEntryDefault(
            'felzenszwalb_sigma',
            self.segmentation_args['felzenszwalb']['sigma']
        )
        app.setEntryChangeFunction(
            "felzenszwalb_sigma",
            self._did_change_felzenszwalb_sigma
        )
        #     Minimum Size
        app.startLabelFrame("Minimum Size")
        app.addValidationEntry("felzenszwalb_min_size")
        app.stopLabelFrame()
        app.setEntryDefault(
            'felzenszwalb_min_size',
            self.segmentation_args['felzenszwalb']['min_size']
        )
        app.setEntryChangeFunction(
            "felzenszwalb_min_size",
            self._did_change_felzenszwalb_min_size
        )
        app.stopTab()
        app.setTabbedFrameChangeFunction(
            'super_pixel',
            self._did_change_super_pixel
        )
        # SLIC
        #     Number of Segments
        app.startTab("SLIC")
        app.startLabelFrame("Number of Segments")
        app.addValidationEntry("slic_n_segments")
        app.stopLabelFrame()
        app.setEntryDefault(
            'slic_n_segments',
            self.segmentation_args['slic']['n_segments']
        )
        app.setEntryChangeFunction(
            "slic_n_segments",
            self._did_change_slic_num_segments
        )
        #     Compactness
        app.startLabelFrame("Compactness ")
        app.addValidationEntry("slic_compactness")
        app.stopLabelFrame()
        app.setEntryDefault(
            'slic_compactness',
            self.segmentation_args['slic']['compactness']
        )
        app.setEntryChangeFunction(
            "slic_compactness",
            self._did_change_slic_compactness
        )
        #     Sigma
        app.startLabelFrame("Sigma ")
        app.addValidationEntry("slic_sigma")
        app.stopLabelFrame()
        app.setEntryDefault(
            'slic_sigma',
            self.segmentation_args['slic']['sigma']
        )
        app.setEntryChangeFunction(
            "slic_sigma",
            self._did_change_slic_sigma
        )
        app.stopTab()
        # Quickshift
        #     Kernel Size
        app.startTab("Quickshift")
        app.startLabelFrame("Kernel Size")
        app.addValidationEntry("quickshift_kernel_size")
        app.stopLabelFrame()
        app.setEntryDefault(
            'quickshift_kernel_size',
            self.segmentation_args['quickshift']['kernel_size']
        )
        app.setEntryChangeFunction(
            "quickshift_kernel_size",
            self._did_change_quickshift_kernel_size
        )
        #     Maximum Distance
        app.startLabelFrame("Maximum Distance")
        app.addValidationEntry("quickshift_max_dist")
        app.stopLabelFrame()
        app.setEntryDefault(
            'quickshift_max_dist',
            self.segmentation_args['quickshift']['max_dist']
        )
        app.setEntryChangeFunction(
            "quickshift_max_dist",
            self._did_change_quickshift_max_distance
        )
        #     Ratio
        app.startLabelFrame("Ratio")
        app.addValidationEntry("quickshift_ratio")
        app.stopLabelFrame()
        app.setEntryDefault(
            'quickshift_ratio',
            self.segmentation_args['quickshift']['ratio']
        )
        app.setEntryChangeFunction(
            "quickshift_ratio",
            self._did_change_quickshift_ratio
        )
        app.stopTab()
        # Watershed
        #     Markers
        app.startTab('Watershed')
        app.startLabelFrame('Makers')
        app.addValidationEntry('watershed_markers')
        app.stopLabelFrame()
        app.setEntryDefault(
            'watershed_markers',
            self.segmentation_args['watershed']['markers']
        )
        app.setEntryChangeFunction(
            'watershed_markers',
            self._did_change_watershed_markers
        )
        #     Compactness
        app.startLabelFrame('Compactness')
        app.addValidationEntry('watershed_compactness')
        app.stopLabelFrame()
        app.setEntryDefault(
            'watershed_compactness',
            self.segmentation_args['watershed']['compactness']
        )
        app.setEntryChangeFunction(
            'watershed_compactness',
            self._did_change_watershed_compactness
        )
        app.stopTab()
        app.stopTabbedFrame()
        # add a list box for selecting the labels
        app.addListBox('labels', self.metadata['label'])
        for idx, color in enumerate(self.metadata['rgb']):
            app.setListItemAtPosBg('labels', idx, '#%02x%02x%02x' % color)
            app.setListItemAtPosFg('labels', idx, '#FFFFFF')
        app.setListBoxChangeFunction('labels', self._did_change_label)
        app.selectListItem('labels', self.metadata['label'][0])

    def run(self) -> None:
        """Start the palette."""
        self._app.go()

    # MARK: Callbacks

    def _did_change_paint(self, _) -> None:
        """Respond to changes in mode of painting."""
        selected = self._app.getRadioButton('paint')
        self.segmentation_args['paint'] = selected.lower().replace(' ', '_')
        self.callback()

    def _did_change_brush_size(self, _) -> None:
        """Respond to changes in the size of the brush."""
        selected = self._app.getScale('Brush Size')
        self.segmentation_args['brush_size'] = int(selected)
        self.callback()

    def _did_change_super_pixel(self, _) -> None:
        """Respond to changes in the selected super pixel algorithm."""
        # get the currently selected tab from the super pixel tab bar
        selected = self._app.getTabbedFrameSelectedTab('super_pixel')
        # convert to lower case and replace spaces with under scores
        selected = selected.lower().replace(' ', '_')
        # set the super pixel algorithm to the selected tab
        self.segmentation_args['super_pixel'] = selected
        # pass the data to the callback
        self.callback()

    def _did_change_entry(self,
        title: str,
        alg: str,
        param: str,
        data_type: 'Callable'
    ) -> None:
        """
        Respond to changes in a segmentation algorithm hyperparameters.

        Args:
            title: the title of the text box to get data from
            alg: the name of the algorithm to set parameters for
            param: the name of the parameter to set
            data_type: the data type to cast the

        Returns:
            None

        """
        # if the entry is empty, return to the default value
        if self._app.getEntry(title) == "":
            self.segmentation_args[alg][param] = self.DEFAULTS[alg][param]
            self._app.setEntryWaitingValidation(title)
            # pass the data to the callback
            self.callback()
        else:
            # try to cast the input to the given input type
            try:
                selected = data_type(self._app.getEntry(title))
                self.segmentation_args[alg][param] = selected
                # set the UI element to valid (green check)
                self._app.setEntryValid(title)
                # pass the data to the callback
                self.callback()
            except ValueError:
                # set the UI element to invalid (red x)
                self._app.setEntryInvalid(title)

    def _did_change_felzenszwalb_scale(self, _) -> None:
        """Respond to changes in the felzenszwalb scale parameter."""
        self._did_change_entry(
            'felzenszwalb_scale',
            'felzenszwalb',
            'scale',
            int
        )

    def _did_change_felzenszwalb_sigma(self, _) -> None:
        """Respond to changes in the felzenszwalb sigma parameter."""
        self._did_change_entry(
            'felzenszwalb_sigma',
            'felzenszwalb',
            'sigma',
            float
        )

    def _did_change_felzenszwalb_min_size(self, _) -> None:
        """Respond to changes in the felzenszwalb min size parameter."""
        self._did_change_entry(
            'felzenszwalb_min_size',
            'felzenszwalb',
            'min_size',
            int
        )

    def _did_change_slic_num_segments(self, _) -> None:
        """Respond to changes in the SLIC number of segments parameter."""
        self._did_change_entry(
            'slic_n_segments',
            'slic',
            'n_segments',
            int
        )

    def _did_change_slic_compactness(self, _) -> None:
        """Respond to changes in the SLIC compactness parameter."""
        self._did_change_entry(
            'slic_compactness',
            'slic',
            'compactness',
            float
        )

    def _did_change_slic_sigma(self, _) -> None:
        """Respond to changes in the SLIC sigma parameter."""
        self._did_change_entry(
            'slic_sigma',
            'slic',
            'sigma',
            float
        )

    def _did_change_quickshift_kernel_size(self, _) -> None:
        """Respond to changes in the Quickshift kernel size parameter."""
        self._did_change_entry(
            'quickshift_kernel_size',
            'quickshift',
            'kernel_size',
            int
        )

    def _did_change_quickshift_max_distance(self, _) -> None:
        """Respond to changes in the Quickshift max distance parameter."""
        self._did_change_entry(
            'quickshift_max_dist',
            'quickshift',
            'max_dist',
            float
        )

    def _did_change_quickshift_ratio(self, _) -> None:
        """Respond to changes in the Quickshift ratio parameter."""
        self._did_change_entry(
            'quickshift_ratio',
            'quickshift',
            'ratio',
            float
        )

    def _did_change_watershed_markers(self, _) -> None:
        """Respond to changes in the Watershed markers parameter."""
        self._did_change_entry(
            'watershed_markers',
            'watershed',
            'markers',
            int
        )

    def _did_change_watershed_compactness(self, _) -> None:
        """Respond to changes in the Watershed compactness parameter."""
        self._did_change_entry(
            'watershed_compactness',
            'watershed',
            'compactness',
            float
        )

    def _did_change_label(self, _) -> None:
        """Respond to changes in the label selection list box."""
        # get the selected items from the list box
        selected = self._app.getListBox('labels')
        # if the length of the list is 0 (i.e., nothing selected), return
        if len(selected) == 0:
            return
        # grab the first (and only) item in the list as the selected label
        self.segmentation_args['label'] = selected[0]
        # call the callback with the updated parameters
        self.callback()
