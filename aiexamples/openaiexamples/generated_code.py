import os

current_dir = os.getcwd()
files = os.listdir(current_dir)

for file in files:
    print(file)