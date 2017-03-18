import os

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)