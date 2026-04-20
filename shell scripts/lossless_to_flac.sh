#!/usr/bin/env bash

###############################################################################
# Audio Library - Lossless Normalization to FLAC
#
# Purpose:
#   Normalize a master lossless audio library by converting all supported
#   lossless formats into FLAC.
#
# Why FLAC?
#   - Lossless compression
#   - Excellent metadata & artwork support
#   - Universally supported
#   - Smaller than WAV/AIFF without quality loss
#
# Behavior:
#   - Processes ALL supported lossless files in INPUT_DIR
#   - Writes FLAC files to OUTPUT_DIR
#   - Preserves all metadata, DOES NOT PRESERVE ARTWORK
#   - Deletes source files ONLY after successful conversion
#
# Supported Input Formats (LOSSLESS ONLY):
#   - WAV  (.wav)
#   - AIFF (.aif / .aiff)
#
# Explicitly Ignored:
#   - MP3, M4A, AAC, etc.
#
# Requirements:
#   - ffmpeg (with FLAC support)
#
# FFMPEG preserves the sample rate and bit depth of the source by default (no resampling or downsampling)
###############################################################################

############################
# Bash Safety Rails
############################

# exit if any command returns a non-zero exit code
#set -o errexit
# treat undefined variables as errors
set -o nounset
# ensure pipeline fails if ANY command fails, not just the last one
set -o pipefail

############################
# User Configuration
############################

INPUT_DIR="/home/psidemica/Lossless Input"
OUTPUT_DIR="/home/psidemica/Lossless FLAC"

FLAC_COMPRESSION_LEVEL=8   # 0-12; 8 is the sweet spot

mkdir -p "$INPUT_DIR" "$OUTPUT_DIR"

############################
# Function: convert_file
#
# Purpose:
#   Convert a single lossless audio file to FLAC.
#
# Arguments:
#   $1  Full path to source audio file
#
# Behavior:
#   - Copies all metadata verbatim
#   - Does NOT touch lossy files
############################
convert_file() {
    local src="$1"
    local filename ext name_no_ext

    filename=$(basename "$src")
    ext="${filename##*.}"
    name_no_ext="${filename%.*}"
    ext="${ext,,}"

    case "$ext" in
        wav|aif|aiff)
            ;;
        *)
            return
            ;;
    esac

    local out_file="$OUTPUT_DIR/${name_no_ext}.flac"

    echo "Converting: $filename"

    ###########################################################################
    # FLAC conversion
    #
    # -map_metadata 0 : preserve all tags
    # -map 0:a        : audio stream
    # -c:a flac       : lossless FLAC encoder
    # -compression_level : size vs CPU tradeoff
    ###########################################################################
    ffmpeg -y -i "$src" \
        -map_metadata 0 \
        -map 0:a \
        -c:a flac \
        -compression_level "$FLAC_COMPRESSION_LEVEL" \
        "$out_file"

    if [[ $? -eq 0 ]]; then
        rm "$src"
        echo "Done"
    else
        echo "Failed: $filename"
    fi
}

############################
# Batch Processing
############################
run_batch() {
    shopt -s nullglob
    for file in "$INPUT_DIR"/*.{wav,WAV,aif,AIF,aiff,AIFF}; do
        convert_file "$file"
    done
    shopt -u nullglob
}

############################
# Entrypoint
############################
run_batch
echo "Lossless library normalized. WAVs and AIFFs have been domesticated."
