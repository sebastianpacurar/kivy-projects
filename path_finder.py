import os


def find_project_root(target="README.md"):
    # go up x levels through directories until root is reached
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):  # go up one level iteratively
        if target in os.listdir(current_dir):
            return current_dir  # return directory if README.md is present
        current_dir = os.path.dirname(current_dir)  # go up one level
