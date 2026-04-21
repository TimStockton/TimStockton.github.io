"""
Program: directory_map.py [v1.0.0]
Description: Creates a visual tree representation of directory structures. Currently limited to 5 levels.
Author: Timothy Stockton
Created: 20220210

use cases:
    - Auditing large folders
    - Verifying export structures
    - Quick sanity checks before bulk operations

TO DO:
    - Improve tree display formatting

notes:
    Reference implementations for CLI-style directory trees:
    - https://realpython.com/directory-tree-generator-python/
    - https://github.com/realpython/materials/tree/master/directory-tree-generator-python
"""

#imports
import os

#variables
usr_dir = ""
one_dir = ""
layer_one = []
two_dir = ""
layer_two = []

#main
print("*****************************************************")
print("*            ~ Welcome to Directory Map ~           *")
print("* Which directory would you like me to map for you? *")
usr_dir = input()
print("*                ... mapping now ...                *")
print("*****************************************************")

print("*****************************************************")
#change current directory to user entered directory
os.chdir(usr_dir)
#print current directory
#print(os.listdir())
#fill layer_one[] with folder names of initial directory
layer_one = os.listdir(usr_dir)
#print("The number of subdirectories in " + usr_dir + " is: " + str(len(layer_one)))
one_dir = usr_dir
#iterate through up to 5 levels of folders from given directory
for index, folder in enumerate(layer_one):
    cur_dir = one_dir + "\\" + layer_one[index]
    if os.path.isdir(cur_dir):
        print(folder) #put before cur_dir modification to also output non folders
        layer_two = os.listdir(cur_dir)
        two_dir = cur_dir
        for index, folder in enumerate(layer_two):
            cur_dir = two_dir + "\\" + layer_two[index]
            if os.path.isdir(cur_dir):
                print("   └── " + folder) #put before cur_dir modification to also output non folders
                layer_three = os.listdir(cur_dir)
                three_dir = cur_dir
                for index, folder in enumerate(layer_three):
                    cur_dir = three_dir + "\\" + layer_three[index]
                    if os.path.isdir(cur_dir):
                        print("          └── " + folder) #put before cur_dir modification to also output non folders
                        layer_four = os.listdir(cur_dir)
                        four_dir = cur_dir
                        for index, folder in enumerate(layer_four):
                            cur_dir = four_dir + "\\" + layer_four[index]
                            if os.path.isdir(cur_dir):
                                print("                 └── " + folder) #put before cur_dir modification to also output non folders
                                layer_five = os.listdir(cur_dir)
                                five_dir = cur_dir
                                for index, folder in enumerate(layer_five):
                                    cur_dir = five_dir + "\\" + layer_five[index]
                                    if os.path.isdir(cur_dir):
                                        print("                        └── " + folder) #put before cur_dir modification to also output non folders
print("*****************************************************")
