import os
import shutil
import subprocess
import multiprocessing
from datetime import date


def main():
    EXTERNAL_DRIVE_PATH = "/Volumes/EOS_DIGITAL"
    if os.path.exists(EXTERNAL_DRIVE_PATH):
        IMAGES_PATH = EXTERNAL_DRIVE_PATH + "/DCIM/100CANON"
        IMAGES = get_images_from_path(IMAGES_PATH)
        TODAY_DATE = get_formatted_date()
        COPY_LOCAL = create_copy_local("/Users/cobymckinney/Documents/Photography/" + TODAY_DATE)
        COPY_PROCESSES = []
        for image in IMAGES:
            IMAGE_PATH = IMAGES_PATH + "/" + image
            COPY_PROCESSES.append(multiprocessing.Process(target=copy_image, args=(IMAGE_PATH, COPY_LOCAL)))
        for copy_process in COPY_PROCESSES:
            copy_process.start()
            copy_process.join()
        subprocess.call(["open", COPY_LOCAL])
        eject_disk()
        print("Images Copied and SD CARD Ejected!")
    else:
        exit()


def get_images_from_path(path):
    image_list = []
    for image in os.listdir(path):
        image_list.append(image)
    return image_list


def copy_image(IMG_PATH, DEST):
    shutil.copy2(IMG_PATH, DEST)


def create_copy_local(local):
    if os.path.isdir(local):
        return local
    else:
        os.mkdir(local)
        return local


def eject_disk():
    os.system("diskutil unmountDisk /dev/disk3")


def get_formatted_date():
    today = date.today()
    return today.strftime("%B-%d-%Y")


if __name__ == "__main__":
    main()
