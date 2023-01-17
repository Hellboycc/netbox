import platform
import typing as t

from .wifi import LinuxAdapter, MacAdapter, WifiAdapter, WindowsAdapter


def get_current_os_info() -> str:
    """Obtain operation system infromation.

    Returns:
        String of operaton system name. For example: Linux or Windows
    """
    return platform.system()


def create_adapter(name: str) -> t.Optional[WifiAdapter]:
    """Create and adapter based on operating system information.

    Returns:
        An object of adapter.
    """
    adapter: t.Optional[WifiAdapter] = None
    if name == "Windows":
        adapter = WindowsAdapter()
    elif name == "Linux":
        adapter = LinuxAdapter()
    else:
        adapter = MacAdapter()
    return adapter
