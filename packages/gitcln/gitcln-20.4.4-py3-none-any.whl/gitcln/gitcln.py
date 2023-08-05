"""
gitcln CLI implementation.
"""
# imports
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os import walk, getcwd, path, remove
from fnmatch import fnmatch
from platform import system
from shutil import rmtree


def main() -> None:
    """
    gitcln CLI main entry point function.
    """
    # get CLI args
    args = argsp()
    # get .gitignore lists
    ddirs, dirs, fils = gitignore_reader()
    # search for .gitignore file(s)/folder(s) and unlink them
    for root, subdirs, files in walk(getcwd()):
        # unlink matched subdirs
        for subdir in subdirs:
            # check if the folder not in CLI ignore list
            if not subdir in args.directories:
                # get directory path
                dirpath = path.join(root, subdir)
                # check ddirs
                for dd in ddirs:
                    # get ddirectory path
                    ddirpath = path.join(root, subdir, dd[1])
                    # match by file name match function
                    if fnmatch(dd[0], subdir):
                        # check if the file exists
                        if path.exists(ddirpath):
                            strdd = "/".join(dd)
                            try:
                                rmtree(path.join(dirpath, dd[1]))
                                print(
                                    pstr(
                                        f"Directory: {path.relpath(dirpath)} :: removed :: {strdd}/",
                                        True,
                                    )
                                )
                            except Exception as ex:
                                print(
                                    pstr(
                                        f"Unable to remove {strdd} :: error :: {ex}",
                                        False,
                                    )
                                )
                # check if the folder on .gitignore list
                for gi in dirs:
                    # match by file name match function
                    if fnmatch(subdir, gi):
                        try:
                            rmtree(dirpath)
                            print(
                                pstr(
                                    f"Directory: {path.relpath(dirpath)} :: removed :: {gi}/",
                                    True,
                                )
                            )
                        except Exception as ex:
                            print(
                                pstr(
                                    f"Unable to remove {path.relpath(dirpath)} :: error :: {ex}",
                                    False,
                                )
                            )
        # unlink matched files
        for f in files:
            # check if the file not in CLI ignore list
            if not f in args.files:
                fpath = path.join(root, f)
                # check if the file on .gitignore list
                for gi in fils:
                    # match by file name match function
                    if fnmatch(f, gi):
                        try:
                            remove(fpath)
                            print(
                                pstr(
                                    f"File: {path.relpath(fpath)} :: removed :: {gi}",
                                    True,
                                )
                            )
                        except Exception as ex:
                            print(
                                pstr(
                                    f"Unable to remove {path.relpath(fpath)} :: error :: {ex}",
                                    False,
                                )
                            )


def argsp() -> list:
    """
    CLI args parser and handler using argpase stdlib.

    :returns: parsed arg list
    :rtype: list
    """
    parser = ArgumentParser(
        description="CLI tool aim to clean local git repository from .gitignore file(s)/folder(s).",
        formatter_class=ArgumentDefaultsHelpFormatter,
        prog="gitcln",
    )
    # ignore DIRS/FILES
    parser.add_argument(
        "-d",
        "--directories",
        help="Directory(ies) to ignore.",
        nargs="*",
        default=[],
        type=str,
    )
    parser.add_argument(
        "-f", "--files", help="File(s) to ignore.", nargs="*", default=[], type=str,
    )
    # get args
    args = parser.parse_args()
    # return validated args
    return args


def gitignore_reader() -> tuple:
    """Read gitignore file and return ignore list.

    :returns: ignore tuple of two list ([ddirs list of lists], [dirs list], [files list])
    :rtype: tuple
    """
    # check if .gitignore exist in current directory.
    if path.exists(path.join(getcwd(), ".gitignore")):
        try:
            # init .gitignore file(s)/folder(s) list.
            ddirs, dirs, files = [], [], []
            # open gitignore file
            with open(".gitignore", "r") as gitignore:
                # iterate over each ignore line
                for ignore in gitignore.readlines():
                    # skip comment line
                    if ignore[0] != "#" and ignore[0] != "\n":
                        if ignore.count("/") == 2:
                            ddirs.append(ignore.strip("\n").split("/")[:2])
                        else:
                            if "/" in ignore:
                                dirs.append(ignore.strip("\n").strip("/"))
                            else:
                                files.append(ignore.strip("\n"))
            return ddirs, dirs, files
        except IOError as ex:
            print(pstr(f"Cannot read .gitignore file:\n\t{ex}", False))
            exit(1)
    else:
        print(
            pstr(f".gitignore file does not exist on this directory: {getcwd()}", False)
        )
        exit(1)


ISLINUX = True if system() == "Linux" else False


def pstr(string: str, success: bool) -> str:
    """pretty string.

    :param string: string to prettify
    :type string: str
    :param success: success status
    :type success: bool
    :returns: pretty string 
    :rtype: str
    """
    # only linux based os
    if ISLINUX:
        # color the string
        if success:
            # green color
            return f"\033[0;37;42m \033[1;37;40m {string}\033[0m"
        else:
            # red color
            return f"\033[0;37;41m \033[1;37;40m {string}\033[0m"
    else:
        return string
