import shutil


def zip_dir(dir_name):
    shutil.make_archive(dir_name, 'zip', dir_name)


def del_dir(dir_name):
    shutil.rmtree(dir_name)


def zip_and_del(dir_name):
    print("Getting your videos ready for delivery.")
    zip_dir(dir_name)
    print("Cleaning up your directory.")
    del_dir(dir_name)
    print("{} is ready for delivery.".format(dir_name))


if __name__ == '__main__':
    zip_dir('tester_dir')