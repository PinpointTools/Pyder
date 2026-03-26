# AGENTS.md
This applies to whatever LLM you're using. Codex, Claude, Gemini, whatever.

---

This project is a cross-desktop platform to making webapps with python as the backend. Your job is to help the user on fixing bugs, adding features, etc..

## On where to edit where the files, there are 2 main files.
- [@src/interactive.py](src/interactive.py)
  - This file contains the user options to pick. This includes:
    - Inputting their Project Name
      - If the project name contains spaces, special characters, and uppercase letters (eg; Pyder Project!!), it will convert it to something more compatible (eg; pyder-project).
    - Inputting their domain system
      - Domain system such as putting as their indentifier. For example, something like `io.github.pinpointtools`. And for the production, it would return `io.github.pinpointtools.pyder-project`. This goes as `{tld}.{second-level domain}.{subdomain}`
    - Selecting between GTK or Qt.
      - This app is built with the intention to make it cross-desktop platform. For Windows, Linux and macOS. GTK and Qt is a option for Linux, as this is required for picking the correct renderer. And this options is only meant for Linux and will be asked in all platform.
    - Selecting frameworks.
      - The user currently has 4 different options to pick for their project: That being:
        - Vanilla
        - Svelte
        - React
        - Vue
    - Selecting variant.
      - This being able to use JavaScript or TypeScript.
    - Selecting their NodeJS Package Manager
      - The user has 2 different options to pick for their project: That being:
        - npm : NodeJS's default package manager.
        - pnpm : A faster alternative to npm.
        - 
- [@src/initialize.py](src/initialize.py)
  - This is where when the user confirms that it's ready to be initialized, it starts here. This includes:
    - Copying icons.
      - From `{pyderProjectRoot}/icon/*` to `{userProject}/icon/`
    - Creating file structure.
      - `{userProject}/`
      - `{userProject}/icon`
      - `{userProject}/src/frontend`
      - `{userProject}/src/backend`
    - Creating files such as:
      - `window.py`
        - Runs pywebview. Having the option to be able to use dev mode or compiled mode.
          - Dev mode being, running the page at `http://localhost:5173`.
          - Compiled mode being, running the page at `src/frontend/dist/index.html`.
      - `run.py`
        - This is where the user can run the flags like `dev`, `compile`, `test`.
          - `dev` flag:
            - This will run the development server in `src/frontend/` from `subprocess.Popen`, which will open the server in a thread.
            - And after a second, it will run pywebview and opening a page at `http://localhost:5173`.
          - `build` flag:
            - It first builds the app in `src/frontend/` with nothing special. Just doing `npm/pnpm run build`.
            - After that, it will compile for Python. Pywebview, and the other packages the user installed.
            - Once all of that is finished, everything will be compiled to `dist/{userProject}`.
        - `test` flag:
          - It first builds the app in `src/frontend/` with nothing special. Just doing `npm/pnpm run build`.
          - Then, instead of building for python, it will open the window. That's it.
      - `src/backend/api.py`
        - This is where the user can do all their Python contacting things. There's only one function and that's getting the user's operating system, and then returning their config path.
      - `.gitignore`
        - This just has the ignores for pnpm, python and other things. Mainly used when the user wants to put their project to GitHub, GitLab, GitBucket, etc...
      - `pyder.py`
        - This is the Pyder settings things. This includes:
          - `projectName` : string
          - `domainSystem` : string
          - `projectID` : string
          - `version` : string
          - `window` : array
            - `minSize` : array of int
            - `maxSize` : array of int
            - `initSize` : array of int
      - `requirements.txt`
        - This includes all the initializing libraries for Pyder. This includes
          - `pyinstaller` : to compile the app.
          - `pywebview` : for the native-window.
            - `pywebview[gtk]` : installs the required GTK libraries
            - `pywebview[qt]` : installs the required Qt libraries
    - Initializing npm with their preferred node packagae manager and their preferred framework with vite.
    - Creating a python virtual environment.
    - Installing python packages in the virtual environment.
    - Finishes everything with a print.

## The other files are just meant to help.
- [@src/print.py](src/print.py)
  - This handles all the printing with termcolor.
    - `print.sucsess("")`
    - `print.log("")`
    - `print.error("")`
    - `print.warning("")`
- [@main.py](main.py)
  - This handles running the [@src/initialize.py](src/initialize.py) script.
  - When terminated, doesn't show errors and says it was cancelled by the user.
- [@tests.py](tests.py)
  - This is only meant for testing. This should not be used for production.
  - For what it initializes:
    - `projectName` : "Project Test"
    - `projectID` : "project-test"
    - `domainSystem` : "io.github.pinpointtools"
    - `gtkorqt` : "GTK"
    - `framework` : "React"
    - `variant` : "TypeScript"
    - `packageManager` : "pnpm"

## What YOU should do:
Instead of using [@main.py](main.py), you should use [@tests.py](tests.py) and check the code inside `project-test`. If you used [@main.py](main.py), then the user will be prompted to make their options intead of it being just initializing with the things inside [@tests.py](tests.py)

You should NOT touch [@CONTRIBUTING.md](CONTRIBUTING.md), [@README.md](README.md), [@LICENSE](LICENSE), and [@CHANGELOG.md](CHANGELOG.md). These files are not meant to touch by a LLM. Same thing applies to `git` commands too. Except for `git diff`, `git status` and other commands that doesn't change anything.

This project prefers to have every variable and functions to be `camelCase`, as it it widely used around the whole project. Please do NOT use anything other than `camelCase`.

---

No this AGENT.md isn't made by an LLM, it's made by a human being. Or, dog. I don't know. This is made by Daveberry.