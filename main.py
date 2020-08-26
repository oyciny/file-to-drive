import os
import shutil
import multiprocessing
import subprocess


def main():
    # Check if the drive exists before continuing. If no drive found check again or quit
    if os.path.exists("/Volumes/EOS_DIGITAL/DCIM/100CANON"):
        DRIVE_PATH = '/Volumes/EOS_DIGITAL/DCIM/100CANON'
        path_handler(DRIVE_PATH)
    else:
        QUIT_CONDITION = get_quit_condition()
        if QUIT_CONDITION == 0 or QUIT_CONDITION == 1:
            handle_quit_condition(QUIT_CONDITION)


def get_quit_condition():
    QUIT_CONDITION = input("Drive not found! Check again? (Y/N) ")
    if QUIT_CONDITION == "Y" or QUIT_CONDITION == "y":
        return 0
    if QUIT_CONDITION == "N" or QUIT_CONDITION == "n":
        return 1
    else:
        print("Invalid option!")
        get_quit_condition()


def handle_quit_condition(condition):
    if condition == 0:
        main()
    else:
        exit()


# Path Handler Function
def path_handler(path):
    FILES = grab_files(path, ".CR2")
    FILE_DESTINATION = create_folder_for_files(input("Please name your new folder: "))
    for file in FILES:
        # Use multiprocessing to speed up the copying of files
        multiprocessing.Process(target=copy_file, args=(FILE_DESTINATION, path+"/"+file)).start()
    # Open Finder to the copied files
    subprocess.call(["open", FILE_DESTINATION])


def grab_files(path, ext):
    return_list = []
    for file in os.listdir(path):
        if file.endswith(ext):
            return_list.append(file)
    return return_list


# File copying handler
def copy_file(dest, file):
    shutil.copy2(file, dest)


# Check if folder exists. If it does use it otherwise create it and continue
def create_folder_for_files(folder_name):
    if os.path.isdir("/Users/cobymckinney/Documents/Photography/" + folder_name):
        return "/Users/cobymckinney/Documents/Photography/" + folder_name
    else:
        os.mkdir("/Users/cobymckinney/Documents/Photography/" + folder_name)
        return "/Users/cobymckinney/Documents/Photography/" + folder_name


if __name__ == '__main__':
    main()
