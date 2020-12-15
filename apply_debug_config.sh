#! /bin/sh

# Exit immediately on error.
set -e

VERSION="${1}"
if [ -z "${VERSION}" ]; then
    echo 'You need to supply the version number as the first argument. This should match up exactly to the name of a directory in the root of this project.'
    exit 1
fi

if [ ! -d "${VERSION}" ]; then
    echo "${VERSION} is not the name of a directory."
    exit 1
fi

function configure {
    ./config_editor --file "${VERSION}/config" $@
}

configure --enable GDB_SCRIPTS
configure --enable KGDB
configure --enable KGDB_SERIAL_CONSOLE

echo "Successfully configured ${VERSION}/config."
