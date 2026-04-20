"""
Program: playlist_map.py [v1.0.0]
Description: Compares a hardcoded source (library) folder to a hardcoded staging (playlist) folder
            - For matching songs:
                - Sets playlist genre to library file only if empty
                - Appends a tag to the library file comment field
Author: Timothy Stockton
Created: 20250901

use cases:
    - Re-organizing a music library
        For example when you want to apply the genre or comment tag of a playlist directory to the original source files.

design notes:
    - Genre and tag values are hardcoded per run
    - GENRE_SWITCH determines whether genre or comment is modified
    - Intended for one-time or limited batch normalization

TO DO:
    - add inline documentation
"""

import os
import sys
import io
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, COMM, ID3NoHeaderError
from mutagen.mp4 import MP4

# Force stdout to UTF-8 so print() won't choke on special characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Register comment so EasyID3 doesn’t throw errors,
# will manage comments through COMM directly
EasyID3.RegisterTextKey("comment", "COMM")

# MP3 comments → UTF-16
# M4A comments → UTF-8
# Rekordbox reads ID3v2.3 tags for MP3s and the ©cmt atom for M4A/MP4 files
# Serato reads ID3v2.3 or v2.4 for MP3, and ©cmt for M4A
# Windows Explorer only reliably reads ID3v2.3 tags, not v2.4
# MediaMonkey can read ID3v2.4 tags


GENRE_SWITCH = False  # True = update genre, False = update comment


def update_mp3(file_path, tag_string, genre_string, genre_mode):
    """Update MP3 tags (ID3). Overwrite COMM frames but preserve content and ensure Explorer visibility."""
    try:
        try:
            audio = EasyID3(file_path)
        except ID3NoHeaderError:
            audio = EasyID3()
            audio.save(file_path)
            audio = EasyID3(file_path)

        if genre_mode:
            current_genre = audio.get("genre", [""])[0].strip()
            print(f"[DEBUG-MP3] {os.path.basename(file_path)} current genre → '{current_genre}'")
            if not current_genre:
                audio["genre"] = [genre_string]
                audio.save(v2_version=3)  # Force ID3v2.3
                return f"Set genre: {genre_string}"
            return f"Genre already set: {current_genre}"

        else:
            id3 = ID3(file_path)

            # Collect all existing comment text, split into tokens
            tokens = []
            for frame in id3.getall("COMM"):
                if frame.text:
                    for t in frame.text:
                        tokens.extend(t.strip().split())

            print(f"[DEBUG-MP3] {os.path.basename(file_path)} old comments tokens → {tokens}")

            # Add the new tag
            tokens.append(tag_string)

            # Deduplicate while preserving order
            seen = set()
            deduped_tokens = []
            for token in tokens:
                if token not in seen:
                    seen.add(token)
                    deduped_tokens.append(token)

            merged_comment = " ".join(deduped_tokens)

            # Overwrite all COMM frames with one clean frame, UTF-16 encoding
            id3.delall("COMM")
            id3.add(COMM(encoding=1, lang="eng", desc="", text=[merged_comment]))  # encoding=1 -> UTF-16
            id3.save(v2_version=3)  # Force ID3v2.3

            return f"Overwrote comments → {merged_comment}"

    except Exception as e:
        return f"Error updating MP3: {e}"


def update_m4a(file_path, tag_string, genre_string, genre_mode):
    """Update M4A tags (MP4 atoms). Overwrite ©cmt but preserve content, deduplicated, Explorer-friendly."""
    try:
        audio = MP4(file_path)

        if genre_mode:
            current_genre = audio.tags.get("\xa9gen", [""])[0].strip() if audio.tags else ""
            print(f"[DEBUG-M4A] {os.path.basename(file_path)} current genre → '{current_genre}'")
            if not current_genre:
                audio.tags["\xa9gen"] = [genre_string]
                audio.save()
                return f"Set genre: {genre_string}"
            return f"Genre already set: {current_genre}"

        else:
            # Collect existing comments, split into tokens
            tokens = []
            if audio.tags and "\xa9cmt" in audio.tags:
                for comment in audio.tags["\xa9cmt"]:
                    tokens.extend(comment.strip().split())

            print(f"[DEBUG-M4A] {os.path.basename(file_path)} old comments tokens → {tokens}")

            # Add the new tag
            tokens.append(tag_string)

            # Deduplicate while preserving order
            seen = set()
            deduped_tokens = []
            for token in tokens:
                if token not in seen:
                    seen.add(token)
                    deduped_tokens.append(token)

            merged_comment = " ".join(deduped_tokens)

            # Overwrite with one clean ©cmt atom
            audio.tags["\xa9cmt"] = [merged_comment]

            # Also remove any extra '----:com.apple.iTunes:iTunNORM' or other comment-like atoms
            for key in list(audio.tags.keys()):
                if key.startswith("----") and "cmt" in key.lower():
                    del audio.tags[key]

            audio.save()
            return f"Overwrote comments → {merged_comment}"

    except Exception as e:
        return f"Error updating M4A: {e}"


def playlist_map(staging_dir, reference_dir, tag_string, genre_string):
    """
    Compare songs in staging_dir against reference_dir (a genre or vibe playlist).
    If filename matches:
        - If genre mode: apply genre if empty.
        - Else: append tag_string to comments.
    Used when initially organizing the music library.
    Example: adding the Dubstep genre to all songs present in the Dubstep genre playlist.
    Example: adding the #drip-lab comment tag to all songs present in that vibe playlist.
    """

    # collect reference files (mp3 + m4a)
    reference_files = {
        f.lower() for f in os.listdir(reference_dir)
        if f.lower().endswith((".mp3", ".m4a"))
    }

    for file_name in os.listdir(staging_dir):
        if not file_name.lower().endswith((".mp3", ".m4a")):
            continue

        if file_name.lower() in reference_files:
            file_path = os.path.join(staging_dir, file_name)

            if file_name.lower().endswith(".mp3"):
                result = update_mp3(file_path, tag_string, genre_string, GENRE_SWITCH)
            else:
                result = update_m4a(file_path, tag_string, genre_string, GENRE_SWITCH)

            print(f"{file_name}: {result}")

# edit the following to use the correct directories, then run via CLI: 'python playlist_map.py'

def setup():
    reference_dir = r"G:/Psidemica/Music/Master Library"
    staging_dir = r"G:/Psidemica/Music/LEGACY ARCHIVE/~~~AMERICAN LEGION SET (KEENE FRIENDLY)/~outro options - end of set and overtime"
    tag_string = "#closer" # examples: #weapon, lounge-of-ascension, #haunted
    genre_string = "Test Genre"

    playlist_map(staging_dir, reference_dir, tag_string, genre_string)

if __name__ == "__main__":
   setup()
