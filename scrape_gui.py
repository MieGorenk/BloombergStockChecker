import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QGridLayout, QLabel,QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout
from scrape_engine import retrieve_urls, scrape_web, add_url_to_file, refresh_data
import json


# The root window of the app
class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    super(MainWindow, self).__init__()
    self.main_app = MainApp() 
    self.setCentralWidget(self.main_app) 

    # Set up menubar
    addUrlAction = QAction('&Add Url to File', self)
    addUrlAction.triggered.connect(self.on_click)
    self.pop_up = PopUp()

    mainMenu = self.menuBar()
    fileMenu = mainMenu.addMenu('&File')
    fileMenu.addAction(addUrlAction)

  # Will show pup up when the menubar is clicked
  def on_click(self):
    self.pop_up.show()
   
# The class of Pop Up Message box
class PopUp(QWidget):
  
  def __init__(self):
    super(PopUp, self).__init__()
    self.setGeometry(150, 200, 300, 150)
    self.setWindowTitle("Add Url...")
    self.initUI()
  
  def initUI(self):
    root = QVBoxLayout()
    up = QHBoxLayout()
    down = QHBoxLayout()
    
    self.url = QLineEdit()
    self.btn = QPushButton("Add", self)
    self.result = QLabel()
  
    up.addWidget(self.url)
    up.addWidget(self.btn)
    down.addWidget(self.result)
    root.addLayout(up)
    root.addLayout(down)
    
    self.btn.clicked.connect(self.add_btn_clicked)
    self.setLayout(root)

  def add_btn_clicked(self):
    result = add_url_to_file(self.url.text())
    if result == "VALID":
      self.result.setText("Stock Added")
    elif result == "EXIST":
      self.result.setText("Stock Already Exist")
    else:
      self.result.setText("Please Enter a Valid Address")



class MainApp(QWidget):
  def __init__(self):
    super(MainApp, self).__init__()
    self.setGeometry(100, 150, 700, 400)
    self.setWindowTitle("Bloomberg Stock Checker")
    self.initUI()
  
  def initUI(self):
    grid = QGridLayout()
    self.setLayout(grid)
    self.widgets = []

    names = ['Stocks', 'stock_combobox', 'x', 'x', 'x', 'refresh', 
              'Name', '', 'x', 'x', 'x', 'x', 
              'Price', '', 'x', 'Currency', '', 'x', 
              'Open', '', 'Prev Close', '', 'Volume', '',
              'Market Cap', '', 'Day Range', '', '52 Week Range', '']
    
    positions = [(y, x) for y in range(5) for x in range(6)]

    for position, name in zip(positions, names):
      if name == 'x':
        continue
      elif name == '':
        label = QLabel()
        label.setText("")
        grid.addWidget(label, *position)
        self.widgets.append(label)
      elif "_combobox" in name:
        self.combobox = QComboBox()
        grid.addWidget(self.combobox, *position)
      elif 'refresh' in name:
        refreshBtn = QPushButton("Refresh \nData")
        grid.addWidget(refreshBtn, *position)
        refreshBtn.clicked.connect(self.refreshBtn_pressed)
      else:
        label = QLabel()
        label.setText(name)
        grid.addWidget(label, *position)
        self.widgets.append(label)
        
    

  def refreshBtn_pressed(self):
    refresh_data()
    self.add_comboBox_item(self.combobox)

  def read_json_data(self):
    with open('data.json') as file:
      data = json.load(file)

    return data
    

  def add_comboBox_item(self, combobox):
    stock_names = self.read_json_data()
    self.combobox.clear()
    for i in stock_names.keys():
      combobox.addItem(i)
    
    combobox.activated[str].connect(self.check_stock)

  def check_stock(self, name):
    stock_names = self.read_json_data()
    data = stock_names[name]
    for i in range(0, len(self.widgets)):
      if i == 19:
        pass
      if self.widgets[i].text() != "":
        for k, v in data.items():
          if k == self.widgets[i].text():
            self.widgets[i+1].setText(v)
          
            
            
    
      
        
          



        # print(stock_names[i])
        # for key, value in stock_names[i].items():
        #   print(key+": " + value)
        

    







if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
