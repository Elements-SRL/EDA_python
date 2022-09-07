import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):
    data = []

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("EDA")
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)
        self.show()

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.btn = QPushButton("QFileDialog static method demo")
        self.btn.clicked.connect(self.get_file)
        layout.addWidget(self.btn)

        # add button
        # button1 = QPushButton(widget)
        # button1.setText("Button1")
        # button1.move(64, 32)
        # button1.clicked.connect(button1)

        self.setCentralWidget(widget)
        self.show()

    def add_data(self, *x_y_l_data_tuple):
        for (x, y, l) in x_y_l_data_tuple:
            self.data.append((x, y, l))
        self.update_plot()

    def update_plot(self):
        self.canvas.axes.cla()
        for (x, y, l) in self.data:
            line, = self.canvas.axes.plot(x, y)
            line.set_label(l)
        self.canvas.axes.legend()

    def get_file(self):
        f_name, _ = QFileDialog.getOpenFileName(self, 'Open file')
        print(f_name)
