# Debuggable kernel
- Uses the arch package system to make building debuggable kernels easy.
- Each supported kernel version is downloaded into a directory named after the version.
- It contains a `PKGBUILD`, kernel configuration and patch files.
- Building the kernel this way means that we get an arch package that can be installed onto an arch system, resulting in a normal linux system that is configured in a sensible way, can connect to the internet and download packages as normal.
- Arch kernel configs appear to have debugging info enabled already.
- The kernel config has been modified to support KGDB over serial.
- After starting the vagrant VM, the build script sets the grub command line parameters to enable debugging over the serial port and wait for a debugger to connect before continuing the boot.
- The `Vagrantfile` also sets up the serial port to point to a pipe file on the host.
- The debug script uses `socat` to turn the pipe file into a PTY and then attaches GDB.
- The state of this repo so far is very very minimal. Lots more work could be done to make this much smoother and allow a greater level of usability by others.

## ToDo's
- Support a command line switch that toggles whether the kernel should/shouldn't wait for a debugger to attach. Or, writeup how to do this manually.
- Support custom user patches.
- Polish this readme.

## Dependencies
- Vagrant
- Arch linux
- Build tools
