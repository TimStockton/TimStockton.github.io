#!/usr/bin/env bash

###############################################################################
# Audio Library - Universal to MP3 Backup Converter
#
# Purpose:
#   Convert a batch of audio files into MP3 format for maximum compatibility.
#   Intended for emergency / fallback USBs when FLAC or AIFF are unsupported.
#
# Behavior:
#   - Processes ALL supported files found in INPUT_DIR
#   - Writes MP3 files to OUTPUT_DIR
#   - Preserves all text metadata (artist, title, album, comments, etc.)
#   - Does NOT preserve cover artwork
#   - Does NOT modify filenames beyond extension change
#
# Supported Input Formats:
#   - FLAC (.flac)
#   - WAV (.wav)
#   - AIFF (.aif / .aiff)
#   - MP3 (.mp3)
#   - M4A / AAC (.m4a)
#
# Notes:
#   - Lossy to lossy is unavoidable; this is a compatibility backup
#   - MP3s are encoded using LAME (via ffmpeg)
#
# Requirements:
#   - ffmpeg (with libmp3lame support)
###############################################################################

############################
# Bash Safety Rails
############################

# exit on any command failure
set -o errexit
# treat undefined variables as errors
set -o nounset
# fail pipelines if any command fails
set -o pipefail

############################
# User Configuration
############################

INPUT_DIR="/home/psidemica/MP3 Backup Input"
OUTPUT_DIR="/home/psidemica/MP3 Backup Output"

# MP3 encoding settings
MP3_BITRATE="320k"        # constant bitrate, DJ-safe and universal
MP3_QUALITY=0             # LAME V0-style psychoacoustics (used internally)

mkdir -p "$INPUT_DIR" "$OUTPUT_DIR"

############################
# Function: convert_file
#
# Purpose:
#   Convert a single audio file to MP3 while preserving metadata and artwork.
#
# Arguments:
#   $1  Full path to source audio file
#
# Behavior:
#   - Copies all metadata verbatim
#   - Copies embedded cover art if present
#   - Does not invent or replace artwork
############################
convert_file() {
    local src="$1"
    local filename ext name_no_ext

    filename=$(basename "$src")
    ext="${filename##*.}"
    name_no_ext="${filename%.*}"
    ext="${ext,,}"  # lowercase

    case "$ext" in
        flac|wav|aif|aiff|mp3|m4a)
            ;;
        *)
            return
            ;;
    esac

    local out_file="$OUTPUT_DIR/${name_no_ext}.mp3"

    echo "Converting: $filename"

    ###########################################################################
    # Conversion logic
    #
    # - map_metadata 0 : copy all tags
    # - map 0:a        : audio stream
    # - libmp3lame     : standard MP3 encoder
    ###########################################################################
    ffmpeg -y \
        -i "$src" \
        -map_metadata 0 \
        -map 0:a \
        -c:a libmp3lame \
        -b:a "$MP3_BITRATE" \
        -vn \
        "$out_file"

    echo "Done"
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
echo "All conversions complete. USB apocalypse kit ready."
