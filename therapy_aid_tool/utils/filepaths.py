import os

def get_filepaths_from_dir(dirpath, key=None):
    filenames = sorted(os.listdir(dirpath), key=key)
    filepaths = [os.path.join(os.path.abspath(dirpath), filename)
                 for filename in filenames]
    return filepaths