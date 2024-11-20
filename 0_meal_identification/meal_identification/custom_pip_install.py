#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os
import shutil
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

def install_packages(package_names):
    """
    Install the specified Python packages using pip.
    """
    print(f"Installing packages: {', '.join(package_names)} via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + package_names)
        print(f"Successfully installed packages: {', '.join(package_names)}.\n")
    except subprocess.CalledProcessError:
        print(f"Error: Failed to install packages: {', '.join(package_names)}. Exiting without modifying environment files.")
        sys.exit(1)

def backup_file(file_path):
    """
    Create a backup of the specified file.
    """
    backup_path = f"{file_path}.bak"
    shutil.copyfile(file_path, backup_path)
    print(f"Backup created: {backup_path}")

def update_yaml_file(file_path, package_names):
    """
    Update the specified YAML file by adding the packages to the pip section.
    If the pip section doesn't exist, it will be created.
    Ensures that the 'name' field remains at the top.
    """
    print(f"Processing '{file_path}'...")

    if not os.path.isfile(file_path):
        print(f"Warning: '{file_path}' not found. Skipping this file.\n")
        return

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    try:
        with open(file_path, 'r') as f:
            data = yaml.load(f) or CommentedMap()

        # Ensure 'dependencies' exists
        if 'dependencies' not in data:
            data['dependencies'] = CommentedSeq()
            print(f"Added 'dependencies' section to '{file_path}'.")

        dependencies = data['dependencies']
        pip_section = None

        # Search for existing pip section
        for item in dependencies:
            if isinstance(item, dict) and 'pip' in item:
                pip_section = item['pip']
                break

        if pip_section is not None:
            added_packages = []
            for pkg in package_names:
                if pkg in pip_section:
                    print(f"'{pkg}' is already present in the pip dependencies of '{file_path}'.")
                else:
                    pip_section.append(pkg)
                    added_packages.append(pkg)
            if added_packages:
                print(f"Added packages to existing pip dependencies in '{file_path}': {', '.join(added_packages)}.")
        else:
            # Add pip section with the packages
            dependencies.append({'pip': list(package_names)})
            print(f"Added new pip section with packages to '{file_path}': {', '.join(package_names)}.")

        # Backup the original file before writing
        # backup_file(file_path)

        # Write back the updated YAML, ensuring 'name' is first
        new_data = CommentedMap()
        if 'name' in data:
            new_data['name'] = data['name']
        for key in data:
            if key != 'name':
                new_data[key] = data[key]

        with open(file_path, 'w') as f:
            yaml.dump(new_data, f)
        print(f"Updated '{file_path}' successfully.\n")

    except Exception as e:
        print(f"Error: An unexpected error occurred while processing '{file_path}'. {e}\n")

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Install Python packages via pip and update environment YAML files."
    )
    parser.add_argument(
        'packages',
        nargs='+',
        help="Names of the Python packages to install."
    )
    parser.add_argument(
        '-f', '--files',
        nargs='*',
        default=['environment.yml', 'environment-ci.yml'],
        help="List of YAML files to update. Defaults to 'environment.yml' and 'environment-ci.yml'."
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    package_names = args.packages
    yaml_files = args.files

    install_packages(package_names)

    for yaml_file in yaml_files:
        update_yaml_file(yaml_file, package_names)

    print(f"Done! Packages installed and aligned in the environment files.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting without modifying environment files.")
        sys.exit(1)
