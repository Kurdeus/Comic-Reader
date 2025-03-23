pyi-makespec --add-data="assets\styles.css;assets" ^
  --add-data="assets\scripts.js;assets" ^
  --add-data="assets\menu.svg;assets" ^
  --add-data="assets\menu-light.svg;assets" ^
  --add-data="assets\scroll.svg;assets" ^
  --add-data="assets\scroll-light.svg;assets" ^
  --add-data="assets\boot.template.html;assets" ^
  --add-data="assets\doc.template.html;assets" ^
  --add-data="assets\img.template.html;assets" ^
  --add-data="assets\roboto-regular.woff2;assets" ^
  --add-data="assets\roboto-bold.woff2;assets" ^
  --add-data="assets\zenscroll.js;assets" ^
  --add-data="version;." ^
  --add-data="unrar.exe;." ^
  --icon="assets\app.ico" ^
  --name="ComicReader" ^
  --noconsole ^
setup.py && ^
pyinstaller --noconfirm ComicReader.spec