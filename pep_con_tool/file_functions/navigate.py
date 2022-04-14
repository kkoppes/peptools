"""file navigation functions"""
import os


# function to find all files or those of a certain type in a directory
def find_files(path, extension=None, subfolders=False):
    """
    list files from directory
    """
    if subfolders:
        return [os.path.join(dirpath, filename)
                for dirpath, dirnames, filenames in os.walk(path)
                for filename in filenames
                if extension is None or filename.endswith(extension)]
    else:
        return [os.path.join(path, filename)
                for filename in os.listdir(path)
                if extension is None or filename.endswith(extension)]



