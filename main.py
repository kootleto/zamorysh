"""Для Buildozer: ему жизненно необходимо, чтобы файл назывался именно main.py."""

import asyncio

import run

if __name__ == "__main__":
    try:
        asyncio.run(run.main())
    except KeyboardInterrupt:
        print("Stopped by user")
