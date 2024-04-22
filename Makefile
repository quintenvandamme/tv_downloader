.PHONY: all clean build

ARCH := $(shell uname -m)
OS := $(shell uname -s)

all: build

pip_init:
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

build: clean pip_init download_ffmpeg
	@echo "=> Building TV Downloader for $(OS)-$(ARCH)"
	pyinstaller -F --add-data "./out/ffmpeg:./ffmpeg/" --onefile --clean --name tvdownloader __main__.py	
	mv dist/tvdownloader out/tvdownloader-$(OS)-$(ARCH)
	rm -rf dist/ build/ tvdownloader.spec ./out/ffmpeg
	@echo "=> Done. Binary is in out/"