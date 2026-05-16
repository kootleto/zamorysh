import argparse
import os

from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, ".env")

load_dotenv(dotenv_path=dotenv_path)


def _add_bool_setting(parser, env_name, cmd_name, short_cmd_name, attr, help_text):
    default = os.getenv(env_name, "False").lower() == "true"
    parser.add_argument(
        f"-{short_cmd_name}",
        f"--{cmd_name}",
        action=argparse.BooleanOptionalAction,
        dest=attr,
        default=default,
        help=help_text + f" (default: {str(default).lower()})",
    )


def _parse_args():
    parser = argparse.ArgumentParser()
    _add_bool_setting(
        parser,
        "INCLUDE_DEMO",
        "demo",
        "d",
        "include_demo",
        "load content from content/demo",
    )
    _add_bool_setting(
        parser, "LOG_ENABLED", "log", "l", "log_enabled", "enable logging in terminal"
    )
    _add_bool_setting(parser, "GUI_MODE", "gui", "g", "gui", "run Kivy")
    return parser.parse_args()


SETTINGS = _parse_args()
