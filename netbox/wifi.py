import re
import subprocess
import typing as t

from . import logger
from .constant import WiFiState
from .exception import CommandException


class WifiAdapter(object):
    """A class that contains generic properties and methods."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def execute_command(command: str) -> str:
        """Execute the specified command and return the result.

        Args:
            command (str): Commands to be executed.

        Raises:
            CommandException: Exception of command executes failed.

        Returns:
            String results of command executes successfully.
        """
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        if process.returncode != 0:
            raise CommandException(message=f"Command: '{command}' executed failed.")
        return process.stdout


class MacAdapter(WifiAdapter):
    """Adapter of Wi-Fi operation under MacOS."""

    AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

    def __init__(self) -> None:
        pass

    def get_current_network(self) -> t.Dict[str, str]:
        return self._get_current_wifi_info()

    def get_networks(self) -> t.List[t.Dict[str, str]]:
        return self._get_scan_results()

    def _get_current_wifi_info(self) -> t.Dict[str, str]:
        """Obtain current connected wifi information.

        Returns:
            Connected wifi information. For example: {'SSID': 'TP-Link001', 'agrCtlRSSI': "-30"}
        """
        command = f"{self.AIRPORT_PATH} -I"
        output = self.execute_command(command=command)
        info = {}
        for line in output.split("\n"):
            if ":" in line:
                (k, v) = line.split(":")
                k = k.strip()
                v = v.strip()
                info.update({k: v})
        return info

    @property
    def interface(self) -> str:
        """Obtain current wifi interface name.

        Returns:
            Wifi interface name. For example: en0
        """
        command = "networksetup -listallhardwareports | awk '/Wi-Fi|AirPort/ {getline; print $NF}'"
        output = self.execute_command(command=command)
        return output.strip()

    def _get_scan_results(self) -> t.List[t.Dict[str, str]]:
        """Obtain surrounding wifi network information.

        Returns:
            Wifi network information.
        """
        command = f"{self.AIRPORT_PATH} -s"
        output = self.execute_command(command=command)
        # clean output data
        _rets = list()
        rets = list()
        for line in output.split("\n")[1:]:
            if line != "":
                line = re.sub(r"\s{2,}", "|", line.strip().replace("--", ""))
                _rets.append(line)
        for line in _rets:
            _line = line.split("|")
            rets.append(
                {
                    "ssid": _line[0],
                    "rssi": _line[1],
                    "channel": _line[2],
                    "HT": _line[3],
                    "security": _line[4],
                }
            )
        return rets

    def get_all_ssid(self):
        """Obtain a collection of available ssid.

        Returns:
            Collection of ssid. For example: ['test01', 'ChinaNet-test001', 'TP-Link1111']
        """
        results = self._get_scan_results()
        all_ssid = list()
        for item in results:
            ssid = item.get("ssid", "")
            all_ssid.append(ssid)
        return all_ssid

    def is_on_or_off(self) -> WiFiState:
        """Obtain state of wifi interface on or off.

        Returns:
            ON if wifi interface state is on, otherwise OFF.
        """
        command = f"networksetup -getairportpower {self.interface}"
        if "On" in self.execute_command(command=command):
            return WiFiState.ON
        else:
            return WiFiState.OFF

    def get_current_ssid(self) -> t.Optional[str]:
        """Obtain current connected ssid.

        Returns:
            String value of ssid.
        """
        return self._get_current_wifi_info().get("SSID", "")

    def get_current_rssi(self) -> t.Optional[str]:
        """Obtain rssi of current connected ssid.

        Returns:
            String value of rssi.
        """
        return self._get_current_wifi_info().get("agrCtlRSSI")

    def connect(self, ssid: str, password: str) -> WiFiState:
        """Connect a special wifi network.

        Args:
            ssid (str): The ssid for a special wifi network.
            password (str): The password for a special wifi network.

        Returns:
            True if connected successfully, otherwise False.
        """
        command = f"networksetup -setairportnetwork {self.interface} {ssid} {password}"
        self.execute_command(command=command)
        if self._get_state() != "running" or self.get_current_ssid() != ssid:
            return WiFiState.CONNECTED_FAILED
        return WiFiState.CONNECTED

    def disconnect(self) -> t.Optional[WiFiState]:
        """Disconnected current wifi network.

        Returns:
            Wifi disconnected or None.
        """
        # command = f"sudo {self.AIRPORT_PATH} -z"
        return WiFiState.DISCONNECTED if self.turn_off() else None

    def _get_state(self) -> t.Optional[str]:
        return self._get_current_wifi_info().get("state")

    def turn_on(self) -> bool:
        """Turn on wifi interface.

        Returns:
            True or False
        """
        command = f"networksetup -setairportpower {self.interface} on"
        try:
            logger.debug(msg=f"Wlan interface {self.interface} will be on.")
            self.execute_command(command=command)
        except CommandException as e:
            return False
        return self.is_on_or_off() == WiFiState.ON

    def turn_off(self) -> bool:
        """Turn off wifi interface.

        Returns:
            True or False.
        """
        command = f"networksetup -setairportpower {self.interface} off"
        try:
            logger.debug(msg=f"Wlan interface {self.interface} will be off.")
            self.execute_command(command=command)
        except CommandException as e:
            return False
        return self.is_on_or_off() == WiFiState.OFF


class WindowsAdapter(WifiAdapter):
    """Adapter of Wi-Fi operation under Windows."""

    def __init__(self) -> None:
        super().__init__()


class LinuxAdapter(WifiAdapter):
    """Adapter of Wi-Fi operation under Linux."""

    def __init__(self) -> None:
        super().__init__()
