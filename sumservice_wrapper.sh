#!/bin/sh

outputdir=$(realpath .)
maxwords=500
maxchunkwords=250
language=auto
port=11001

while getopts "L:W:p:" opt; do
    case $opt in
        L) language=$OPTARG ;;
        W) maxwords=$OPTARG ;;
        p) maxwords=$OPTARG ;;
        :) printf 'Option -%s requires an argument\n' "$OPTARG" >&2;
           exit 2 ;;
        *) printf 'Invalid option %s' "$OPT" >&2; exit 2 ;;
    esac
done
shift "$((OPTIND - 1))"

if [ -z "$port" ]; then
    echo "ERROR: Missing port">&2
fi
if [ -z "$outputdir" ]  || [ ! -d "$outputdir" ]; then
    echo "ERROR: Outputdir not provided or does not exist">&2
    exit 2
fi

if [ $# -eq 0 ]; then
    echo "ERROR: No input files provided...">&2
    exit 2
fi

for f in "$@"; do
    f="$(realpath "$f")"
    printf "%s\t%s\t%s\t%s\t%s\n"  "$f" "$outputdir" "$language" "$maxwords" "$maxchunkwords" | nc localhost "$port" >&2
done

echo "Done...">&2
