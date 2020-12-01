#! /usr/bin/env python3
import argparse

def build_kernel(version):
    print(f"Building kernel version {version}.")


def main():
    parser = argparse.ArgumentParser(description="Builds an arch package.")
    parser.add_argument("version", help="The version of the kernel that you want to build.")
    args = parser.parse_args()

    build_kernel(args.version)


if __name__ == "__main__":
    main()
