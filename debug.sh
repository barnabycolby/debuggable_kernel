#! /bin/sh
set -e
socat -d -d /tmp/kernel_debugging pty,link=/tmp/kernel_pty &
gdb built_version/src/archlinux-linux/vmlinux -x gdbinit
