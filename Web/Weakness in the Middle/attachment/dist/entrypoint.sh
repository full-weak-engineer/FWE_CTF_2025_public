#!/bin/sh
exec su -s /bin/sh -c 'exec "$0" "$@"' app -- "$@"