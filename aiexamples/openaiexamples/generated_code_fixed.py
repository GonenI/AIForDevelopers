import os

# @@@@@@ Get the current working directory
current_dir = os.getcwd()

# @@@@@@ Get a list of all files in the current directory
files = os.listdir(current_dir)

# @@@@@@ Print each file 
for file in files:
    print(file)