#!/bin/sh

# Entrypoint for the docker container, generates the configuration on-the-fly from the template and runtime environment variables

# shellcheck disable=SC2086
GLOBAL_ENV=1 make clean sumservice.toml && exec clam --config sumservice.toml $CLAM_EXTRA
