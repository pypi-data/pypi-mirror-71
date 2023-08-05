# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtCore

from prettyqt import core


QtCore.QFile.__bases__ = (core.FileDevice,)


class File(QtCore.QFile):
    @contextlib.contextmanager
    def open_file(self, flags):
        self.open(flags)
        yield None
        self.close()
