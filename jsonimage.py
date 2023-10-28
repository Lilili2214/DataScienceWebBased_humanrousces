import os
import json

directory = './image_employee'

files_in_directory = os.listdir(directory)

image_files = [file for file in files_in_directory if file.endswith(('.jpg', '.jpeg', '.png'))]

image_dict = {i: os.path.join(directory, image_file) for i, image_file in enumerate(image_files)}

with open('image_files.json', 'w') as f:
    json.dump(image_dict, f)
