from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys
import os
import requests
import threading

from get_videos import get_videos
from settings import Settings

settings = Settings()

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
        settings_menu = self.menubar.addMenu('Menu')
        settings_action = QAction('Instellingen', self.window)
        settings_action.triggered.connect(lambda: SettingsApplication(self.window))
        settings_menu.addAction(settings_action)
        about_action = QAction('Over', self.window)
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
        self.search_button = QPushButton('Zoeken')
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
        videos = get_videos(search_query, settings)
        for video in videos:
            videoItem(video, self.search_results)

    def run(self):
        self.app.exec()

class SettingsApplication:
    def __init__(self, window):
        # Create a new dialog window
        self.window = QDialog(window)
        self.window.setWindowTitle('Instellingen')
        self.window.setWindowIcon(QIcon(resource_path('data/logo/logo-256x256.png')))
        self.window.setMinimumSize(600, 300)
        self.window.show()
        self._create_widgets()

    def _create_widgets(self):
        layout = QVBoxLayout()
        download_layout = QHBoxLayout()
        save_layout = QHBoxLayout()

        # Create a label for the download path
        download_path_label = QLabel('Download locatie:')
        download_layout.addWidget(download_path_label, stretch=1000)

        # Create a line edit for the download path
        self.download_path_input = QLabel()
        self.download_path_input.setText(settings.get('Settings', 'download_path'))
        download_layout.addWidget(self.download_path_input)

        # create a button and use a slot to connect it to the function
        save_button = QPushButton('Open')
        # add the standard folder icon to the button
        save_button.setIcon(QIcon.fromTheme('folder'))

        save_button.clicked.connect(lambda: self._save_settings())
        download_layout.addWidget(save_button)

        layout.addLayout(download_layout)
        layout.addLayout(save_layout)

        self.window.setLayout(layout)

    def _save_settings(self):
        download_path = QFileDialog.getExistingDirectory(self.window, 'Selecteer een download locatie')
        if download_path:
            self.download_path_input.setText(download_path)
            settings.set('Settings', 'download_path', download_path)

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
        about_text = QLabel('TV Downloader is een applicatie die het mogelijk maakt om video\'s van verschillende nieuwswebsites te downloaden.')
        about_text.setWordWrap(True)
        layout.addWidget(about_text)

        # Create a layout for the version information and the close button
        version_layout = QHBoxLayout()

        # Create a version label
        version_text = QLabel('Versie 0.1.1 (beta)')
        version_layout.addWidget(version_text, stretch=1000)

        # Add a close button
        close_button = QPushButton('Ok')
        close_button.clicked.connect(self.window.close)
        version_layout.addWidget(close_button)

        layout.addLayout(version_layout)
        self.window.setLayout(layout)

        self.window.show()

if __name__ == '__main__':
    app = MainApplication()
    app.run()

# test
# https://www.hln.be/buitenland/live-gijzeling-in-nederlands-cafe-voorbij-vier-slachtoffers-vrijgelaten-gijzelnemer-geboeid-door-de-politie~a0dfda52/
# https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/2024/vrt-nws-journaal-vrt-nws-journaal-laat-20240421/
# https://focus-wtv.be/nieuws/miss-belgie-west-vlaamse-finalisten-vallen-niet-in-de-prijzen
# https://www.bruzz.be/actua/politiek/vlaams-minister-van-brussel-regering-blinkt-uit-passiviteit-en-inertie-2024-02-21
# https://www.tvoost.be/nieuws/jan-tratnik-wint-omloop-oliver-naesen-heel-knap-vierde-als-je-vooraf-de-benen-niet-kan-inschatten-is-dit-een-mooi-resultaat-165206
# https://www.tvl.be/nieuws/jongeren-die-voor-het-eerst-stemmen-weten-weinig-of-niets-over-de-verkiezingen-165198
# https://www.robtv.be/nieuws/weekwas-zaterdag-24-februari-165193
# https://www.hln.be/video/productie/we-hebben-de-ram-bij-de-horens-gevat-letterlijk-428950
# https://www.nieuwsblad.be/cnt/dmf20240225_94177728
# https://www.vrt.be/vrtmax/a-z/vrt-nws-journaal/2024/vrt-nws-journaal-vrt-nws-journaal-13u-20240225
# https://www.rtv.be/regionale-sport/wout-van-aert-wil-meteen-scoren-tijdens-openingsweekend
# https://www.vrt.be/vrtnws/nl/kijk/2024/02/25/d7d-oekraine-oorlog-iryna-mudra-gevlucht-met-zoon-nooit-opgeven-/
# https://www.vrt.be/vrtnws/nl/2024/02/26/liveblog-boerenprotest/
# https://www.gva.be/cnt/dmf20240229_96365490
# https://www.ringtv.be/felicitaties-voor-drie-jarigen-die-op-schrikkeldag-jarig-zijn
# https://www.standaard.be/cnt/dmf20231113_92216398
# https://www.vrt.be/vrtnws/nl/2024/02/29/poetin-toespraak-parlement/