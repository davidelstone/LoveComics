import sys
import atexit
from comicbook import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.image = 'C:\\Users\\David\\Documents\\Projects\\Comic Reader\\img\\chew.jpg'
        self.temp_dirs = []
        self.comic_loaded = False
        self.current_comic = object()

    def init_UI(self):
        self.statusBar().showMessage("Ready")
        self.resize(300, 300)
        self.setWindowTitle("Comic Reader v0.1")

        # Top Menu
        menu = self.menuBar()
        file = menu.addMenu("File")

        open = QAction("Open Comic...", self)
        file.addAction(open)

        exit = QAction("Exit", self)
        file.addAction(exit)

        file.triggered[QAction].connect(self.process_action)

        # Image display panel

    def load_image(self):
        # TODO: Allow scrolling.
        container = QWidget()
        panel = QLabel(container)
        self.setCentralWidget(container)
        pixmap = QPixmap(self.image)
        panel.setPixmap(pixmap.scaledToWidth(self.width()))
        panel.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, resizeEvent):
        self.load_image()

    def process_action(self, act):
        options = {
            "Open Comic...": self.open_file,
            "Exit": win.close
        }
        try:
            options[act.text()]()  # Run selected menu option
        except KeyError as e:
            print("Error - " + e)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', "Comic book files (*.cbr *.cbz)")
        cbf = ComicBookFile(filename[0])

        if cbf.type.lower() == "cbr":
            self.current_comic = cbf.unrar()
            self.comic_loaded = True
            self.temp_dirs.append(self.current_comic.tempdir)
            self.display_comic()
        elif cbf.type.lower() == "cbz":
            cbf.unzip()
        else:
            print("File not supported.")

    def display_comic(self):
        # Boop.
        self.image = self.current_comic.images[self.current_comic.current_page]
        self.load_image()

    def mouseReleaseEvent(self, event):
        # TODO: Forward and back, set page boundaries.
        print(event)
        if self.comic_loaded:
            self.current_comic.flip_page('next')
            print(self.current_comic.current_page)
            self.display_comic()


    def cleanup_temp_dirs(self):
        for dir in self.temp_dirs:
            dir.cleanup()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    atexit.register(win.cleanup_temp_dirs)
    sys.exit(app.exec_())
