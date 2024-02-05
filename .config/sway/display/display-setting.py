#!/usr/bin/env python3

"""
Apply display settings using swaymsg based on a JSON configuration file.

Version: 0.1
Author: King of the light
License: GNU General Public License v3.0
License URL: https://www.gnu.org/licenses/gpl-3.0.html
"""

import sys
import json
import subprocess
import os


def print_help():
    print(f"Usage: {sys.argv[0]} <mode> [options]")
    print("Options:")
    print("  -c <json_file>, --config=<json_file>  Specify a custom JSON configuration file.")
    print("  -m, --mode                             List available modes in the curent json file.")
    print("  -h, --help                             Display this help message.")


def determine_config_path():
    """
    Determine the path to the JSON configuration file.

    Default: display-settings-{hostname}.json
    Can be specified by the argument -c or --config
    """
    if '-c' in sys.argv or '--config' in sys.argv:
        import json
        try:
            index = sys.argv.index('-c')
            custom_config_file = sys.argv[index + 1]
            return custom_config_file
        except IndexError:
            print("Error: No configuration file provided with -c option.")
            sys.exit(1)
        except ValueError:
            print("Error: Invalid usage of -c option.")
            sys.exit(1)
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


def execute_swaymsg(display, settings):
    import subprocess
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
        print_help()
        sys.exit(1)

    return_codes = []

    for display, settings in default_settings.items():
        mode_display_settings = mode_settings.get(display, {})
        # Merge default and mode settings
        settings = {**settings, **mode_display_settings}
        return_codes.append(execute_swaymsg(display, settings))

    # Exit with the highest return code from swaymsg
    sys.exit(max(return_codes))


def main():
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
        print_help()
        if len(sys.argv) == 0:
            sys.exit(1)
        else:
            sys.exit(0)

    config_file = determine_config_path()
    config = load_json(config_file)

    if '-m' in sys.argv or '--mode' in sys.argv:
        print("Available modes:")
        for mode in config.keys():
            print(f"  - {mode}")
        sys.exit(0)

    mode = sys.argv[1]
    apply_settings(mode, config)


main()
