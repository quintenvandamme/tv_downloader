import locale

class Lang:
    def __init__(self, lang=None):
        loc = locale.getdefaultlocale()[0]

        if lang is None or lang == "":
            if loc.startswith("en_"):
                self.lang = "en"
            elif loc.startswith("nl_"):
                self.lang = "nl"
            elif loc.startswith("de_"):
                self.lang = "de"
            elif loc.startswith("fr_"):
                self.lang = "fr"
            else:
                self.lang = "en"
        else:
            self.lang = lang

    def get(self, key):
        if self.lang == "en":
            return en[key]
        elif self.lang == "nl":
            return nl[key]
        elif self.lang == "de":
            return de[key]
        elif self.lang == "fr":
            return fr[key]
        
    def getLanguages(self):
        languages = ["en", "nl", "de", "fr"]
        return languages

    def getLanguage(self):
        return self.lang

    def setLanguage(self, lang):
        self.lang = lang
        
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
    "no-description": "No description available",
    "save": "Save",
    "language": "Language",
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
    "no-description": "Geen beschrijving beschikbaar",
    "save": "Opslaan",
    "language": "Taal",
}

de = {
    "menu": "Menü",
    "settings": "Einstellungen",
    "about": "Über",
    "search": "Suche",
    "download_location": "Download Standort:",
    "open": "Öffnen",
    "vrt_account": "VRT Konto",
    "e-mail": "E-Mail",
    "password": "Passwort",
    "select-download-location": "Download Standort auswählen",
    "about-text": "TV Downloader ist eine Anwendung, die es Ihnen ermöglicht, Videos von verschiedenen Nachrichtenwebsites herunterzuladen.",
    "version": "Version",
    "Ok": "Ok",
    "no-description": "Keine Beschreibung verfügbar",
    "save": "Speichern",
    "language": "Sprache",
}

fr = {
    "menu": "Menu",
    "settings": "Paramètres",
    "about": "À propos",
    "search": "Rechercher",
    "download_location": "Emplacement de téléchargement:",
    "open": "Ouvrir",
    "vrt_account": "Compte VRT",
    "e-mail": "E-mail",
    "password": "Mot de passe",
    "select-download-location": "Sélectionner l'emplacement de téléchargement",
    "about-text": "TV Downloader est une application qui vous permet de télécharger des vidéos à partir de différents sites d'actualités.",
    "version": "Version",
    "Ok": "Ok",
    "no-description": "Aucune description disponible",
    "save": "Enregistrer",
    "language": "Langue",
}