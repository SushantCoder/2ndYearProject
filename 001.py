import sys
from PyQt5.QtWidgets import * # pip install PyQtWebEngine
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.browser=QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Hajmola's NavBar
        navbar=QToolBar()
        self.addToolBar(navbar)

        home_btn=QAction('Home',self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)


        back_btn=QAction('Back',self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        for_btn=QAction('Forward',self)
        for_btn.triggered.connect(self.browser.forward)
        navbar.addAction(for_btn)

        rload_btn=QAction('Reload',self)
        rload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(rload_btn)

        self.url_bar=QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url)


    def navigate_home(self):
        self.browser.setUrl(QUrl("http://google.com"))
                        

    def navigate_to_url(self):
        url=self.url_bar.text()
        self.browser.setUrl(QUrl(url))


    def update_url(self,url1):
        self.url_bar.setText(url1.toString())

HajmoBrowser=QApplication(sys.argv)
QApplication.setApplicationName('Sasta Browser')
window=MainWindow()
HajmoBrowser.exec_()