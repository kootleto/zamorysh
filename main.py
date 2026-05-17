"""Для сборки EXE и APK."""

import asyncio
import os
import sys

import run

# для Pyinstaller, чтобы Kivy не потерял пути
if hasattr(sys, "_MEIPASS"):
    os.chdir(getattr(sys, "_MEIPASS"))

if __name__ == "__main__":
    asyncio.run(run.main())
