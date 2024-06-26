from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import os
import requests
import threading

from get_videos import get_videos
from settings import Settings
from lang import Lang

settings = Settings()
lang = Lang(settings.get('Settings', 'language'))

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

def create_icon_from_url(url):
    image_data = requests.get(url).content

    pixmap = QPixmap()
    pixmap.loadFromData(image_data)

    icon = QIcon(pixmap)
    return icon

class videoItem:
    def __init__(self, video, list_widget):
        # Create a QWidget to hold your item content
        item_widget = QWidget()

        # Create a layout for the item widget
        item_layout = QHBoxLayout()
        item_widget.setLayout(item_layout)

        # Create a image for the thumbnail form a url
        thumbnail_icon = create_icon_from_url(video.thumbnailUrl)
        thumbnail_label = QLabel()
        thumbnail_label.setPixmap(thumbnail_icon.pixmap(250, 250))
        item_layout.addWidget(thumbnail_label)
       
        # Create layout for the metadata
        metadata_layout = QVBoxLayout()

        # Create a label for the title
        title_label = QLabel(video.title)
        title_label.setWordWrap(True)
        font = title_label.font()
        font.setBold(True)
        title_label.setFont(font)
        metadata_layout.addWidget(title_label)

        # Create a label for the description
        description_text = video.description
        if len(description_text) > 200:
            description_text = description_text[:200] + '...'

        if description_text == '':
            description_text = lang.get('no-description')

        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        # set maximum length of description
        description_label.setMaximumWidth(300)
        metadata_layout.addWidget(description_label)

        # Create layout for date and download button
        date_layout = QHBoxLayout()

        # Create a label for the date
        date_label = QLabel(video.date)
        date_layout.addWidget(date_label, stretch=1000)

        # Create button to download the video
        if video.exists():
            download_button = QPushButton('gedownload')
            download_button.setEnabled(False)
            date_layout.addWidget(download_button)
        else:
            download_button = QPushButton('Download')
            download_button.clicked.connect(lambda: video.download(date_layout, settings.get('Settings', 'download_path')))
            date_layout.addWidget(download_button)

        # Add the metadata layout to the item layouts
        
        metadata_layout.addLayout(date_layout)
        item_layout.addLayout(metadata_layout, stretch=1000)

        # Create a QListWidgetItem and set the item widget as its widget
        list_item = QListWidgetItem()
        list_item.setSizeHint(item_widget.sizeHint())  # Set size hint to ensure proper sizing
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, item_widget)

class MainApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon(resource_path('data/logo/logo-256x256.png')))
        
        self.app.setApplicationName('tvdownloader')
        self.app.setDesktopFileName('tvdownloader.desktop')

        self.window = QWidget()
        self.window.setWindowTitle('TV Downloader')
        self.window.setWindowIcon(QIcon(resource_path('data/logo/logo-256x256.png')))
        self.window.show()
        self._create_widgets()
        self._create_menubar()


    def _create_menubar(self):
        self.menubar = QMenuBar(self.window)
        self.window.layout().setMenuBar(self.menubar)

        # create settings button
        settings_menu = self.menubar.addMenu(lang.get('menu'))
        settings_action = QAction(lang.get('settings'), self.window)
        settings_action.triggered.connect(lambda: SettingsApplication(self.window))
        settings_menu.addAction(settings_action)
        about_action = QAction(lang.get('about'), self.window)
        about_action.triggered.connect(lambda: AboutApplication(self.window))
        settings_menu.addAction(about_action)


    def _create_widgets(self):
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        # Create a search input field
        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self._handle_search)
        search_layout.addWidget(self.search_input, stretch=1000)

        # Create a search button
        self.search_button = QPushButton(lang.get('search'))
        self.search_button.clicked.connect(self._handle_search)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch(1)

        # Add the search layout to the main layout
        main_layout.addLayout(search_layout)

        # Create the content area. This is a list of search results
        self.search_results = QListWidget()
        main_layout.addWidget(self.search_results)

        self.window.setLayout(main_layout)
        self.event = threading.Event()

    def _handle_search(self):
        # This function will be called when the search button is clicked        
        search_query = self.search_input.text()

        # Clear the search results
        self.search_results.clear()

        videos = get_videos(search_query, settings,self.window)
        for video in videos:
            videoItem(video, self.search_results)

    def run(self):
        self.app.exec()

class SettingsApplication:
    def __init__(self, window):
        # Create a new dialog window
        self.window = QDialog(window)
        self.window.setWindowTitle(lang.get('settings'))
        self.window.setWindowIcon(QIcon(resource_path('data/logo/logo-256x256.png')))
        self.window.setMinimumSize(400, 300)
        self.window.show()
        self._create_widgets()

    def _create_widgets(self):
        layout = QVBoxLayout()
        download_layout = QHBoxLayout()
        save_layout = QHBoxLayout()

        # Create a label for the download path
        download_path_label = QLabel(lang.get('download_location'))
        download_layout.addWidget(download_path_label, stretch=1000)

        # Create a line edit for the download path
        self.download_path_input = QLabel()
        self.download_path_input.setText(settings.get('Settings', 'download_path'))
        download_layout.addWidget(self.download_path_input)

        # create a button and use a slot to connect it to the function
        download_button = QPushButton(lang.get('open'))
        # add the standard folder icon to the button
        download_button.setIcon(QIcon.fromTheme('folder'))

        download_button.clicked.connect(lambda: self._download_button_action())
        download_layout.addWidget(download_button)

        # create a language setting
        language_layout = QHBoxLayout()

        selectedLang = settings.get('Settings', 'language')
        if selectedLang == '':
            selectedLang = lang.getLanguage()

        language_label = QLabel(lang.get('language'))
        language_layout.addWidget(language_label)
        self.language_combobox = QComboBox()
        languages = lang.getLanguages()
        languages.remove(selectedLang)
        languages.insert(0, selectedLang)
        for language in languages:
            self.language_combobox.addItem(language)

        language_layout.addWidget(self.language_combobox)

        # create vrt account settings
        vrt_account_layout = QHBoxLayout()
        vrt_account_label = QLabel(lang.get('vrt_account'))
        vrt_account_layout.addWidget(vrt_account_label)
        self.vrt_account_email_input = QLineEdit(settings.get('Vrt', 'email'))
        self.vrt_account_email_input.setPlaceholderText(lang.get('e-mail'))
        self.vrt_account_email_input.width = 400
        vrt_account_layout.addWidget(self.vrt_account_email_input)
        self.vrt_account_input = QLineEdit(settings.get('Vrt', 'password'))
        self.vrt_account_input.setPlaceholderText(lang.get('password'))
        self.vrt_account_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.vrt_account_input.width = 250
        vrt_account_layout.addWidget(self.vrt_account_input)
    
        # add a save button
        save_button = QPushButton(lang.get('save'))
        save_button.clicked.connect(lambda: self._save_button_action())
        save_layout.addWidget(save_button)

        layout.addLayout(download_layout)
        layout.addLayout(language_layout)
        layout.addLayout(vrt_account_layout)
        layout.addLayout(save_layout)

        self.window.setLayout(layout)

    def _download_button_action(self):
        download_path = QFileDialog.getExistingDirectory(self.window, lang.get('select-download-location'))
        if download_path:
            self.download_path_input.setText(download_path)
            settings.set('Settings', 'download_path', download_path)

    def _save_button_action(self):
        settings.set('Settings', 'download_path', self.download_path_input.text())
        settings.set('Vrt', 'email', self.vrt_account_email_input.text())
        settings.set('Vrt', 'password', self.vrt_account_input.text())
        settings.set('Settings', 'language', self.language_combobox.currentText())
        lang.setLanguage(self.language_combobox.currentText())
        self.window.close()

class AboutApplication:
    def __init__(self, parent):
        # Create a new dialog window
        self.window = QDialog(parent)
        self.window.setWindowTitle('Over')
        self.window.setWindowIcon(QIcon(resource_path('data/logo/logo-256x256.png')))
        self.window.setMinimumSize(100, 150)

        # Create a layout for the window
        layout = QVBoxLayout()
        
        # Create a label with the about text
        about_text = QLabel(lang.get('about-text'))
        about_text.setWordWrap(True)
        layout.addWidget(about_text)

        # Create a layout for the version information and the close button
        version_layout = QHBoxLayout()

        # Create a version label
        version_text = QLabel(f'{lang.get("version")} 0.1.2 (beta)')
        version_layout.addWidget(version_text, stretch=1000)

        # Add a close button
        close_button = QPushButton(lang.get('Ok'))
        close_button.clicked.connect(self.window.close)
        version_layout.addWidget(close_button)

        layout.addLayout(version_layout)
        self.window.setLayout(layout)

        self.window.show()

if __name__ == '__main__':
    app = MainApplication()
    app.run()