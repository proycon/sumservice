#!/bin/sh

# wrapper for the background service

if [ -d env ]; then
    . env/bin/activate
fi
exec atrium_summarize --server "$@"
