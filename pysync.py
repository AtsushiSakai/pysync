"""
pysync: A rsync like tool by pure python only using standard libraries.

Author: Atsushi Sakai

"""
import os
import json
from os.path import abspath, join, isdir, expanduser, dirname, relpath, basename
import shutil
import time


def run(conf_file_path="~/pysync_conf.json"):
    """
    Run synchronization task with json config file.

    :param conf_file_path: conf file path. Default if ~/pysync_conf.json
    """
    with open(__normalize_path(conf_file_path)) as f:
        conf_dict = json.load(f)
        sync(conf_dict["sources"], conf_dict["dest_dir"], conf_dict["excludes"])


def sync(sources: list, dest_dir: str, excludes: list):
    """
    Sync sources directories under dest directory

    :param sources: source directory path list
    :param dest_dir: destination directory
    :param excludes: exclude path string list
    """
    print("Start sync!!")
    __validate_input(sources, dest_dir, excludes)
    start = time.time()
    n_checked_file, n_copied_file = 0, 0

    dest_dir = __normalize_path(dest_dir)
    __create_dir_if_not_exist(dest_dir)
    print(f"{dest_dir=}")

    for source in sources:
        source = join(__normalize_path(source), "")  # add / if it does not exist
        print(f"{source=}")

        for cur_dir, dirs, files in os.walk(source):

            if __in_excludes(cur_dir, excludes):
                continue

            # create directory
            copy_dir = join(dest_dir, basename(dirname(source)),
                            relpath(cur_dir, source))
            __create_dir_if_not_exist(copy_dir)

            for file in files:
                n_checked_file += 1
                source_file_path = join(cur_dir, file)
                dest_file_path = join(copy_dir, file)

                if (__copy_if_not_exist(dest_file_path, source_file_path) or
                        __copy_if_update(dest_file_path, source_file_path)):
                    print(f"{source_file_path=} to {dest_file_path}")
                    n_copied_file += 1

    elapsed_time = time.time() - start
    print(f"Done!! {elapsed_time=}[sec], {n_checked_file=}, {n_copied_file=}")


def __normalize_path(path):
    return abspath(expanduser(path))


def __validate_input(sources, dest_dir, excludes):

    if not isinstance(sources, list):
        raise TypeError("sources should be list")
    elif not isinstance(dest_dir, str):
        raise TypeError("path should be str")
    elif not isinstance(excludes, list):
        raise TypeError("excludes should be list")

    for source in sources:
        if not isdir(expanduser(source)):
            raise ValueError(f"Invalid {source=}")

    if not isdir(expanduser(dirname(dest_dir))):
        raise ValueError(f"Invalid {dest_dir=}")


def __copy_if_not_exist(dest_file_path, source_file_path):
    if not os.path.exists(dest_file_path):
        try:
            shutil.copy2(source_file_path, dest_file_path)
            print("Copied!! Because the file does not exists")
        except OSError as e:
            print(f"OSError {e}")
        except FileNotFoundError as e:
            print(f"FileNotFoundError {e}")

        return True
    return False


def __copy_if_update(dest_file_path, source_file_path):
    source_file_time = os.stat(source_file_path).st_mtime
    dest_file_time = os.stat(dest_file_path).st_mtime
    if source_file_time - dest_file_time > 1:
        try:
            shutil.copy2(source_file_path, dest_file_path)
            print("Copied!! Because the file updated")
        except (FileNotFoundError, PermissionError) as e:
            print(e)
        return True
    return False


def __create_dir_if_not_exist(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


def __in_excludes(dir_name, excludes):
    for exclude in excludes:
        if exclude in dir_name:
            return True
    return False


def main():
    run()


def main_direct_sync_call():
    sources = ["../pysync/"]
    dest_dir = "~/backup_test/"
    excludes = [".git", ".idea"]
    sync(sources, dest_dir, excludes)


if __name__ == '__main__':
    run()


