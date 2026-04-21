#!/bin/bash
# create-test-structure.sh
# Creates test directory structure for fix-spaces.sh

create_test_structure() {
    local base_dir="$1"
    
    # Remove existing test directory if present
    rm -rf "$base_dir" 2>/dev/null
    
    echo "Creating test structure in '$base_dir'..."
    
    # Create directory structure with spaces
    mkdir -p "$base_dir/E F/G H/J    K"
    
    # Create files with spaces
    touch "$base_dir/a b"
    touch "$base_dir/E F/a b"
    touch "$base_dir/E F/G H/a b"
    touch "$base_dir/E F/G H/J    K/a b"
    
    # Create some files without spaces for comparison
    touch "$base_dir/normal_file"
    touch "$base_dir/E F/another_normal"
    
    echo "Created test structure:"
    find "$base_dir" -print | sort
}

# Usage: ./create-test-structure.sh "Test Dir"
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"directory-name\""
    echo "Example: $0 \"Test Dir\""
    exit 1
fi

create_test_structure "$1"