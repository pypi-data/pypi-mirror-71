"""
FileBrowser

A module for creating interactive file browser widgets in a Jupyter notebook

Workflow Overview
-----------------
1. Create object
2. Browse file interactively
3. Extract path of selected file

Basic Usage
-----------
1. Import module and create widget

    .. highlight:: python
    .. code-block:: python

        import fluorseg as fs
        f = fs.FileBrowser()
        f.widget()

2. Browse

    ... interactively

3. Extract path of selected file

    .. highlight:: python
    .. code-block:: python

        f.path
"""

import os
import ipywidgets as widgets
import glob

def get_lif_list(path):
    """
    Returns a list of files ending in *.lif in provided folder

    :param: path
    :return: list -- filenames

    """
    path += '/*.lif'
    return glob.glob(path)


def get_roi_zip_list(path):
    """
    Returns a list of files ending in *.zip in provided folder

    :param: path
    :return: list -- filenames

    """
    path += '/*.zip'
    return glob.glob(path)


class FileBrowser(object):
    """ Implements an ipywidgets directory chooser.
    Only shows directories.

    >>> f = FileBrowser
    >>> f.widget() # activate the widget
    >>> ...
    >>> f.path # get the selected directory...

    """

    def __init__(self):
        self.path = os.getcwd()
        self._update_files()

    def _update_files(self):
        self.files = list()
        self.dirs = list()
        if os.path.isdir(self.path):
            for f in os.listdir(self.path):
                ff = self.path + "/" + f
                if os.path.isdir(ff) and f[0] != '.':
                    self.dirs.append(f)
                    # else:
                    # self.files.append(f)

    def widget(self):
        box = widgets.VBox()
        self._update(box)
        return box

    def _update(self, box):

        def on_click(b):
            if b.description == 'up one level':
                self.path = os.path.split(self.path)[0]
            else:
                self.path = self.path + "/" + b.description
            self._update_files()
            self._update(box)

        buttons = []
        # if self.files:
        button = widgets.Button(description='up one level', background_color='#aaaaaa')
        button.on_click(on_click)
        buttons.append(button)
        for f in self.dirs:
            button = widgets.Button(description=f, background_color='#d0d0ff')
            button.on_click(on_click)
            buttons.append(button)
        for f in self.files:
            button = widgets.Button(description=f)
            button.on_click(on_click)
            buttons.append(button)
        box.children = tuple([widgets.HTML("You have selected: <h3>%s</h3>" % (self.path,))] + buttons)