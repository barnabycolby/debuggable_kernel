#! /usr/bin/env python3
import argparse
import os

def build_kernel(version):
    # First, check that we have the arch package for the specified version.
    script_directory = os.path.dirname(os.path.realpath(__file__))
    version_directory = os.path.join(script_directory, version)
    if not os.path.isdir(version_directory):
        print(f"Kernel version {version} is not supported.")
        return

    print(f"Building kernel version {version}.")


def main():
    parser = argparse.ArgumentParser(description="Builds an arch package.")
    parser.add_argument("version", help="The version of the kernel that you want to build.")
    args = parser.parse_args()

    build_kernel(args.version)


if __name__ == "__main__":
    main()
