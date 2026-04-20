#!/bin/bash

# script name: clean_list.sh
# script author: Timothy Stockton
# last modified: 20251017
#
# this script concatenates lists together and outputs the result
# the original order is preserved, redundant items are removed
# it accounts for both space and colon separated lists

# prepare output variable
master_list=""

# combine args
input="$*"

# add dots to leading, trailing, and double colons
# replace colons with spaces
cleaned=$(echo $input | sed -e 's/^:/.:/' -e 's/::/:.:/' -e 's/:$/:./' -e 's/:/ /g')

# loop over all args
for sub_list in $cleaned; do
        case $master_list in  
        "")
            # first iteration, master_list is empty
            master_list="$sub_list"
            ;;
        $sub_list|$sub_list:*|*:$sub_list:*|*:$sub_list)
            # sub_list is somewhere in master_list already
            # do nothing, deduplicate
            continue
            ;;
        *)  
            # sub_list not yet in master_list
	    # add it to the end, colon separated
            master_list="$master_list:$sub_list"
            ;;
        esac
    done
echo $master_list
