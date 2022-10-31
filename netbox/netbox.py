import os


def get_current_os_info():

    return "Linux" if os.name == "posix" else "Windows"
