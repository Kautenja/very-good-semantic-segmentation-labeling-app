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
        """Setup the subviews after the view is loaded into memory."""

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
        app.addLabelEntry("Scale ")
        app.setEntryChangeFunction("Scale ", self._did_change_felzenszwalb_scale)
        app.addLabelEntry("Sigma ")
        app.setEntryChangeFunction("Sigma ", self._did_change_felzenszwalb_sigma)
        app.addLabelEntry("Minimum Size ")
        app.setEntryChangeFunction("Minimum Size ", self._did_change_felzenszwalb_min_size)
        app.stopTab()

        app.startTab("SLIC")
        app.addLabelEntry("Number of Segments ")
        app.setEntryChangeFunction("Number of Segments ", self._did_change_slic_num_segments)
        app.addLabelEntry("Compactness  ")
        app.setEntryChangeFunction("Compactness  ", self._did_change_slic_compactness)
        app.addLabelEntry("Sigma  ")
        app.setEntryChangeFunction("Sigma  ", self._did_change_slic_sigma)
        app.stopTab()

        app.startTab("Quickshift")
        app.addLabelEntry("Kernel Size ")
        app.setEntryChangeFunction("Kernel Size ", self._did_change_quickshift_kernel_size)
        app.addLabelEntry("Maximum Distance ")
        app.setEntryChangeFunction("Maximum Distance ", self._did_change_quickshift_max_distance)
        app.addLabelEntry("Ratio ")
        app.setEntryChangeFunction("Ratio ", self._did_change_quickshift_ratio)
        app.stopTab()

        app.startTab("Watershed")
        app.addLabelEntry("Markers ")
        app.setEntryChangeFunction("Markers ", self._did_change_watershed_markers)
        app.addLabelEntry("Compactness ")
        app.setEntryChangeFunction("Compactness ", self._did_change_watershed_compactness)
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
        selected = self._app.getEntry('Scale ')
        print(selected)

    def _did_change_felzenszwalb_sigma(self, _):
        selected = self._app.getEntry('Sigma ')
        print(selected)

    def _did_change_felzenszwalb_min_size(self, _):
        selected = self._app.getEntry('Minimum Size ')
        print(selected)

    def _did_change_slic_num_segments(self, _):
        selected = self._app.getEntry('Number of Segments ')
        print(selected)

    def _did_change_slic_compactness(self, _):
        selected = self._app.getEntry('Compactness  ')
        print(selected)

    def _did_change_slic_sigma(self, _):
        selected = self._app.getEntry('Sigma  ')
        print(selected)

    def _did_change_quickshift_kernel_size(self, _):
        selected = self._app.getEntry('Kernel Size ')
        print(selected)

    def _did_change_quickshift_max_distance(self, _):
        selected = self._app.getEntry('Maximum Distance ')
        print(selected)

    def _did_change_quickshift_ratio(self, _):
        selected = self._app.getEntry('Ratio ')
        print(selected)

    def _did_change_watershed_markers(self, _):
        selected = self._app.getEntry('Markers ')
        print(selected)

    def _did_change_watershed_compactness(self, _):
        selected = self._app.getEntry('Compactness ')
        print(selected)

    def _did_change_label(self, _):
        selected = self._app.getListBox('labels')[0]
        print(selected)

    # MARK: Execution Stack

    def run(self):
        """Start the application."""
        self._app.go()
