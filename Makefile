.PHONY: all clean build

ARCH := $(shell uname -m)
OS := $(shell uname -s)

all: build

pip_init:
	@echo "=> Installing pip requirements"
	pip install -r requirements.txt --break-system-packages

clean:
	@echo "=> Cleaning up"
	rm -rf dist/ build/ out/ tvdownloader.spec

build: clean pip_init
	@echo "=> Building TV Downloader for $(OS)-$(ARCH)"
	pyinstaller --onefile --clean --name tvdownloader __main__.py	
	mkdir out
	mv dist/tvdownloader out/tvdownloader
	rm -rf dist/ build/ tvdownloader.spec
	@echo "=> Done. Binary is in out/"