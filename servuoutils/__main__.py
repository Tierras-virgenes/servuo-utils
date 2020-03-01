import os
from os.path import splitext, basename, isfile, join
from pathlib import Path

SCRIPTS_PATH = join(Path(__file__).parent.absolute(), "scripts")
SCRIPTS_LIST = [basename(splitext(join(SCRIPTS_PATH, f))[0]) for f in os.listdir(SCRIPTS_PATH) 
                if isfile(join(SCRIPTS_PATH, f)) and not f.startswith("__")]

# https://stackoverflow.com/questions/3178285/list-classes-in-directory-python
CLASSES_LIST = ["TODO"]

def main():
    print("Usage:")
    print("To use binaries you can execute them with `python -m servuoutils.scripts.SCRIPT_NAME -OPTION`")
    print("Run one of the following scripts:")
    for script in SCRIPTS_LIST:
        print("\t- " + script)
    print("To use as a library, import and manage one of the following classes:")
    for sclass in CLASSES_LIST:
        print("\t- " + sclass)
    print("* Note: User -h option to print help.")

if __name__ == "__main__":
    main()