# Compile your Pyder app.
To compile your Pyder app, all you need to do (and make sure you're in the same folder as your project) is
```bash
python run.py compile
```
This commands compiles the app through Vite frontend, and bundles everything with PyInstaller.

# PyWebView Problem:
Depending on your operating system, PyWebView might be screwed up.

## Windows
All you need in windows is [WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2?form=MA13LH#download) and the app will run perfectly fine.

## Linux
- **GTK: OPENING** - you need `webkit2gtk4.1` in your package manager.
- **Qt: OPENING** - you need `qtwebkit` or `qt5-qtwebkit`. This has not been tested.
- **GTK & Qt: COMPILING** - Good luck soldier. I don't even remember what libraries I installed to compile the app.

## macOS
You don't need anything special to open the app. Just open it.