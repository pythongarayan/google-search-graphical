import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import webbrowser

class GoogleSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayoutDirection(Qt.RightToLeft)
        layout = QVBoxLayout()

        # اضافه کردن لوگو
        logo_label = QLabel(self)
        pixmap = QPixmap('path_to_logo.png')  # مسیر لوگو را اینجا وارد کنید
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Search input and button
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.perform_search)
        search_button = QPushButton('جستجو')
        search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)

        # Results list
        self.results_list = QListWidget()
        self.results_list.setLayoutDirection(Qt.RightToLeft)
        self.results_list.itemDoubleClicked.connect(self.open_link)

        layout.addLayout(search_layout)
        layout.addWidget(self.results_list)

        self.setLayout(layout)
        self.setWindowTitle('جستجوی گوگل')
        self.setGeometry(300, 300, 600, 400)

    def perform_search(self):
        query = self.search_input.text()
        url = f"https://www.google.com/search?q={query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            self.results_list.clear()
            for result in soup.find_all('div', class_='g'):
                title_element = result.find('h3')
                link_element = result.find('a')
                
                if title_element and link_element:
                    title = title_element.text
                    link = link_element['href']
                    if link.startswith('/url?q='):
                        link = link.split('/url?q=')[1].split('&')[0]
                    self.results_list.addItem(f"{title}\n{link}")
        except Exception as e:
            print(f"خطایی رخ داد: {e}")

    def open_link(self, item):
        link = item.text().split('\n')[1]
        webbrowser.open_new(link)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GoogleSearchApp()
    ex.show()
    sys.exit(app.exec_())
