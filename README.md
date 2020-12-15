# Debuggable kernel
- Uses the arch package system to make building debuggable kernels easy.
- Each supported kernel version is downloaded into a directory named after the version.
- It contains a `PKGBUILD`, kernel configuration and patch files.
- Building the kernel this way means that we get an arch package that can be installed onto an arch system, resulting in a normal linux system that is configured in a sensible way, can connect to the internet and download packages as normal.

## ToDo's
- Support building a debuggable kernel.
- Support custom user patches.
- Polish this readme.

## Dependencies
- Vagrant
- Arch linux
- Build tools
