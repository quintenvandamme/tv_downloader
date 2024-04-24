.PHONY: all clean build

ARCH := $(shell uname -m)
OS := $(shell uname -s)

all: appimage

pip_requirements:
	@echo "=> Installing pip requirements"
	pip install -r requirements.txt --break-system-packages
	mkdir out

clean:
	@echo "=> Cleaning up"
	rm -rf dist/ build/ out/ tvdownloader.spec

download_ffmpeg:
	@echo "=> Downloading ffmpeg"
	curl -L https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz -o ffmpeg.tar.xz
	tar -xf ffmpeg.tar.xz
	mv ./ffmpeg-git-*-amd64-static/ffmpeg ./out/ffmpeg
	rm -rf ffmpeg.tar.xz ffmpeg-git-*-amd64-static

build: clean pip_requirements download_ffmpeg
	@echo "=> Building TV Downloader for $(OS)-$(ARCH)"
	pyinstaller -F --add-data "./out/ffmpeg:./ffmpeg/" --add-data "./data/logo/logo-64x64.png:./data/logo/" --windowed --onefile --clean --name tvdownloader --icon=data/logo/logo.ico  gui/main.py
	mv dist/tvdownloader out/tvdownloader-$(OS)-$(ARCH)
	rm -rf dist/ build/ tvdownloader.spec ./out/ffmpeg
	chmod +x out/tvdownloader-$(OS)-$(ARCH)
	@echo "=> Done. Binary is in out/"

appimage: build
	@echo "=> Downloading AppImage Tool"
	curl -L https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-$(ARCH).AppImage -o appimagetool.AppImage
	chmod +x appimagetool.AppImage
	@echo "=> Building AppImage"
	mkdir -p out/appimage.AppDir
	mkdir -p out/appimage.AppDir/usr/bin
	cp  out/tvdownloader-$(OS)-$(ARCH) out/appimage.AppDir/usr/bin/tvdownloader
	cp data/appimage/* out/appimage.AppDir/
	cp data/logo/logo-256x256.png out/appimage.AppDir/
	chmod +x out/appimage.AppDir/AppRun
	chmod +x out/appimage.AppDir/tvdownloader.desktop
	ARCH=$(ARCH) ./appimagetool.AppImage out/appimage.AppDir out/tvdownloader-$(OS)-$(ARCH).AppImage 
	rm -rf out/appimage.AppDir appimagetool.AppImage
	@echo "=> Done. AppImage is in out/"