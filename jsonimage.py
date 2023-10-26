import os
import json

# specify the directory you want to scan for image files
directory = './image_employee'

# get a list of all files in the directory
files_in_directory = os.listdir(directory)

# filter the list for files ending in .jpg, .jpeg, .png
image_files = [file for file in files_in_directory if file.endswith(('.jpg', '.jpeg', '.png'))]

# create a dictionary where the keys are the index order and the values are the file paths
image_dict = {i: os.path.join(directory, image_file) for i, image_file in enumerate(image_files)}

# write the dictionary to a json file
with open('image_files.json', 'w') as f:
    json.dump(image_dict, f)
