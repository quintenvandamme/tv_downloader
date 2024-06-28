import locale

class Lang:
    def __init__(self, lang=None):
        loc = locale.getdefaultlocale()[0]

        if lang is None:
            if loc.startswith("en_"):
                self.lang = "en"
            elif loc.startswith("nl_"):
                self.lang = "nl"
            else:
                self.lang = "en"
        else:
            self.lang = lang

    def get(self, key):
        if self.lang == "en":
            return en[key]
        elif self.lang == "nl":
            return nl[key]
        
en = {
    "menu": "Menu",
    "settings": "Settings",
    "about": "About",
    "search": "Search",
    "download_location": "Download location:",
    "open": "Open",
    "vrt_account": "VRT account",
    "e-mail": "E-mail",
    "password": "Password",
    "select-download-location": "Select download location",
    "about-text": "TV Downloader is an application that allows you to download videos from various news websites.",
    "version": "Version",
    "Ok": "Ok",
}

nl = {
    "menu": "Menu",
    "settings": "Instellingen",
    "about": "Over",
    "search": "Zoeken",
    "download_location": "Download locatie:",
    "open": "Open",
    "vrt_account": "VRT account",
    "e-mail": "E-mail",
    "password": "Wachtwoord",
    "select-download-location": "Selecteer een download locatie",
    "about-text": "TV Downloader is een applicatie die het mogelijk maakt om video\'s van verschillende nieuwswebsites te downloaden.",
    "version": "Versie",
    "Ok": "Ok",
}