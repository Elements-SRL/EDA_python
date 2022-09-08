# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import matplotlib
from PyQt5 import QtWidgets
import gui

matplotlib.use('Qt5Agg')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_to_file = "../Data/Data_CH001_000.abf"
    # path_to_file = input("Inserisci il path del file: ")
    # abf = fh.open_abf(path_to_file)
    # abf2 = fh.open_abf("../Data/Data_CH002_000.abf")
    # abf3 = fh.open_abf("../Data/Data_CH003_000.abf")
    # abf4 = fh.open_abf("../Data/Data_CH004_000.abf")

    # if abf is None:
    #     # TODO show error message
    #     exit(0)

    # print(abf.sweepY)  # displays sweep data (ADC)
    # print(abf.sweepX)  # displays sweep times (seconds)
    # print(abf.sweepC)  # displays command waveform (DAC)
    # print(abf)
    # print(abf.headerText)  # display header information in the console
    # abf.headerLaunch()  # display header information in a web browser

    # for i in range(0,abf.sweepCount):
    #     abf.setSweep(i)
    #     plt.plot(abf.sweepX, abf.sweepY, alpha=.5, label="sweep %d" % i)

    # plt.plot(abf.sweepX, abf.sweepY, label="channel 1")
    # plt.plot(abf2.sweepX, abf2.sweepY, label="channel 2")
    # plt.plot(abf3.sweepX, abf3.sweepY, label="channel 3")
    # plt.plot(abf4.sweepX, abf4.sweepY, label="channel 4")
    # plt.plot(abf.sweepX, abf.sweepC, label=abf.sweepLabelC)  # mV

    # plt.ylabel(abf.sweepLabelY)
    # plt.xlabel(abf.sweepLabelX)
    # plt.legend()
    # plt.show()

    app = QtWidgets.QApplication(sys.argv)
    w = gui.MainWindow()
    # w.add_data((abf.sweepX, abf.sweepY, "channel 1"), (abf2.sweepX, abf2.sweepY, "channel 2"),
    #            (abf3.sweepX, abf3.sweepY, "channel 3"), (abf4.sweepX, abf4.sweepY, "channel 4"))
    app.exec()
