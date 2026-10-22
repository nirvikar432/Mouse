# Mouse Keep-Alive

A small Windows utility that periodically moves the mouse pointer by a few
pixels and immediately returns it to its original position. This can help
prevent a Windows computer from being considered idle.

## Requirements

- Windows
- Python 3.8 or newer
- No third-party Python packages

The script uses only Python standard-library modules and the Windows `user32`
API.

## Usage

### Start

Double-click `START_MOUSE.bat`, or run the following from Command Prompt or
PowerShell:

```powershell
pythonw.exe SCRIPT.PY
```

The script runs in the background and nudges the mouse every 10 seconds.
Starting it again while it is already running has no effect because the
`MOUSE_RUNNING.lock` file prevents multiple instances.

### Stop

Double-click `STOP_MOUSE.bat`. The running process checks for the stop signal
and exits cleanly. You can also stop the process with `Ctrl+C` when running it
with `python.exe` in a terminal.

## Files

| File | Purpose |
| --- | --- |
| `SCRIPT.PY` | Main keep-alive script |
| `START_MOUSE.bat` | Starts the script without opening a console window |
| `STOP_MOUSE.bat` | Creates the stop signal file |
| `START_MOUSE.lnk` | Optional Windows shortcut for starting the utility |
| `MOUSE_RUNNING.lock` | Runtime lock used to enforce a single instance |
| `STOP_MOUSE.flag` | Temporary stop signal created while stopping |

`MOUSE_RUNNING.lock` and `STOP_MOUSE.flag` are runtime files. They are
excluded from version control by `.gitignore`.

## Notes

- The utility is intended for computers you own or are authorized to operate.
- The mouse movement is relative and is reversed immediately, so the pointer
  should remain in its original position.
- The script intentionally supports Windows only.
