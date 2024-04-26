import os
import sys

OS = sys.platform
ARCH = os.uname().machine

def _run_command(command):
    os.system(command)

def _createDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def _get_ffmpeg():
    FFMPEG_ARCH = ""

    if ARCH == "x86_64":
        FFMPEG_ARCH = "amd64"
    elif ARCH == "aarch64":
        FFMPEG_ARCH = "arm64"

    if FFMPEG_ARCH == "":
        print("=> Unsupported architecture")
        exit(1)
    
    if OS == "linux":
        _run_command(f"curl -L https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-{FFMPEG_ARCH}-static.tar.xz -o ffmpeg.tar.xz")
        _run_command("tar -xf ffmpeg.tar.xz")
        _run_command(f"mv ./ffmpeg-git-*-{FFMPEG_ARCH}-static/ffmpeg ./out/ffmpeg")
        _run_command(f"rm -rf ffmpeg.tar.xz ffmpeg-git-*-{FFMPEG_ARCH}-static")

    elif OS == "win32":
        pass
    
def install_dependencies():
    print("=> Installing dependencies...")
    _run_command("pip install -r requirements.txt")

def clean():
    print("=> Cleaning up...")

    if OS == "linux":
        _run_command("rm -rf dist/ build/ out/ tvdownloader.spec")
    elif OS == "win32":
        _run_command("rmdir /s /q dist build out")
        _run_command("del tvdownloader.spec")

def build_appimage():
    print("=> Building AppImage for {OS}-{ARCH}...")
    _run_command(f'curl -L https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-{ARCH}.AppImage -o appimagetool.AppImage')
    _run_command('chmod +x appimagetool.AppImage')
    _createDir('out/appimage.AppDir/usr/bin')
    _run_command(f'cp out/tvdownloader-{OS}-{ARCH} out/appimage.AppDir/usr/bin/tvdownloader')
    _run_command('cp data/appimage/* out/appimage.AppDir/')
    _run_command('cp data/logo/logo-256x256.png out/appimage.AppDir/')
    _run_command('chmod +x out/appimage.AppDir/AppRun')
    _run_command('chmod +x out/appimage.AppDir/tvdownloader.desktop')
    _run_command(f'ARCH={ARCH} ./appimagetool.AppImage out/appimage.AppDir out/tvdownloader-{OS}-{ARCH}.AppImage')
    _run_command('rm -rf out/appimage.AppDir appimagetool.AppImage')
    print(f"=> Built out/tvdownloader-{OS}-{ARCH}.AppImage")

def build():
    clean()
    install_dependencies()
    print(f"=> Building TV Downloader for {OS}-{ARCH}...")
    _createDir("out")
    _get_ffmpeg()

    if OS == "linux":
        _run_command('pyinstaller -F --add-data "./out/ffmpeg:./ffmpeg/" --add-data "./data/logo/logo-64x64.png:./data/logo/" --windowed --onefile --clean --name tvdownloader --icon=data/logo/logo.ico  gui/main.py')
        _run_command(f'mv dist/tvdownloader out/tvdownloader-{OS}-{ARCH}')
        _run_command('rm -rf dist/ build/ tvdownloader.spec ./out/ffmpeg')
        _run_command(f'chmod +x out/tvdownloader-{OS}-{ARCH}')
        print(f"=> Built out/tvdownloader-{OS}-{ARCH}")
        build_appimage()
    elif OS == "win32":
        pass    

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("=> Usage: python build.py [build|clean]")
        exit(1)
    elif args[0] == "build":
        build()
    elif args[0] == "clean":
        clean()
    

if __name__ == "__main__":
    main()