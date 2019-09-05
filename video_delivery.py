"""Video Delivery

Zips a directory and deletes it

This file can also be imported as a module and contains the following
functions:

    * zip_dir - zips a file or directory
    * del_dir - Deletes a given directory
    * zip_and_del - zips a directory then deletes the original directory
"""


import shutil


def zip_dir(dir_name: str):
    """zips a file or directory

    Args:
        dir_name (str): The directory to zip

    Returns:
        None
    """
    shutil.make_archive(dir_name, 'zip', dir_name)


def del_dir(dir_name: str):
    """Deletes a given directory

    Args:
        dir_name (str): The directory to be deleted

    Returns:
        None
    """
    shutil.rmtree(dir_name)


def zip_and_del(dir_name: str):
    """zips a directory then deletes the original directory

    Args:
        dir_name (str): The directory to be zipped then deleted

    Returns:
        None
    """
    print("Getting your videos ready for delivery.")
    zip_dir(dir_name)
    print("Cleaning up your directory.")
    del_dir(dir_name)
    print("{} is ready for delivery.".format(dir_name))


if __name__ == '__main__':
    zip_dir('tester_dir')