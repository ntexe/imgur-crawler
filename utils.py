import os

def create_folder_if_not_exits(path):
    if not os.path.exists(path):
        os.makedirs(path)
