import os

import ping3


class Netbox(object):
    def __init__(self) -> None:
        self.ping = ping3.ping

    def check_host_state(self, host, src_addr=None, interface=None):

        name = Netbox._get_current_os_info()
        if name == "Windows":
            return self.ping(host=host, src_addr=src_addr)

        elif name == "Linux":
            return self.ping(host=host, interface=interface)
        else:
            return self.ping(host)

    @staticmethod
    def _get_current_os_info():

        if os.name == "posix" and os.uname().sysname == "Darwin":
            return "MacOS"
        elif os.name == "posix":
            return "Linux"
        else:
            return "Windows"
