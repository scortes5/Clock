import sys
from PyQt5.QtWidgets import QApplication
from home import HomeView



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeView()
    window.run()
    sys.exit(app.exec_())
