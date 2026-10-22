"""Keep Windows awake by making a small mouse movement every 30 seconds."""

import ctypes
import os
import time
from ctypes import wintypes
from pathlib import Path


INTERVAL_SECONDS = 10
BASE_DIR = Path(__file__).resolve().parent
STOP_FILE = BASE_DIR / "STOP_MOUSE.flag"
LOCK_FILE = BASE_DIR / "MOUSE_RUNNING.lock"


class SingleInstance:
    """Hold an exclusive Windows file lock while the script is running."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle = None

    def acquire(self) -> bool:
        import msvcrt

        self.handle = self.path.open("a+")
        self.handle.write("1")
        self.handle.flush()
        self.handle.seek(0)
        try:
            msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            self.handle.close()
            self.handle = None
            return False
        return True

    def release(self) -> None:
        import msvcrt

        if self.handle is not None:
            self.handle.seek(0)
            msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            self.handle.close()
            self.handle = None


def nudge_mouse() -> None:
    """Send real relative mouse input and return the pointer to its position."""
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    mouse_event = user32.mouse_event
    mouse_event.argtypes = (
        wintypes.DWORD,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.DWORD,
        ctypes.POINTER(ctypes.c_ulong),
    )
    mouse_event.restype = None

    mouse_event(0x0001, 10, 0, 10, None)
    time.sleep(0.1)
    mouse_event(0x0001, -10, 0, -10, None)


def main() -> None:
    if os.name != "nt":
        raise RuntimeError("This script is intended to run on Windows.")

    STOP_FILE.unlink(missing_ok=True)
    instance = SingleInstance(LOCK_FILE)
    if not instance.acquire():
        return

    try:
        while True:
            for _ in range(INTERVAL_SECONDS * 10):
                if STOP_FILE.exists():
                    return
                time.sleep(0.1)
            nudge_mouse()
    except KeyboardInterrupt:
        pass
    finally:
        STOP_FILE.unlink(missing_ok=True)
        instance.release()


if __name__ == "__main__":
    main()