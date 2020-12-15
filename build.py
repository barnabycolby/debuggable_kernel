#! /usr/bin/env python3
import argparse
import os
import subprocess
import sys
import tempfile

VM_DIR = 'vm'

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
    os.chdir(VM_DIR)
    os.system("vagrant up")

    # Copy the kernel, assuming that it's already been built.
    kernel_package_path = f"linux-{version}-x86_64.pkg.tar.zst"
    os.system(f"vagrant scp ../{version}/{kernel_package_path} :~")

    # Install the kernel that we just copied.
    os.system(f"vagrant ssh -c 'sudo pacman -U --noconfirm ~/{kernel_package_path} && reboot'")

    os.chdir("..")


# Although we could set the kernel command line parameters using the kernel config, it means that the user will have to rebuild the kernel to change them.
# Instead, we'll modify the grub file, which allows the user to override the command line at boot time using the GRUB bootloader.
def set_debugging_cmdline_parameters():
    # First, get the grub file from the VM. If the command fails, we'll let the exception escape for now.
    os.chdir(VM_DIR)
    destination_path = "/etc/default/grub"
    command = f"vagrant ssh -c 'cat {destination_path}'"
    command_output = subprocess.check_output(command, shell=True)

    # Find the command line that we need to edit.
    line_delimiter = b"\r\n"
    lines = command_output.split(line_delimiter)
    key = b"GRUB_CMDLINE_LINUX_DEFAULT="
    for i, line in enumerate(lines):
        if line.startswith(key):
            index_to_append_at = line.rfind(b'"')
            if index_to_append_at == -1:
                print(f"The {key} line in {destination_path} didn't look like I expected it to. Exiting because I don't yet know how to handle this case.")
                sys.exit(1)

            new_line = line[:index_to_append_at] + b" kgdboc=ttyS0,115200 kgdbwait" + b'"'
            lines[i] = new_line
            break
    else:
        print(f"Failed to find the {key} key in {destination_path}. Exiting because I don't yet know how to handle this case.")
        sys.exit(1)

    # Write the new contents to an actual file to make it easier to use with vagrant.
    source_path = "~/new_grub_file"
    with tempfile.NamedTemporaryFile() as temporary_file:
        new_file_contents = b"\n".join(lines)
        temporary_file.write(new_file_contents)
        temporary_file.flush()

        # Write the file to the remote.
        os.system(f"vagrant scp '{temporary_file.name}' '{source_path}'")

    os.system(f"vagrant ssh -c 'sudo mv {source_path} {destination_path}'")

    # Finally, we need to tell grub to regenerate the actual grub file based on the change we just made.
    os.system(f"vagrant ssh -c 'sudo grub-mkconfig -o /boot/grub/grub.cfg'")

    # At the start of this function, we chdir'd to the VM directory. Reverse that here.
    os.chdir("..")


def main():
    parser = argparse.ArgumentParser(description="Builds an arch package.")
    parser.add_argument("version", help="The version of the kernel that you want to build.")
    args = parser.parse_args()

    version = args.version
    os.symlink(version, "built_version", target_is_directory=True)
    build_kernel(version)
    create_vagrant_vm(version)
    set_debugging_cmdline_parameters()


if __name__ == "__main__":
    main()
