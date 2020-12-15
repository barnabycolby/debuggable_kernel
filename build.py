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

    # Change to the directory and start the build process.
    # Use os.system because it's soooo much simpler than subprocess and we don't need any
    # more power.
    print(f"Building kernel version {version}.")
    os.chdir(version_directory)
    os.system("makepkg -srf")
    os.chdir("..")


def create_vagrant_vm(version):
    # Start the VM.
    os.chdir("vm")
    os.system("vagrant up")

    # Copy the kernel, assuming that it's already been built.
    kernel_package_path = f"linux-{version}-x86_64.pkg.tar.zst"
    os.system(f"vagrant scp ../{version}/{kernel_package_path} :~")

    # Install the kernel that we just copied.
    os.system(f"vagrant ssh -c 'sudo pacman -U --noconfirm ~/{kernel_package_path} && reboot'")

    os.chdir("..")


def main():
    parser = argparse.ArgumentParser(description="Builds an arch package.")
    parser.add_argument("version", help="The version of the kernel that you want to build.")
    args = parser.parse_args()

    version = args.version
    build_kernel(version)
    create_vagrant_vm(version)


if __name__ == "__main__":
    main()
