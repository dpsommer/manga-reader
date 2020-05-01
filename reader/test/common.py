import os
import shutil

DIRPATH = os.path.abspath(os.path.dirname(__file__))


def clean_tree(dir):
    if os.path.isdir(dir):
        for filename in os.listdir(dir):  # teardown
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        os.rmdir(dir)
