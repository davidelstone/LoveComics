import atexit
from comicbook import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.image = 'C:\\Users\\David\\Documents\\Projects\\Comic Reader\\img\\splash.png'
        self.temp_dirs = []
        self.comic_loaded = False
        self.current_comic = object()

    def init_UI(self):
        self.resize(550, 700)
        self.setWindowTitle('LoveComics')
        self.setWindowIcon(QIcon('C:\\Users\\David\\Documents\\Projects\\Comic Reader\\img\\LCIcon.png'))

        # Top Menu
        menu = self.menuBar()
        file = menu.addMenu("File")

        open = QAction("Open Comic...", self)
        file.addAction(open)

        exit = QAction("Exit", self)
        file.addAction(exit)

        self.status = QLabel("")
        self.statusBar().addPermanentWidget(self.status)

        file.triggered[QAction].connect(self.process_action)

    def load_image(self):
        container = QWidget()
        panel = QLabel(container)
        pixmap = QPixmap(self.image)
        panel.setPixmap(pixmap.scaledToWidth(self.width() - 20, Qt.SmoothTransformation))
        panel.setAlignment(Qt.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidget(panel)
        scroll.setWidgetResizable(True)

        self.setCentralWidget(scroll)
        panel.setFocus()

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
            self.statusBar().showMessage("Error - " + e)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', "Comic book files (*.cbr *.cbz)")
        cbf = ComicBookFile(filename[0])

        if cbf.type.lower() in ("cbr", "cbz"):
            self.statusBar().showMessage("Loading %s " % cbf.path)
            self.current_comic = cbf.unrar()
            self.comic_loaded = True
            self.temp_dirs.append(self.current_comic.tempdir)
            self.statusBar().clearMessage()
            self.display_comic()
        else:
            self.statusBar().showMessage("File not supported.", 20)

    def display_comic(self):
        self.image = self.current_comic.images[self.current_comic.current_page]
        self.load_image()
        self.status.setText("Page %i of %i   " % (self.current_comic.current_page, self.current_comic.total_pages))

    def mouseReleaseEvent(self, event):
        if self.comic_loaded:
            if event.button() == Qt.LeftButton and self.current_comic.current_page > 0:
                self.current_comic.flip_page('prev')
                self.display_comic()
            elif event.button() == Qt.RightButton and self.current_comic.current_page < self.current_comic.total_pages:
                self.current_comic.flip_page('next')
                self.display_comic()

    def keyReleaseEvent(self, event):
        if self.comic_loaded:
            if event.key() == Qt.Key_Left and self.current_comic.current_page > 0:
                self.current_comic.flip_page('prev')
                self.display_comic()
            elif event.key() == Qt.Key_Right and self.current_comic.current_page < self.current_comic.total_pages:
                self.current_comic.flip_page('next')
                self.display_comic()

    def cleanup_temp_dirs(self):
        for tmp_dir in self.temp_dirs:
            tmp_dir.cleanup()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    atexit.register(win.cleanup_temp_dirs)
    sys.exit(app.exec_())
