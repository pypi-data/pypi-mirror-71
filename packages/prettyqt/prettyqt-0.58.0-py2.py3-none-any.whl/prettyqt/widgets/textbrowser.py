# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import docutils.core
from qtpy import QtWidgets
from prettyqt import gui, widgets, core


QtWidgets.QTextBrowser.__bases__ = (widgets.TextEdit,)


class TextBrowser(QtWidgets.QTextBrowser):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOpenExternalLinks(True)

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    font=gui.Font(self.font()))

    def __setstate__(self, state):
        self.__init__()
        self.setPlainText(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])

    # def dragEnterEvent(self, event):
    #     u = event.mimeData().urls()
    #     for url in u:
    #         file_path = os.path.abspath(url.toLocalFile())

    #         ext = file_path.split(".")[-1]
    #         if ext in ["txt", "md", "markdown"]:
    #             event.accept()
    #         else:
    #             event.ignore()

    # def dropEvent(self, event):
    #     event.accept()
    #     self.show_markdown(self.filePath)

    def show_markdown(self, file_path):
        with open(file_path) as f:
            file_content = f.read()
        self.setMarkdown(file_content)

    def show_rst(self, file_path):
        with open(file_path) as f:
            file_content = f.read()
        html = docutils.core.publish_string(file_content, writer_name="html")
        self.setHtml(str(html))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    reader = TextBrowser()
    reader.show()
    app.exec_()
