"""A palette for working with semantic segmentation labeling."""
import pandas as pd
from appJar import gui


class Palette(object):
    """A palette for working with semantic segmentation labeling."""

    # the width of the window
    WIDTH = 500
    # the height of the window
    HEIGHT = 700

    def __init__(self, metadata: pd.DataFrame) -> None:
        """
        .

        Args:
            metadata

        Returns:
            None

        """
        self.metadata = metadata
        self.segmentation_args = {
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
        # create an application window
        dims = '{}x{}'.format(self.WIDTH, 10 * len(metadata) + self.HEIGHT)
        self._app = gui(self.__class__.__name__, dims)
        self._window_did_load(self._app)
        self._view_did_load(self._app)


    # MARK: View Hierarchy

    def _window_did_load(self, app):
        """Perform global window decoration."""
        app.setFont(14)

    def _view_did_load(self, app):
        """Setup the sub-views after the view is loaded into memory."""

        app.startLabelFrame("Paint Style")
        app.addRadioButton("paint", "Brush")
        app.addRadioButton("paint", "Super Pixel")
        app.setRadioButtonChangeFunction('paint', self._did_change_paint)
        app.stopLabelFrame()

        app.addLabelScale('Brush Size')
        app.setScaleRange('Brush Size', 0, 50, curr=7)
        app.showScaleIntervals('Brush Size', 5)
        app.showScaleValue('Brush Size', show=True)
        app.setScaleChangeFunction('Brush Size', self._did_change_brush_size)

        app.startLabelFrame("Super Pixel Algorithm")
        app.addRadioButton("super_pixel", "Felzenszwalb")
        app.addRadioButton("super_pixel", "SLIC")
        app.addRadioButton("super_pixel", "Quickshift")
        app.addRadioButton("super_pixel", "Watershed")
        app.setRadioButtonChangeFunction('super_pixel', self._did_change_super_pixel)
        app.stopLabelFrame()



        app.startTabbedFrame("SuperPixel")

        app.startTab("Felzenszwalb")
        app.startLabelFrame("Scale")
        app.addLabelEntry("felzenszwalb_scale")
        app.stopLabelFrame()
        app.setEntryDefault('felzenszwalb_scale', self.segmentation_args['felzenszwalb']['scale'])
        app.setEntryChangeFunction("felzenszwalb_scale", self._did_change_felzenszwalb_scale)

        app.startLabelFrame("Sigma")
        app.addLabelEntry("felzenszwalb_sigma")
        app.stopLabelFrame()
        app.setEntryDefault('felzenszwalb_sigma', self.segmentation_args['felzenszwalb']['sigma'])
        app.setEntryChangeFunction("felzenszwalb_sigma", self._did_change_felzenszwalb_sigma)

        app.startLabelFrame("Minimum Size")
        app.addLabelEntry("felzenszwalb_min_size")
        app.stopLabelFrame()
        app.setEntryDefault('felzenszwalb_min_size', self.segmentation_args['felzenszwalb']['min_size'])
        app.setEntryChangeFunction("felzenszwalb_min_size", self._did_change_felzenszwalb_min_size)
        app.stopTab()



        app.startTab("SLIC")
        app.startLabelFrame("Number of Segments")
        app.addLabelEntry("slic_n_segments")
        app.stopLabelFrame()
        app.setEntryDefault('slic_n_segments', self.segmentation_args['slic']['n_segments'])
        app.setEntryChangeFunction("slic_n_segments", self._did_change_slic_num_segments)

        app.startLabelFrame("Compactness ")
        app.addLabelEntry("slic_compactness")
        app.stopLabelFrame()
        app.setEntryDefault('slic_compactness', self.segmentation_args['slic']['compactness'])
        app.setEntryChangeFunction("slic_compactness", self._did_change_slic_compactness)

        app.startLabelFrame("Sigma ")
        app.addLabelEntry("slic_sigma")
        app.stopLabelFrame()
        app.setEntryDefault('slic_sigma', self.segmentation_args['slic']['sigma'])
        app.setEntryChangeFunction("slic_sigma", self._did_change_slic_sigma)
        app.stopTab()



        app.startTab("Quickshift")
        app.startLabelFrame("Kernel Size")
        app.addLabelEntry("quickshift_kernel_size")
        app.stopLabelFrame()
        app.setEntryDefault('quickshift_kernel_size', self.segmentation_args['quickshift']['kernel_size'])
        app.setEntryChangeFunction("quickshift_kernel_size", self._did_change_quickshift_kernel_size)

        app.startLabelFrame("Maximum Distance")
        app.addLabelEntry("quickshift_max_dist")
        app.stopLabelFrame()
        app.setEntryDefault('quickshift_max_dist', self.segmentation_args['quickshift']['max_dist'])
        app.setEntryChangeFunction("quickshift_max_dist", self._did_change_quickshift_max_distance)

        app.startLabelFrame("Ratio")
        app.addLabelEntry("quickshift_ratio")
        app.stopLabelFrame()
        app.setEntryDefault('quickshift_ratio', self.segmentation_args['quickshift']['ratio'])
        app.setEntryChangeFunction("quickshift_ratio", self._did_change_quickshift_ratio)
        app.stopTab()



        app.startTab("Watershed")
        app.startLabelFrame("Makers")
        app.addLabelEntry("watershed_markers")
        app.stopLabelFrame()
        app.setEntryDefault('watershed_markers', self.segmentation_args['watershed']['markers'])
        app.setEntryChangeFunction("watershed_markers", self._did_change_watershed_markers)

        app.startLabelFrame("Compactness")
        app.addLabelEntry("watershed_compactness")
        app.stopLabelFrame()
        app.setEntryDefault('watershed_compactness', self.segmentation_args['watershed']['compactness'])
        app.setEntryChangeFunction("watershed_compactness", self._did_change_watershed_compactness)
        app.stopTab()
        app.stopTabbedFrame()

        app.addListBox('labels', self.metadata['label'])
        for idx, color in enumerate(self.metadata['rgb']):
            app.setListItemAtPosBg('labels', idx, '#%02x%02x%02x' % color)
            app.setListItemAtPosFg('labels', idx, '#FFFFFF')
        app.setListBoxChangeFunction('labels', self._did_change_label)

    # MARK: Callbacks

    def _did_change_paint(self, _):
        selected = self._app.getRadioButton('paint')
        print(selected)

    def _did_change_brush_size(self, _):
        selected = self._app.getScale('Brush Size')
        print(selected)

    def _did_change_super_pixel(self, _):
        selected = self._app.getRadioButton('super_pixel')
        print(selected)

    def _did_change_felzenszwalb_scale(self, _):
        selected = self._app.getEntry('felzenszwalb_scale')

        self.segmentation_args['felzenszwalb']['scale'] = selected

    def _did_change_felzenszwalb_sigma(self, _):
        selected = self._app.getEntry('felzenszwalb_sigma')

        self.segmentation_args['felzenszwalb']['sigma'] = selected

    def _did_change_felzenszwalb_min_size(self, _):
        selected = self._app.getEntry('felzenszwalb_min_size')

        self.segmentation_args['felzenszwalb']['min_size'] = selected

    def _did_change_slic_num_segments(self, _):
        selected = self._app.getEntry('slic_n_segments')

        self.segmentation_args['slic']['n_segments'] = selected

    def _did_change_slic_compactness(self, _):
        selected = self._app.getEntry('slic_compactness')

        self.segmentation_args['slic']['compactness'] = selected

    def _did_change_slic_sigma(self, _):
        selected = self._app.getEntry('slic_sigma')

        self.segmentation_args['slic']['sigma'] = selected

    def _did_change_quickshift_kernel_size(self, _):
        selected = self._app.getEntry('quickshift_kernel_size')

        self.segmentation_args['quickshift']['kernel_size'] = selected

    def _did_change_quickshift_max_distance(self, _):
        selected = self._app.getEntry('quickshift_max_dist')

        self.segmentation_args['quickshift']['max_dist'] = selected

    def _did_change_quickshift_ratio(self, _):
        selected = self._app.getEntry('quickshift_ratio')

        self.segmentation_args['quickshift']['ratio'] = selected

    def _did_change_watershed_markers(self, _):
        selected = self._app.getEntry('watershed_markers')

        self.segmentation_args['watershed']['markers'] = selected

    def _did_change_watershed_compactness(self, _):
        selected = self._app.getEntry('watershed_compactness')

        self.segmentation_args['watershed']['compactness'] = selected

    def _did_change_label(self, _):
        selected = self._app.getListBox('labels')[0]
        print(selected)

    # MARK: Execution Stack

    def run(self):
        """Start the application."""
        self._app.go()
