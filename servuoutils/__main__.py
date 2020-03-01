import os

SCRIPTS_PATH = os.path.join("servuoutils", "scripts")
SCRIPTS_LIST = [os.path.join(SCRIPTS_PATH, f) for f in os.listdir(SCRIPTS_PATH) 
                if os.path.isfile(os.path.join(SCRIPTS_PATH, f)) and not f.startswith("__")]

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