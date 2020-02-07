../.local/bin/pyinstaller -w skeleton.py --exclude-module matplotlib --exclude-m
mkdir dist/skeleton/tinycss2
cp utils/tinycss2/VERSION dist/skeleton/tinycss2/VERSION
mkdir dist/skeleton/svg
cp svg/* dist/skeleton/svg/
cp LICENSE dist/skeleton/LICENSE