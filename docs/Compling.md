To compile a generated Pyder app:

1. Go into your generated project.
2. Install the frontend dependencies in `src/frontend`.
3. Run `python run.py compile`.

For local runtime without rebuilding, use `python window.py`. That opens the already-built app from `src/frontend/dist/index.html`.

Example on Linux/macOS:

```bash
cd my-pyder-app/src/frontend
npm install
cd ../..
venv/bin/python run.py compile
```

Example on Windows PowerShell:

```powershell
cd my-pyder-app\src\frontend
npm install
cd ..\..
venv\Scripts\python run.py compile
```

This command builds the Vite frontend and packages the app with PyInstaller. The packaged app is written to the project's `dist/` directory as a folder-based bundle for faster startup.
