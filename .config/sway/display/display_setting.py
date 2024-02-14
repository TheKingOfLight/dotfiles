#!/usr/bin/env python3

"""
Apply display settings using swaymsg based on a JSON configuration file.

Version: 0.4
Author: King of the light
License: GNU General Public License v3.0
License URL: https://www.gnu.org/licenses/gpl-3.0.html
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys


def load_json(json_file: str) -> dict:
    """
    Load JSON data from a file.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(
            "Configuration file '%s' not found. Please check if the file exists.", json_file)
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(
            "Invalid JSON format in configuration file '%s'. Please ensure the file contains valid JSON data.", json_file)
        sys.exit(1)

    return data


def check_config_format(data: dict) -> bool:
    """
    Check the format of the JSON data.
    Ensure there is a mode called "default" with required parameters.
    This ensures that in swaymsg specifed settings are available.
    """

    if 'default' not in data:
        logging.error(
            "'default' mode not found in the configuration file.")
        sys.exit(1)

    for mode, mode_settings in data.items():
        for display, settings in mode_settings.items():
            # Check if display is a string without special characters and spaces

            if not isinstance(display, str) or not re.match(r'^[a-zA-Z0-9_-]+$', display):
                logging.error(
                    "Display '%s' in mode '%s' is invalid. Display names must be strings without special characters or spaces.", display, mode)
                sys.exit(1)

            # Check if settings are strings and not lists

            for setting_name, setting_value in settings.items():
                if not isinstance(setting_value, str):
                    logging.error(
                        "Setting '%s' for display '%s' in mode '%s' must be a string.", setting_name, display, mode)
                    sys.exit(1)

    return True


def execute_swaymsg(display: str, settings: dict[str, str]) -> int:
    """
    Use swaymsg to change the display settings.
    All settings of specified display are set to the specified settings
    """
    command = [
        'swaymsg', 'output', display,

        'mode', settings['MODE'],
        'position', settings['POSITION'],
        'scale', settings['SCALE'],
        'scale_filter', settings['SCALE_FILTER'],
        'background', settings['BACKGROUND'],
        'transform', settings['TRANSFORM'],
        'max_render_time', settings['RENDER_TIME'],
        'adaptive_sync', settings['SYNC'],
        'render_bit_depth', settings['BIT_DEPTH'],
        settings['ENABLE']
    ]
    result = subprocess.run(command, check=False)

    if result.returncode != 0:
        logging.error(
            "Executing swaymsg for display %s. Return code: %s", display, result.returncode)
        sys.exit(result.returncode)

    logging.info("Swaymsg executed successfully for display %s.", display)

    return result.returncode


def apply_settings(mode: str, data: dict) -> None:
    """
    Itterates over all specifed Displays in the mode to
    change the settings using execute_swaymsg().
    Collects all return codecs from the command.

    The settings specified in the mode will be merged with
    settings in 'default' if some settings are not specified.
    """

    if 'default' in data:
        default_settings = data['default']
    else:
        logging.error(
            "'default' mode settings not found in the configuration file. \n Verify the configuration file.")
        sys.exit(1)

    if mode in data:
        mode_settings = data[mode]
    else:
        logging.error(
            "Mode '%s' not found in the configuration file. \n Either you specified a wrong mode or the configuration file is bad.", mode)
        sys.exit(1)

    return_codes = []

    for display, settings in default_settings.items():
        mode_display_settings = mode_settings.get(display, {})
        # Merge default and mode settings
        settings = {**settings, **mode_display_settings}
        return_codes.append(execute_swaymsg(display, settings))

    if max(return_codes) == 0:
        logging.info("Successfully changed to mode %s.", mode)
    else:
        logging.error(
            "Could not change to mode %s because of an error in swaymsg", mode)

    # Exit with the highest return code from swaymsg
    sys.exit(max(return_codes))


def handle_arguments(parser: argparse.ArgumentParser, args: argparse.Namespace) -> argparse.Namespace:
    """
    Check the arguments for errors.
    Check if there's a conflict between arguments
    Handle outpu of arguments that only print information
    """
    exclude_list = [args.mode, args.mode_list,
                    args.check_settings, args.license]

    if sum(bool(x) for x in exclude_list) > 1:
        parser.error(
            "Argument error: Conflicting arguments. Please consider that some arguments exclude each other.")
        parser.print_help()

    if sum(bool(x) for x in exclude_list) == 0:
        parser.error(
            "Argument error: No mode provided. Please choose a mode or another argument.")
        parser.print_help()

    if args.license:
        print("Author: King of the light")
        print("License: GNU General Public License v3.0")
        print("License URL: https://www.gnu.org/licenses/gpl-3.0.html")
        sys.exit(0)

    # Determine the path to the JSON configuration file.
    #
    # Default: display-settings-{hostname}.json if no path is specified
    # Else use the specified file

    if args.config:
        config_file = args.config
    else:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        hostname = os.uname().nodename
        config_file = os.path.join(
            script_directory, f"display-settings-{hostname}.json")
    args.config = config_file

    if args.check_settings:
        config = load_json(config_file)
        check_config_format(config)
        print("JSON settings check passed successfully.")
        sys.exit(0)

    if args.mode_list:
        config = load_json(config_file)
        print("Available modes:")

        for mode in config.keys():
            print(f"  - {mode}")
        sys.exit(0)

    return args


def parse_args() -> argparse.Namespace:
    """
    This function parses command-line arguments using argparse
    This defines the program's arguments and returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog=f'{os.path.basename(__file__)}',
        description='Apply display settings using swaymsg based on a JSON configuration file.')
    parser.add_argument(
        'mode', nargs='?', help='Specify the mode to apply from the configuration file')
    parser.add_argument(
        '-c', '--config', help='Specify a custom JSON configuration file.')
    parser.add_argument('-m', '--mode-list', action='store_true',
                        help='List available modes in the current json file.')
    parser.add_argument('--check-settings', action='store_true',
                        help='Check if JSON settings are correctly formatted.')
    parser.add_argument('--version', action='version', version='%(prog)s 0.4')
    parser.add_argument('--license', action='store_true',
                        help='Display author, license, and license URL.')

    args = handle_arguments(parser, parser.parse_args())

    return args


def main() -> None:
    """
    Main logic when the script is executed.
    """
    # Set up logging
    logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)s: %(message)s')

    args = parse_args()

    config = load_json(args.config)
    check_config_format(config)
    apply_settings(args.mode, config)


main()
