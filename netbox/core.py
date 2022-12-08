import time
import typing as t

import ping3  # type:ignore

from .constant import WiFiState
from .helper import create_adapter, get_current_os_info
from .wifi import BaseAdapter, LinuxAdapter, MacAdapter, WindowsAdapter


class Netbox(object):
    """A class that contains commonly used network operation."""

    def __init__(self) -> None:
        self.ping = ping3.ping
        self._wifi_ctl: t.Optional[BaseAdapter] = create_adapter(
            name=get_current_os_info()
        )

    def check_host_state(
        self,
        host: str,
        src_addr: t.Optional[str] = None,
        interface: t.Optional[str] = None,
    ) -> float:
        """Check special host is alive or not.

        Args:
            host: IP address or domain.
            src_addr: Windows only, defaults to None.
            interface: Linux only, defaults to None.

        Returns:
            Time of ping successfully. For example: 0.07222890853881836
        """
        name = get_current_os_info()
        if name == "Windows":
            return self.ping(host=host, src_addr=src_addr)

        elif name == "Linux":
            return self.ping(host=host, interface=interface)
        else:
            return self.ping(host)

    @property
    def current_wifi_info(self) -> t.Dict[str, str]:
        """Obtain current connected wifi information.

        Returns:
            Connected wifi information. For example: {'SSID': 'TP-Link001', 'agrCtlRSSI': "-30"}
        """
        return self._wifi_ctl._get_current_wifi_info()

    @property
    def ssid(self) -> t.Optional[str]:
        """Obtain ssid of current connected wifi.

        Returns:
            Connected wifi ssid. For example: Chinanet-test001
        """
        return self._wifi_ctl.get_current_ssid()

    @property
    def rssi(self) -> t.Optional[str]:
        """Obtain the signal of currnet connected wifi.

        Returns:
            Connected wifi rssi. For example: -34
        """
        return self._wifi_ctl.get_current_rssi()

    def connect(self, ssid: str, password: str, retry: int = 5) -> None:
        """Connect a special wifi network.

        Args:
            ssid: The ssid for a special wifi network.
            password: The password for a special wifi network.
            retry: Number of wifi scan retries.
        """
        # Determine whether the current wifi interface is available
        if self._wifi_ctl.is_on_or_off() == WiFiState.OFF:
            # If the wifi interface is not available, start the wifi interface
            if self._wifi_ctl.turn_on():
                time.sleep(2)
                self._connect(ssid, password, retry=retry)
        else:
            print(f"Wifi interface {self._wifi_ctl.interface} is working normally.")
            self._connect(ssid, password, retry=retry)

    def disconnect(self) -> t.Optional[WiFiState]:
        """Disconnected current wifi network."""
        return self._wifi_ctl.disconnect()

    def turn_on_wifi(self) -> bool:
        """Enable wifi interface."""
        return self._wifi_ctl.turn_on()

    def turn_off_wifi(self) -> bool:
        """Disable wifi interface."""
        return self._wifi_ctl.turn_off()

    @property
    def wifi_state(self):
        """Obtain current wifi state.

        Returns:
            Current wifi state. For example: running
        """
        return self._wifi_ctl.get_state()

    def wifi_scan(self):
        """Obtain surrounding wifi network information.

        Returns:
            Wifi network information (ssid collection).
        """
        return self._wifi_ctl.get_scan_results()

    def get_all_ssid(self):
        """Obtain a collection of available ssid.

        Returns:
            Collection of ssid. For example: ['test01', 'ChinaNet-test001', 'TP-Link1111']
        """
        return self._wifi_ctl.get_all_ssid()

    def _connect(self, ssid: str, password: str, retry: int) -> None:
        """Connect a special wifi network.

        Args:
            ssid: The ssid for a special wifi network.
            password: The password for a special wifi network.
            retry: Number of wifi scan retries
        """
        _retry = 1
        while _retry <= retry:
            # print(f"Sanning count: {_retry}")
            results = self._wifi_ctl.get_all_ssid()
            if ssid in results:
                print(f"[Scanning count = {_retry}] ==> SSID: {ssid} find already.")
                break
            else:
                print(f"[Scanning count = {_retry}] ==> SSID: {ssid} not found.")
            _retry = _retry + 1
        else:
            return None
        if self._wifi_ctl.connect(ssid=ssid, password=password) == WiFiState.CONNECTED:
            time.sleep(2)
            result = self.check_host_state("jd.com")
            if result:
                print(
                    f"SSID: {ssid} connected successfully, ping cost time is: {result:.2f}s"
                )
            else:
                print("Network is unreachable, please check it first!")
        else:
            print(f"Password or ssid verification failed.")
