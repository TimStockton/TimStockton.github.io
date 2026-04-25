"""
Program: music_library_manager.py [v1.0.0]
Description: Manages metadata changes (individual or bulk), playlist generation, filtering.
Author: Timothy Stockton
Created: 20250810

core features:
    - Read and update metadata
    - Filter tracks by:
        - Genre
        - BPM
        - Camelot key
        - Custom comment tags
    - Batch tag updates
    - Genre playlist generation
    - Crate playlist generation
    - Duplicate detection
    - Missing metadata scans

designed around:
    - Dual libraries (lossy + lossless)
    - Genre-based playlists
    - Crate-based playlists using structured comment tags
    - Safe, repeatable exports

Supported formats:
    - .mp3
    - .m4a
    - .flac

Playlist behavior (important):
    - Multi-genre tracks are copied once per genre
        - This is intentional
        - Playlists are organizational views, not canonical storage
    - Duplicate prevention
        - Existing files are skipped
        - Re-running the script is safe

Crate system:
    Crates are driven by predefined, allowed values stored in the track's comment field.

Crate tags:
    - Do not use prefixes
    - Must exactly match one of the allowed crate names
    - Are grouped into logical categories
    Tracks containing one or more valid crate tags in the comment field will be exported into the corresponding crate playlists.
    Tracks without valid crate tags are ignored during crate exports.

Dependencies:
    First-time use will likely require:
    ```pip install mutagen```

Typical workflow (DJ use case):
    1. Download new tracks
    2. Place them in a staging folder
    3. Analyze tracks in Mixed In Key
        - BPM
        - Camelot key
        - Energy
    4. Run tagging script to standardize metadata
    5. Scan for missing or invalid tags
    6. Deduplicate against master libraries
    7. Move tracks into:
        - Lossy library or
        - Lossless library
    8. Generate playlists (genres and/or crates)
    9. Export playlists to:
        - Phone (reference)
        - Rekordbox
    10. Analyze waveforms / beatgrids
    11. Add hot cues
    12. Export to USB for performance

TO DO:
    - Add a basic user interface (phase 2)
    - Package as platform independant .exe (phase 3)
"""

import os
import sys
import shutil
import re
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from pathlib import Path

# testing without actually copying files
# does not impact metadata changes
DRY_RUN = False

# accepted file formats
SUPPORTED_AUDIO = (".mp3", ".m4a", ".flac")

# standard audio file metadata tags
TAG_TITLE = "title"
TAG_RATING = "rating"
TAG_COMMENT = "comment"
TAG_ARTIST = "artist"
TAG_ALBUM_ARTIST = "albumartist"
TAG_ALBUM = "album"
TAG_YEAR = "date"
TAG_NUMBER = "#"
TAG_GENRE = "genre"
TAG_LENGTH = "length"
TAG_MOOD = "mood"
TAG_KEY = "initialkey"
TAG_BPM = "bpm"

# the comments tag field will be used to store custom tags and mixedinkey camelot wheel key
# this field is automatically displayed in DJ software like rekordbox and serato
# DJ software does not overwrite the comment field, mixedinkey can but can be set not to
# lossy mp3 files that are officially sourced will be marked as such
# the structure of the comment tag will be as follows (all optional, bpm and key highly encouraged):
# song-bpm camelot-key #official #core-tag #sub-tag #sub-tag #utility-tag

# Phase 1 → Python CLI
# Use mutagen to load and modify tags.
# Build functions for sorting, filtering, and copying files to playlist folders.

# Phase 2 → Add a simple GUI
# Start with Tkinter or PyQt for drag-and-drop and filter selection.

# Phase 3 → Package
# Use PyInstaller to make a single .exe or .app so you can run it without Python installed.

# may need to create "pages" to support large numbers of songs
# in the future, could use playlist .m3u files instead of physical .xxx copies, rekordbox supports .m3u (how?)

# mutagen handles reading/writing ID3 tags: ID3 (MP3) Vorbis comments (FLAC) MP4 atoms (M4A)
# filters and sorting use Python’s built-in list/dict tools
# os, shutil, and pathlib handle moving/copying without worrying about platform-specific quirks
# UI is achievable without rewriting, options include: 
#       Tkinter (built-in, easy, checkboxes for filters, folder selection dialogs), 
#       PyQt / PySide (more modern, better for polished cross-platform apps), 
#       Kivy (good for cross-platform apps), 
#       CustomTkinter (modernized Tkinter)
# PyInstaller or py2exe can package this script into a .exe

# Add functionality for a recomendation of path options based on the current song.
# Heavier -> #heavy #closebpm #similar key
# Weirder -> #weird #bpm #key #psychedelic
# Faster -> #higherbpm #samekey
# Slower -> #lowerbpm #samekey
# Like a tree you can click the branches on. Gives up to 3 song options when a path branch is selected.
# This can be used to build setlists (and possibly integrated into live DJing in the future).

# For filtering, want a way to select 1-5 crate tags and have all matches displayed in one list sorted by bpm and key

# In the future, can automate lossy to lossless
# FLAC files placed in staging folder, script locates matching mp3 file in lossy library (if present)
# then script copies existing metadata from MP3 to FLAC and deletes the MP3, placing FLAC in lossless library

# In the future, consider scenarios where only WAV is available for purchase, not FLAC

# future abstraction of tracks
# @dataclass
# class Track:
#     path: Path
#     tags: dict

# future logging instead of printing
# import logging
# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger(__name__)

# in the future can cache once per run and pass around objects instead of reading every file and tag every time
# less of a concern now, more of a concern when the library total passes 10k song files

# in the future, can filter by tag so that you can change the spelling of a tag (and other edits to the whole tag group)

# TODO: add a way to exit filtering by tag after desired edits have been made (besides ctrl+c)
# TODO: add a way to go through the batch files one by one, not just bulk edit with same values (unless desired, minimal use cases)

# TODO: include only 'dream pop' and not dreampop', convert dreampop (same for Hip-Hop)

# used when creating 'playlist' folders by genre
GENRE_GROUPS = {
    "Bass House": ["Bass House", "Deep House"],
    "Bounce": ["Bounce"],
    "Chillstep": ["Chillstep", "Melodic Dubstep"],
    "Cinematic": ["Classical", "Soundtrack", "Orchestral"],
    "Comedy": ["Comedy", "Comedy Rock"],
    "Country": ["Country"],
    "Dance": ["House", "French House", "Progressive House", "Tech House", "Dance", "Eurodance", "Tropical House", "Acid House", "Latin", "Hip House", "Salsa", "French House", "Stutter House", "Speed House"],
    "Downtempo": ["Downtempo", "Indie Electronic", "Dreampop", "Dream Pop", "Ambient", "Chillout"],
    "Drum & Bass": ["Drum & Bass", "Breaks", "Liquid Funk"],
    "Drumstep": ["Drumstep", "Electronica"],
    "Dubstep": ["Dubstep", "Deep Dubstep", "Brostep", "Reggaestep", "UK Dubstep"],
    "Electro Swing": ["Electro Swing"],
    "Experimental Bass": ["Experimental Bass"],
    "Funky": ["Funk", "Nu Disco", "Disco House", "Disco", "Funky House", "Disco-Funk", "Future Funk"],
    "Future": ["Future Bass", "Future House", "Future Rave"],
    "Garage": ["Garage", "UK Garage", "Future Garage"],
    "Glitch Hop": ["Glitch Hop"],
    "Hard Dance": ["Hardcore", "Happy Hardcore", "Techno", "Hard Techno", "Melodic Techno", "Hard Dance", "Hardstyle", "UK Hardcore"],
    "LoFi": ["LoFi", "Chillhop", "Beatbox"],
    "Lounge": ["Swing", "Jazz", "Blues", "Easy Listening", "Bluegrass"],
    "Mainstage": ["Mainstage", "Electro House", "Big Room", "Big Room House"],
    "Metal": ["Metal", "Death Metal", "Black Metal", "Nu Metal", "Speed Metal", "Post-Hardcore", "Progressive Metal", "Pirate Metal", "Viking Metal", "Thrash Metal", "Metalcore", "Alternative Metal", "Heavy Metal", "Melodic Death Metal", "Groove Metal", "Funk Metal", "Gothic Metal", "Industrial Metal", "Power Metal", "Christian Metal", "Symphonic Metal", "Post Hardcore", "Doom Metal"],
    "Midtempo": ["Midtempo", "Synthwave"],
    "Moombah": ["Moombahcore", "Moombahton"],
    "Other": ["Other", "Fanfare"],
    "Pop": ["Pop", "World", "Bubblegum Dance", "K-Pop", "Synthpop", "Dance-Pop", "Ukulele", "Electropop", "Art Pop", "Power Pop", "Pop Rock", "Pop Rap", "A Cappella", "New Wave"],
    "Rap": ["Hip Hop/Rap", "Rap", "Rapstep", "Alternative Hip Hop", "R&B", "Snap", "Reggaeton/Hip-Hop", "Gangsta Rap", "West Coast Hip Hop", "Hip Hop", "Hip-Hop", "Rap Metal", "Southern Hip Hop", "Comedy Hip Hop", "Country Rap", "Japanese Hip Hop"],
    "Reggae": ["Reggae", "Reggae Fusion"],
    "Riddim": ["Riddim", "Tearout", "Breakout", "Deathstep", "Briddim", "Metalstep", "Vomitstep"],
    "Soul": ["Soul", "Soul Blues", "R&B/Soul"],
    "Rock": ["Rock", "Alternative Rock", "Classic Rock", "Punk Rock", "Rockabilly", "Rock and Roll", "Pop Punk", "Hard Rock", "Post-Grunge", "Soft Rock", "Folk Rock", "Alternative", "Heartland Rock", "Celtic Punk", "Electronic Rock", "Acoustic Punk", "Southern Rock", "Psychedelic Rock", "Progressive Rock", "Funk Rock", "Indie Rock"],
    "Trance": ["Trance", "Psy Trance", "Psy-Trance", "Jamtronica", "Melodic Trance"],
    "Trap": ["Trap", "Trap & Bass", "Phonk", "Hybrid Trap", "Tribal Trap", "UK Bass"]
}


# used when creating 'playlist' folders by tag
CRATE_GROUPS = {
    "Core": [
        "warrior-combat-gym", "turbo-race-track", "subterranean-drip-lab",
        "open-format-club", "lounge-of-ascension", "bar-of-melancholy"
    ],
    "Sub": [
        "alien", "bars", "frozen", "guitar", "haunted", "meta", "weird", "bouncy", "wobble",
        "organic", "smoke", "magic", "summer", "talkbot", "science", "funky", "deep"
    ],
    "Utility": [
        "anthem", "weapon", "sample", "tool", "mashup", "mixlet", "hype",
        "opener", "closer", "psidemica", "mix", "other", "pandemica"
    ]
}
# GROUP DESCRIPTIONS:
# --
# warrior-combat-gym:       angry, headbang, fight
# turbo-race-track:         fast, energetic, chase
# subterranean-drip-lab:    wonky, dark, wobble
# open-format-club:         dance, party, hype
# lounge-of-ascension:      light, funky, groovy
# bar-of-melancholy:        gloom, sad, reflection
# --
# alien:                    extraterrestrial, space
# bars:                     spitting fire, rap lyrics
# frozen:                   winter, cold, christmas
# guitar:                   shredding, solos
# haunted:                  spooky, dark, halloween
# meta:                     pop culture, memes, 4th wall
# weird:                    trippy and psychedelic, odd, wonky
# bouncy:                   off-kilter, energetic, hoppin
# wobble:                   oscillating, pulsating, wub
# organic:                  piano, strings, woodwinds, classical
# smoke:                    puff puff pass, chill
# magic:                    spellcaster, shaman, wizard
# summer:                   sun, beach, warm
# talkbot:                  vocal synth, vocal bass
# science:                  tech, lab, munitions
# funky:                    groovy and psychedelic, flowy
# deep:                     low, donk, rumble
# --
# anthem:                   rally, iconic
# weapon:                   surprise, devastate
# sample:                   soundboard
# tool:                     DJ helpers
# mashup:                   combo, double
# mixlet:                   multiple combos/doubles
# hype:                     gets the people GOING
# opener:                   great first tracks
# closer:                   great final tracks
# psidemica:                my originals and remixes
# mix:                      my mixes
# other:                    IDK but keep it separated
# pandemica:                alter ego originals and remixes
# --

# called by read_audio_tags()
# Mutagen returns inconsistent tag shapes across formats (MP3/M4A/FLAC).
# This function normalizes all tag values into lowercase keys with list[str] values.
def normalize_tags(tags):
    normalized = {}
    for k, vals in tags.items():
        if isinstance(vals, list):
            normalized[k.lower()] = [str(v).strip() for v in vals]
        else:
            normalized[k.lower()] = [str(vals).strip()]
    return normalized


# called by build_genre_playlists()
def normalize_genre(g):
    return re.sub(r"\s+", " ", g.lower().strip())

    
# called by filter_songs(), build_genre_playlists(), and build_crate_playlists()
def read_audio_tags(file_path):
    """
    Read audio tags (MP3, M4A, or FLAC) and return as a dictionary.
    """
    try:
        # easy=True ensures consistent, human-readable tag names across formats
        audio = File(file_path, easy=True)

        # If mutagen can't parse the file, return empty tags
        if audio is None:
            return {}

        tags = normalize_tags(audio.tags or {})

        # inject comment consistently
        comment = get_comment_raw(file_path)
        if comment:
            tags["comment"] = [comment]

        return tags

    except Exception as e:
        print(f"Error reading tags for {file_path}: {e}")
        return {}


# called by bulk_edit_tags()
def edit_audio_tags(file_path, edits):
    """
    Edit MP3, M4A, and FLAC metadata tags.
    Supports comment replacement for all formats.
    edits: dict of {tag_name: new_value}
    """
    suffix = file_path.lower()

    try:
        if suffix.endswith(".mp3"):
            from mutagen.id3 import ID3, COMM, ID3NoHeaderError, TIT2, TPE1, TALB, TDRC, TCON

            try:
                audio = ID3(file_path)
            except ID3NoHeaderError:
                audio = ID3()

            for key, value in edits.items():
                if key == TAG_COMMENT:
                    audio.delall("COMM")
                    audio.add(COMM(encoding=3, lang="eng", desc=value, text=value))
                elif key == TAG_TITLE:
                    audio.delall("TIT2")
                    audio.add(TIT2(encoding=3, text=value))
                elif key == TAG_ARTIST:
                    audio.delall("TPE1")
                    audio.add(TPE1(encoding=3, text=value))
                elif key == TAG_ALBUM:
                    audio.delall("TALB")
                    audio.add(TALB(encoding=3, text=value))
                elif key == TAG_YEAR:
                    audio.delall("TDRC")
                    audio.add(TDRC(encoding=3, text=value))
                elif key == TAG_GENRE:
                    audio.delall("TCON")
                    audio.add(TCON(encoding=3, text=value))
                else:
                    # fallback: add as TXXX frame
                    from mutagen.id3 import TXXX
                    audio.add(TXXX(encoding=3, desc=key, text=value))
            audio.save(file_path)

        elif suffix.endswith(".m4a"):
            from mutagen.mp4 import MP4
            audio = MP4(file_path)
            for key, value in edits.items():
                if key == TAG_COMMENT:
                    audio["©cmt"] = [value]
                else:
                    audio[key] = [value]
            audio.save()

        elif suffix.endswith(".flac"):
            from mutagen.flac import FLAC
            audio = FLAC(file_path)
            for key, value in edits.items():
                if key == TAG_COMMENT:
                    audio["comment"] = [value]
                else:
                    audio[key] = [value]
            audio.save()

        print(f"Updated tags for: {os.path.basename(file_path)}")

    except Exception as e:
        print(f"Error updating {file_path}: {e}")

    # old logic:

    # # grab song file
    # audio = File(file_path, easy=True)
    # if not audio:
    #     return
    
    # # update the tags
    # for key, value in edits.items():
    #     audio[key] = [value]

    # # save tag changes
    # audio.save()
    # # display success and info to user
    # print(f"Updated tags for: {os.path.basename(file_path)}")


# called by run_editor()
def filter_songs(folder, filter_key=None, filter_value=None):
    """
    Scan folder for MP3/M4A and return files matching the filter.
    filter_key: 'artist', 'album', 'genre', 'date', etc.
    filter_value: text to match (case-insensitive, partial match allowed).
    """
    matching_files = []
    checked = 0

    # Guard against unsupported or mistyped tag names to avoid silent zero-match scans
    if filter_key and filter_key.lower() not in {
        TAG_ARTIST, TAG_ALBUM, TAG_GENRE, TAG_YEAR, TAG_COMMENT
    } and filter_key != "filename":
        print(f"Unknown tag: {filter_key}")
        return []

    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(SUPPORTED_AUDIO):
                file_path = os.path.join(root, f)

                # heartbeat every 250 files
                checked += 1
                if checked % 250 == 0:
                    print(f" Scanned {checked} files...", flush=True)

                tags = read_audio_tags(file_path)

                if not filter_key:  # no filter means match all
                    matching_files.append((file_path, tags))

                elif filter_key == "filename":
                    if filter_value.lower() in f.lower():
                        matching_files.append((file_path, tags))

                else:
                    raw = tags.get(filter_key.lower(), [])
                    value = " ".join(raw).lower() if isinstance(raw, list) else str(raw).lower()
                    if filter_value and filter_value.lower() in value:
                        matching_files.append((file_path, tags))
    return matching_files


# called by run_editor()
def copy_to_playlist(files_with_tags, output_folder):
    """
    Copy matching MP3 files to output folder (playlist).
    """
    os.makedirs(output_folder, exist_ok=True)

    for file_path, _ in files_with_tags:
        dest_path = os.path.join(output_folder, os.path.basename(file_path))
        if DRY_RUN:
            print(f"[DRY RUN] Would copy {file_path} to {dest_path}")
        else:
            shutil.copy2(file_path, dest_path)
            print(f"Copied: {os.path.basename(file_path)}")


# called by run_editor()
def bulk_edit_tags(files_with_tags):
    """
    Prompt user to edit tags for all matching files (applies same values to all).
    Fully supports comment updates.
    """
    print("\nEnter new tag values (leave blank to skip):")
    new_title = input("New title: ").strip()
    new_artist = input("New artist: ").strip()
    new_album = input("New album: ").strip()
    new_genre = input("New genre: ").strip()
    new_year = input("New year: ").strip()
    new_comment = input("New comment (will replace existing comment for ALL matches): ").strip()

    # TODO: display the files to be edited (if not bulk editing) so you know what you are changing...

    edits = {}
    if new_title: edits[TAG_TITLE] = new_title
    if new_artist: edits[TAG_ARTIST] = new_artist
    if new_album: edits[TAG_ALBUM] = new_album
    if new_genre: edits[TAG_GENRE] = new_genre
    if new_year: edits[TAG_YEAR] = new_year
    if new_comment: edits[TAG_COMMENT] = new_comment

    if not edits:
        print("No edits made.")
        return
    
    # confirmation
    print("\nThe following edits will be applied to all matching files:")
    for k, v in edits.items():
        print(f"  {k}: {v}")
    confirm = input("Apply changes to ALL files? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborting edits.")
        return
    
    # update tags
    for file_path, _ in files_with_tags:
        edit_audio_tags(file_path, edits)
    print(f"\nSuccessfully updated {len(files_with_tags)} files.")


# called by menu()
# Songs may belong to multiple genre groups.
# Each matching genre results in a separate copy (non-exclusive classification).
# if two genres, will only copy to unknown folder if both genres are unknown
def build_genre_playlists(source_folder):
    """
    Scan source folder for MP3/M4A files and copy them into genre-based playlist folders.
    Uses exact genre matching only. Files that don't match go into 'Unsorted'.
    """
    base_folder = os.path.dirname(source_folder.rstrip("/\\"))
    playlist_root = os.path.join(base_folder, "Playlists - Genre")
    os.makedirs(playlist_root, exist_ok=True)

    unsorted_folder = os.path.join(playlist_root, "Unsorted")
    os.makedirs(unsorted_folder, exist_ok=True)
    
    print(f"\nBase Folder: {base_folder}")
    print(f"\nPlaylist Root: {playlist_root}")
    print(f"\nBegin copying song files into genre folders...")

    processed = 0
    for root, _, files in os.walk(source_folder):
        for f in files:
            if f.lower().endswith(SUPPORTED_AUDIO):
                processed += 1
                if processed % 250 == 0:
                    print(f" Processed {processed} files...", flush=True)

                file_path = os.path.join(root, f)
                tags = read_audio_tags(file_path)
                genre_vals = tags.get("genre", [])
                genre = ",".join(genre_vals).lower()

                matched = False
                for group, genre_list in GENRE_GROUPS.items():
                    # fuzzy match genre to avoid sending close matches to unsorted
                    # handles scenarios like 'House/Tech House' and 'Bass House, Deep House'
                    genre_tokens = {
                        normalize_genre(g)
                        for chunk in genre.split(",")
                        for g in chunk.split("/")
                    }
                    genre_list_norm = {normalize_genre(g) for g in genre_list}
                    if genre_tokens & genre_list_norm:
                        output_folder = os.path.join(playlist_root, group)
                        os.makedirs(output_folder, exist_ok=True)
                        dest_path = os.path.join(output_folder, os.path.basename(file_path))

                        # Skip if a file with the same name already exists in this genre folder.
                        # This prevents lossy/lossless collisions without renaming files.
                        if os.path.exists(dest_path):
                            print(f"Skipped duplicate: {dest_path}")
                            continue

                        if DRY_RUN:
                            print(f"[DRY RUN] Would copy {file_path} to {dest_path}")
                            matched = True
                        else:
                            shutil.copy2(file_path, dest_path)
                            print(f"Copied {f} to {group}")
                            matched = True

                if not matched:
                    unsorted_path = os.path.join(unsorted_folder, os.path.basename(file_path))
                    if DRY_RUN:
                        print(f"[DRY RUN] Would copy {file_path} to {unsorted_path}")
                    else:
                        shutil.copy2(file_path, unsorted_path)
                        print(f"Copied {f} to Unsorted")

    print(f"\nFinished! Processed {processed} songs.")
    return


# called by build_crate_playlists()
def extract_comment_tags(comment: str) -> set[str]:
    """
    Extract #tags from the comment field, ignoring Camelot key.
    """
    if not comment:
        return set()

    key_pattern = re.compile(r"\b0?\d{1,2}[AB]\b", re.I)

    tags = set()
    for token in re.split(r"[,\s]+", re.sub(r"[^\w#-]", " ", comment.lower())):
        # Ignore Camelot key (like 7A or 12B)
        if key_pattern.match(token):
            continue

        # Ignore dash separators (added between key and BPM by Mixed In Key
        if token == "-":
            continue

        # Ignore numeric BPM values to prevent accidental hashtag extraction
        if token.isdigit() and 60 <= int(token) <= 220:
            continue

        # Keep tags, strip '#'
        # tags are manually added, or added via this script with a space in-between
        if token.startswith("#"):
            tags.add(token[1:].lower())

    return tags


# called by build_create_playlists()
# EasyID3 uses "comment", MP4 (M4A) uses "©cmt", FLAC uses "comment" but sometimes returns lists differently
def get_comment_raw(file_path: str) -> str:
    suffix = file_path.lower()

    try:
        # MP3 - ID3 COMM frames
        if suffix.endswith(".mp3"):
            audio = ID3(file_path)
            comments = []
            for key, frame in audio.items():
                if key.startswith("COMM"):
                    comments.extend(frame.text)
            return " ".join(comments)

        # M4A - MP4 atom ©cmt
        elif suffix.endswith(".m4a"):
            audio = MP4(file_path)
            return " ".join(audio.tags.get("©cmt", []))

        # FLAC - Vorbis comments (case-insensitive, multi-key)
        elif suffix.endswith(".flac"):
            audio = FLAC(file_path)

            comments = []
            for k, v in audio.tags.items():
                if k.lower() in ("comment", "comments", "description"):
                    if isinstance(v, list):
                        comments.extend(v)
                    else:
                        comments.append(str(v))

            return " ".join(comments)

    except Exception as e:
        print(f"Comment read error: {file_path}: {e}")

    return ""


# called by menu()
def build_crate_playlists(source_folder):
    """
    Copy audio files into comment tag folders. 
    Only put into Unsorted if tags exist but none match CRATE_GROUPS.
    """

    base_folder = os.path.dirname(source_folder.rstrip("/\\"))
    playlist_root = os.path.join(base_folder, "Playlists - Crate")
    os.makedirs(playlist_root, exist_ok=True)

    unsorted_folder = os.path.join(playlist_root, "Unsorted")
    os.makedirs(unsorted_folder, exist_ok=True)

    print(f"Structure setup complete, begin copying song files into crate folders...")

    processed = 0

    for root, _, files in os.walk(source_folder):
        for f in files:
            if not f.lower().endswith(SUPPORTED_AUDIO):
                continue

            processed += 1
            if processed % 100 == 0:
                print(f"Processed {processed} files...", flush=True)

            file_path = os.path.join(root, f)
            comment = get_comment_raw(file_path)
            crate_tags = extract_comment_tags(comment)

            # Files without any hashtag-based crate tags are ignored entirely
            # (they are not placed into Unsorted)
            if not crate_tags:
                continue

            matched = False
            for group, crate_list in CRATE_GROUPS.items():
                for crate in crate_list:
                    if crate.lower() in crate_tags:
                        output_folder = os.path.join(playlist_root, group, crate)
                        os.makedirs(output_folder, exist_ok=True)
                        dest_path = os.path.join(output_folder, f)

                        if os.path.exists(dest_path):
                            print(f"Skipped duplicate: {dest_path}")
                            matched = True
                            continue

                        if DRY_RUN:
                            print(f"[DRY RUN] Would copy {file_path} to {dest_path}")
                            matched = True
                        else:
                            shutil.copy2(file_path, dest_path)
                            print(f"Copied {f} to {group}/{crate}")
                            matched = True

            # Only dump in Unsorted if tags existed but no matches were found
            if not matched:
                if DRY_RUN:
                    print(f"[DRY RUN] Would copy {file_path} to {os.path.join(unsorted_folder, f)}")
                else:
                    shutil.copy2(file_path, os.path.join(unsorted_folder, f))
                    print(f"Copied {f} to Unsorted (tags present but no match)")

    print(f"Finished: all song files have been copied to playlist folders by crate (comment tags).")
    return


# called by menu()
def run_editor(source_folder):
    # display possible custom tags
    print("--------------------------------------------------------------------------------", flush=True)
    print("* Core Comment Tags *", flush=True)
    print("warrior-combat-gym\tturbo-race-track\tsubterranean-drip-lab\nopen-format-club\tlounge-of-ascension\tbar-of-melancholy", flush=True)
    print("* Sub Comment Tags *", flush=True)
    print("alien\tbars\tfrozen\tguitar\thaunted\tmeta\norganic\tsmoke\tmagic\tsummer\ttalkbot\tscience", flush=True)
    print("* Utility Comment Tags *", flush=True)
    print("anthem\tweapon\tsample\ttool\tmashup\tmixlet\nopener\tcloser\tpsidemica\tmix\tother\tpandemica", flush=True)
    print("--------------------------------------------------------------------------------", flush=True)
    # user provides filename or tag to filter results, or nothing for all results
    filter_key = input("Filter by filename or tag (comment/title/artist/album/genre/date). Leave blank for all: ").strip().lower()
    if filter_key == "":
        filter_key = None
    filter_value = ""
    if filter_key:
        # example: if genre was entered as the filter tag, provide which genre to match
        filter_value = input(f"Enter value to match in {filter_key}: ").strip()

    print("Scanning files (this can take a while on large libraries)...", flush=True)
    # retrieve songs that match the filter parameters and display the number of matches
    matches = filter_songs(source_folder, filter_key, filter_value)
    print(f"\nFound {len(matches)} matching files.")
    
    # end execution if there are no filter results
    if not matches:
        print("No matching songs found.")
        return

    # ask user for metadata edits
    edit_choice = input("Do you want to edit tags for these files? (y/n): ").strip().lower()
    if edit_choice == "y":
        # they will be edited all at once, same values for all
        # TODO: determine if batch editing is even needed
        bulk_edit_tags(matches)

    # ask user for playlist output
    playlist_choice = input("Do you want to copy these files to a playlist folder? (y/n): ").strip().lower()
    if playlist_choice == "y":
        # create playlist, user provides destination folder
        output_folder = input("Enter playlist output folder path: ").strip()
        copy_to_playlist(matches, output_folder)
        print("\nPlaylist created successfully!")
        # TODO: edit print logic for when playlist already exists and songs are just copied

    return


# called by setup()
def menu(source_folders):
    while True:
        print(f"Which subroutine do you want to run?")
        mode = input("(n)ormal editor (g)enre playlists, (c)rate playlists, (q)uit: ").strip().lower()

        if mode == "n":
            for folder in source_folders:
                run_editor(folder)
        elif mode == "g":
            for folder in source_folders:
                build_genre_playlists(folder)
        elif mode == "c":
            for folder in source_folders:
                build_crate_playlists(folder)
        elif mode == "q":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid mode. Try again.")


# called by main()
# Supports scanning multiple libraries (lossy + lossless) in one run.
# Each library is processed independently using the same logic.
def setup():
    lossy_raw = input("Enter LOSSY library folder path (or leave blank to skip): ").strip().strip('"')
    lossless_raw = input("Enter LOSSLESS library folder path (or leave blank to skip): ").strip().strip('"')

    sources = []

    if lossy_raw:
        sources.append(Path(lossy_raw).expanduser().resolve())

    if lossless_raw:
        sources.append(Path(lossless_raw).expanduser().resolve())

    if not sources:
        print("No source folders provided. Exiting.")
        sys.exit(1)

    menu([str(p) for p in sources])


def main():
    print("=== Music Library Manager ===", flush=True)
    print("--- Edits MP3/M4A Metadata and Builds Playlists ---", flush=True)
    setup()


if __name__ == "__main__":
    main()
