#!/bin/sh

export CUDA_VISIBLE_DEVICES=0

STATUS_FILE=$1
shift
INPUT_DIR=$1
shift
OUTPUT_DIR=$1
shift

if [ -z "$STATUS_FILE" ] || [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "One or more positional arguments are missing">&2
    exit 1
fi
if [ -z "$HF_TOKEN" ]; then
    echo "HF_TOKEN not set">&2
    exit 1
fi

WORDS=500
while getopts "l:w:p:" arg; do
    case $arg in
        l)
            if [ "$OPTARG" != "auto" ]; then
                EXTRA_ARG=--force-language $OPTARG
            fi
            ;;
        w)
            WORDS=$OPTARG
            ;;
        *)
            echo "Invalid option">&2
            exit 1
            ;;
    esac
done

echo "Starting..." > "$STATUS_FILE"
INPUT_FILE=$(ls "$INPUT_DIR" | head -n 1)

if summarize-interviews \
    --model-name deepseek-ai/DeepSeek-R1-Distill-Llama-8B \
    --srt-file "$INPUT_DIR/$INPUT_FILE" \
    --summary-words "$WORDS" \
    --intro-prompt "$INTRO_PROMPT" \
    --use-gpu yes \
    --device-id 0 \
    --cache-dir "$CACHE_DIR" \
    --output-dir "$OUTPUT_DIR" \
    --hf-token "$HF_TOKEN" $EXTRA_ARG; then
    echo "Done." > "$STATUS_FILE"
    exit 0
else
    echo "Failed." > "$STATUS_FILE"
    exit 1
fi
