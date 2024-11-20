#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import yaml
import shutil

def install_package(package_name):
    """
    Install the specified Python package using pip.
    """
    print(f"Installing '{package_name}' via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed '{package_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install '{package_name}'. Exiting without modifying environment files.")
        sys.exit(1)

def backup_file(file_path):
    """
    Create a backup of the specified file.
    """
    backup_path = f"{file_path}.bak"
    shutil.copyfile(file_path, backup_path)
    print(f"Backup created: {backup_path}")

def update_yaml_file(file_path, package_name):
    """
    Update the specified YAML file by adding the package to the pip section.
    If the pip section doesn't exist, it will be created.
    """
    print(f"Processing '{file_path}'...")
    
    if not os.path.isfile(file_path):
        print(f"Warning: '{file_path}' not found. Skipping this file.")
        return

    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f) or {}

        dependencies = data.get('dependencies', [])
        pip_dependencies = None

        # Search for existing pip section
        for dep in dependencies:
            if isinstance(dep, dict) and 'pip' in dep:
                pip_dependencies = dep['pip']
                break

        if pip_dependencies is not None:
            if package_name in pip_dependencies:
                print(f"'{package_name}' is already present in the pip dependencies of '{file_path}'.")
            else:
                pip_dependencies.append(package_name)
                print(f"Added '{package_name}' to existing pip dependencies in '{file_path}'.")
        else:
            # Add pip section with the package
            dependencies.append({'pip': [package_name]})
            print(f"Added new pip section with '{package_name}' to '{file_path}'.")

        data['dependencies'] = dependencies

        # Backup the original file before writing
        backup_file(file_path)

        # Write back the updated YAML
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        print(f"Updated '{file_path}' successfully.\n")

    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file '{file_path}'. {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred while processing '{file_path}'. {e}")

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Install a Python package via pip and update environment YAML files.")
    parser.add_argument('package', help="Name of the Python package to install.")
    parser.add_argument('-f', '--files', nargs='*', default=['environment.yml', 'environment-ci.yml'],
                        help="List of YAML files to update. Defaults to 'environment.yml' and 'environment-ci.yml'.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    package_name = args.package
    yaml_files = args.files

    install_package(package_name)

    for yaml_file in yaml_files:
        update_yaml_file(yaml_file, package_name)

    print(f"Done! '{package_name}' installed and aligned in the environment files.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting without modifying environment files.")
        sys.exit(1)
