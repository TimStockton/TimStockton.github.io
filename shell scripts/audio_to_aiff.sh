#!/usr/bin/env bash

###############################################################################
# Audio Library - DJ Setlist Converter (Batch Mode)
#
# Purpose:
#   Convert a batch of audio files into a DJ-ready setlist format:
#     - AIFF container
#     - 16-bit PCM
#     - 44,100 Hz sample rate
#
# Why AIFF 16/44.1?
#   - Native CD quality
#   - Maximum compatibility with DJ software & players
#   - Zero surprise resampling artifacts on club systems
#
# Behavior:
#   - Processes ALL supported files found in INPUT_DIR
#   - Writes converted files to OUTPUT_DIR
#   - Deletes source files ONLY after successful conversion
#   - Does NOT preserve cover artwork
#   - Flags lossy sources by appending:
#       __Lossy_Source__
#
# Supported Input Formats:
#   - FLAC (.flac)     [lossless]
#   - WAV (.wav)       [lossless]
#   - AIFF (.aif/.aiff)[lossless]
#   - MP3 (.mp3)       [lossy]
#   - M4A / AAC (.m4a) [lossy]
#
# Important:
#   - Upsampling != quality improvement
#   - This script is for DJ setlists, NOT archival masters
#
# Requirements:
#   - ffmpeg (built with aiff + pcm support)
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

INPUT_DIR="/home/psidemica/DJ Setlist Input"
OUTPUT_DIR="/home/psidemica/DJ Setlist Output"

TARGET_RATE=44100
TARGET_BITS=16

mkdir -p "$INPUT_DIR" "$OUTPUT_DIR"

############################
# Function: convert_file
#
# Purpose:
#   Convert a single audio file to DJ-ready AIFF format.
#
# Arguments:
#   $1  Full path to source audio file
#
# Behavior:
#   - Determines lossy vs lossless based on file extension
#   - Converts audio to 16-bit / 44.1 kHz PCM AIFF
#   - Preserves all text metadata (artist, title, comments, etc.)
#   - Does NOT preserve embedded cover art from source
#
# Lossy sources:
#   - Appends " __Lossy_Source__" to filename
#
# Safety:
#   - Source file is deleted ONLY if ffmpeg succeeds
############################
convert_file() {
    local src="$1"
    local filename ext name_no_ext
    local is_lossy=false

    filename=$(basename "$src")
    ext="${filename##*.}"
    name_no_ext="${filename%.*}"
    ext="${ext,,}"  # lowercase extension

    # NOTE: lossy detection is EXTENSION-BASED BY DESIGN (DJ workflow)
    case "$ext" in
        mp3|m4a)
            is_lossy=true
            ;;
        flac|wav|aif|aiff)
            ;;
        *)
            return
            ;;
    esac

    local suffix=""
    [[ "$is_lossy" == true ]] && suffix=" __Lossy_Source__"

    local out_file="$OUTPUT_DIR/${name_no_ext}${suffix}.aiff"

    echo "Converting: $filename"

    if ffmpeg -y \
        -i "$src" \
        -map_metadata 0 \
        -map 0:a \
        -c:a pcm_s${TARGET_BITS}be \
        -ar "$TARGET_RATE" \
        "$out_file"
    then
        if [[ -s "$out_file" ]]; then
            rm -- "$src"
            echo "Done"
        else
            echo "Output missing or empty: $out_file" >&2
        fi
    else
        echo "Failed: $filename" >&2
    fi

}

############################
# Batch Processing
############################
run_batch() {
    shopt -s nullglob
    for file in "$INPUT_DIR"/*.{flac,FLAC,wav,WAV,aif,AIF,aiff,AIFF,mp3,MP3,m4a,M4A}; do
        convert_file "$file"
    done
    shopt -u nullglob
}

############################
# Entrypoint
############################
run_batch
echo "All conversions complete. Go melt faces."
