#!/usr/bin/env python3

"""
Apply display settings using swaymsg based on a JSON configuration file.

Version: 0.3
Author: King of the light
License: GNU General Public License v3.0
License URL: https://www.gnu.org/licenses/gpl-3.0.html
"""

import sys
import json
import subprocess
import os
import argparse
import re


def determine_config_path(custom_path):
    """
    Determine the path to the JSON configuration file.

    Default: display-settings-{hostname}.json
    Can be specified by the argument -c or --config
    """

    if custom_path:
        return custom_path
    else:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        hostname = os.uname().nodename

        return os.path.join(script_directory, f"display-settings-{hostname}.json")


def load_json(json_file):
    """
    Load JSON data from a file.
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(
            f"Error: Invalid JSON format in configuration file '{json_file}'.")
        sys.exit(1)

    return data


def check_config_format(data):
    """
    Check the format of the JSON data.
    Ensure there is a mode called "default" with required parameters.
    This ensures that in swaymsg specifed settings are available.
    """

    if 'default' not in data:
        print("Error: 'default' mode not found in the configuration file.")
        sys.exit(1)

    for mode, mode_settings in data.items():
        for display, settings in mode_settings.items():
            # Check if display is a string without special characters and spaces

            if not isinstance(display, str) or not re.match(r'^[a-zA-Z0-9_-]+$', display):
                print(
                    f"Error: Display '{display}' in mode '{mode}' is invalid. Display names must be strings without special characters or spaces.")
                sys.exit(1)
            # Check if settings are strings and not lists

            for setting_name, setting_value in settings.items():
                if not isinstance(setting_value, str):
                    print(
                        f"Error: Setting '{setting_name}' for display '{display}' in mode '{mode}' must be a string.")
                    sys.exit(1)


def execute_swaymsg(display, settings):
    command = [
        'swaymsg',
        'output', display, 'mode', settings['MODE'], ',',
        'output', display, 'position', settings['POSITION'], ',',
        'output', display, 'scale', settings['SCALE'], ',',
        'output', display, 'scale_filter', settings['SCALE_FILTER'], ',',
        'output', display, 'background', settings['BACKGROUND'], ',',
        'output', display, 'transform', settings['TRANSFORM'], ',',
        'output', display, 'max_render_time', settings['RENDER_TIME'], ',',
        'output', display, 'adaptive_sync', settings['SYNC'], ',',
        'output', display, 'render_bit_depth', settings['BIT_DEPTH'], ',',
        'output', display, settings['ENABLE']
    ]
    result = subprocess.run(command)

    if result.returncode != 0:
        print(
            f"Error executing swaymsg for display {display}. Return code: {result.returncode}")
        sys.exit(result.returncode)

    return (result.returncode)


def apply_settings(mode, data):
    if 'default' in data:
        default_settings = data['default']
    else:
        print("Error: 'default' mode settings not found in the configuration file.")
        print("Verify the configuration file.")
        sys.exit(1)

    if mode in data:
        mode_settings = data[mode]
    else:
        print(f"Error: Mode '{mode}' not found in the configuration file.")
        print("Ether you specified a wrong mode or the configuration file is bad.")
        sys.exit(1)

    return_codes = []

    for display, settings in default_settings.items():
        mode_display_settings = mode_settings.get(display, {})
        # Merge default and mode settings
        settings = {**settings, **mode_display_settings}
        return_codes.append(execute_swaymsg(display, settings))

    # Exit with the highest return code from swaymsg
    sys.exit(max(return_codes))


def list_available_modes(config_file):
    config = load_json(config_file)
    print("Available modes:")

    for mode in config.keys():
        print(f"  - {mode}")
    sys.exit(0)


def handle_arguments(parser, args):
    """
    Check the arguments for errors.
    Print the desired message and exit for "overriding" Arguments.
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
        list_available_modes(config_file)
        sys.exit(0)

    return args


def parse_args():
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
    parser.add_argument('--version', action='version', version='%(prog)s 0.2')
    parser.add_argument('--license', action='store_true',
                        help='Display author, license, and license URL.')

    args = handle_arguments(parser, parser.parse_args())

    return args


def main():
    args = parse_args()

    config = load_json(args.config)
    check_config_format(config)
    apply_settings(args.mode, config)


main()
