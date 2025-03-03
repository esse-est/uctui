## UC-TUI
UC-TUI (unicurses-terminal user interface) is a Python project, made to be ran on simple, headless devices.

It consists primarily of `uctui.py` and the `apps/` directory. `uctui.py` is the actual runner, the "TUI" of it all. From there, apps can be called that are found inside the `apps/` directory. This format means that plugins/third party apps can be easily implimented.



___

### Installation

#### Requirements:

Python3, unicurses installed in venv.

#### Setup Venv/Conda:
This isn't included as it most often boils down to user preference, but for quick setup run the one-liner:
`mkdir .venv && python3 -m venv .venv`

#### Config Values:
Again, specifics vary based off of personal preference, just have a look through `config.txt` prior to running UC-TUI for the first time.

___

### Running:

Running `python3 uctui.py` should suffice most of the time, see `config.txt` for more information.