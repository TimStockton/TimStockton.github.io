#!/bin/bash

# Script: user_management.sh
# Author: Timothy Stockton
# Modified: 20251212
#
# This script:
#   - Reports accounts with no password (and locks them)
#   - Reports expired accounts
#   - Reports expiration dates for all accounts
#   - Reports accounts that never expire
#   - Locks or unlocks specified accounts
#   - Adds users (interactively or from file, not crontab)
#         username, home dir, full name, password, exp date
#         read from command line or file
#         reset password on first login
#   - Changes exp date for specified accounts (except root)
#   - Optionally logs all actions to a specified file
#
# Must run as root (modifies system accounts)


# Path to logfile, if used
LOGFILE=""
# System file that stores user password/expiration info
SHADOW="/etc/shadow"

# Print to console (and logfile if enabled)
# -------------------------
log() {
    if [ -n "$LOGFILE" ]; then
        echo "$@" >> "$LOGFILE"
    fi
    echo "$@"
}

# Make sure the script is running as root
# -------------------------
require_root() {
    # EUID = effective user ID, root ID is 0
    if [ "$EUID" -ne 0 ]; then
        echo "You must run this script as root."
        exit 1
    fi
}

# Report users with no password and lock them
# -------------------------
report_no_pass() {
    log "*** Users With No Password ***"

    # $1 is the username field
    # $2 is the password field
    # password value is * for system accounts
    # password value ! or !* means account was never assigned a password
    # locking accounts with password ! or !* does nothing
    # awk creates list of users
    awk -F: '($2=="" || $2=="!" ||$2=="!*") {print $1}' "$SHADOW" | while read user; do
        if [ -n "$user" ]; then
            log "User $user has no password and will be locked if not already"
            usermod -L "$user"
        fi
    done
}

# Report expired accounts using chage output
# -------------------------
report_expired() {
    log "*** Expired Accounts ***"

    # date +%s = seconds since unix epoch (January 1st 1970)
    # 86400 = seconds in a day = 60 sec x 60 min x 24 hrs
    today=$(( $(date +%s) / 86400 ))

    # Read users from $SHADOW (input redirection at end of while)
    while IFS=: read user pass last min max warn inactive expire; do

        # Only check accounts with an expiration, -1 means never expire
        if [ -n "$expire" ] && [ "$expire" != "-1" ]; then

            # Log user if expiration date is before today
            # $expire is default formatted as days (not seconds)
            if [ "$expire" -lt "$today" ]; then
                log "$user : EXPIRED"
            fi
        fi
    done < "$SHADOW"
}

# Report expiration date for every user
# -------------------------
report_expirations() {
    log "*** Expiration Dates ***"

    # Extract all usernames (field 1) from $SHADOW
    cut -d: -f1 "$SHADOW" | while read user; do

        # Print human readable exp, filter exp date line, extract field 2 (date string)
        exp_date=$(chage -l "$user" | grep "Account expires" | cut -d: -f2)
        log "$user expires on: $exp_date"
    done
}

# Report all accounts that never expire
# -------------------------
report_no_expire() {
    log "*** Accounts That Never Expire ***"

    # Read users from $SHADOW (input redirection at end of while)
    while IFS=: read user pass last min max warn inactive expire; do

        # account never expires if empty or -1
        if [ -z "$expire" ] || [ "$expire" = -1 ]; then
            log "$user
        fi
    done < "$SHADOW"
}

# Lock a list of accounts
# -------------------------
lock_users() {
    log "*** Locking Users ***"

    for user in "$@"; do
        log "Locking $user"
        usermod -L "$user"
    done
}

# Unlock a list of accounts
# -------------------------
unlock_users() {
    log "*** Unlocking Users ***"

    for user in "$@"; do
        log "Unlocking $user"
        usermod -U "$user"
    done
}

# Add a user interactively (one user at a time)
# -------------------------
add_user() {
    username="$1"

    log "*** Adding user: $username ***"

    # Check if user already exists, discard stdout and stderr
    if id "$username" >/dev/null 2>&1; then
        log "User $username already exists."
        return
    fi

    # Prompt for home directory, default to /home/<username>
    read -p "Home Directory [/home/$username]: " home
    home=${home:-/home/$username}

    # Prompt for name
    read -p "Full Name: " full_name

    # Prompt for password twice (silently)
    # echo used for newline
    read -s -p "Password: " pw1; echo
    read -s -p "Confirm Password: " pw2; echo

    if [ "$pw1" != "$pw2" ]; then
        echo "Passwords do not match!"
        exit 1
    fi

    # Prompt for exp date
    read -p "Expiration date (YYYY-MM-DD or leave empty): " exp_date

    # Create the user
    useradd -m -d "$home" -c "$full_name" "$username"
    echo "$username:$pw1" | chpasswd

    # Force password change at next login
    chage -d 0 "$username"

    # Set expiration (except root)
    if [ -n "$exp_date" ]; then
        if [ "$username" = "root" ]; then
            log "Not setting expiration for root"
        else
            usermod -e "$exp_date" "$username"
        fi
    fi

    log "User $username created"
}

# Add users from a CSV file
# File Format: username,home,full_name,password,expiration_date(YYYY-MM-DD)
# -------------------------
add_users_from_file() {
    file="$1"

    log "*** Adding Users From File ***"

    # Read file entries from $file (input redirection at end of while)
    while IFS=, read username home full_name password exp_date; do

        # Skip header line (if present)
        if echo "$username" | grep -qi "username"; then
            continue
        fi

        # Skip existing users, discard stdout and stderr
        if id "$username" >/dev/null 2>&1; then
            log "User $username already exists... Skipping"
            continue
        fi

        # Extract home directory (use default if empty)
        home=${home:-/home/$username}

        # Create the user
        useradd -m -d "$home" -c "$full_name" "$username"
        echo "$username:$password" | chpasswd

        # Force password change at next login
        chage -d 0 "$username"

        # Set expiration (skip root)
        if [ -n "$exp_date" ] && [ "$username" != "root" ]; then
            usermod -e "$exp_date" "$username"
        fi

        log "User $username created from file"
    done < "$file"
}

# Change expiration date for a user (except root)
# -------------------------
set_expire() {
    username="$1"
    # (YYYY-MM-DD)
    newdate="$2"

    log "*** Changing Expiration ***"

    if [ "$username" = "root" ]; then
        log "Cannot set expiration for root"
        return
    fi

    if ! id "$username" >/dev/null 2>&1; then
        log "User $username does not exist"
        return
    fi

    log "Setting expiration for $username to $newdate"
    usermod -e "$newdate" "$username"
}

# Main
# -------------------------

# Ensure root privileges
require_root

# If the first arg is "log", set the logfile
if [ "$1" = "log" ]; then
    LOGFILE="$2"
    # discard log config args
    shift 2
fi

# Extract non-log arg then discard
cmd="$1"
shift

# Make function call based on command arg
case "$cmd" in
    report_no_pass)      report_no_pass ;;
    report_expired)      report_expired ;;
    report_expirations)  report_expirations ;;
    report_no_expire)    report_no_expire ;;
    lock)                lock_users "$@" ;;
    unlock)              unlock_users "$@" ;;
    add_user)            add_user "$@" ;;
    add_users_from_file) add_users_from_file "$1" ;;
    set_expire)          set_expire "$1" "$2" ;;
    *)
        echo "Unknown command: $cmd"
        echo "Available commands:"
        echo "report_no_pass"
        echo "report_expired"
        echo "report_expirations"
        echo "report_no_expire"
        echo "lock USER(S)"
        echo "unlock USER(S)"
        echo "add_user USER"
        echo "add_users_from_file FILE"
        echo "set_expire USER DATE"
        exit 1
        ;;
esac
