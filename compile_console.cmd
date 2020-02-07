pyinstaller skeleton.py --exclude-module matplotlib --exclude-module Qt5 --exclude-module PySide2 --exclude-module numpy --exclude-module PyQt5 
mkdir dist\skeleton\tinycss2
copy utils\tinycss2\version dist\skeleton\tinycss2
mkdir dist\skeleton\svg
copy svg\*.* dist\skeleton\svg
copy LICENCE dist\skeleton