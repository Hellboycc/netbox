import json
import logging
import time
import typing as t

import ping3  # type:ignore

from . import logger
from .constant import WiFiState
from .helper import create_adapter, get_current_os_info
from .wifi import LinuxAdapter, MacAdapter, WifiAdapter, WindowsAdapter


class Netbox(object):
    """A class that contains commonly used network operation."""

    def __init__(self) -> None:
        self.ping = ping3.ping
        self._wifi_adapter: t.Optional[WifiAdapter] = create_adapter(
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
    def current_wifi_info(self) -> str:
        """Obtain current connected wifi information.

        Returns:
            Connected wifi information. For example: {'SSID': 'TP-Link001', 'agrCtlRSSI': "-30"}
        """
        info = {}
        ret = self._wifi_adapter.get_current_network()
        info.update(
            {
                "code": 0,
                "message": "",
                "data": {
                    "ssid": ret.get("SSID", ""),
                    "rssi": ret.get("agrCtlRSSI", ""),
                    "noise": ret.get("agrCtlNoise", ""),
                    "state": ret.get("state", ""),
                    "mode": ret.get("op mode", ""),
                    "tx_rate": ret.get("lastTxRate", ""),
                    "max_rate": ret.get("maxRate", ""),
                    "auth": ret.get("802.11 auth", ""),
                    "security": ret.get("link auth", ""),
                    "mcs": ret.get("MCS", ""),
                    "guard_interval": ret.get("guardInterval", ""),
                    "channel": ret.get("channel", ""),
                    "nss": ret.get("NSS", ""),
                },
            }
        )
        return json.dumps(info, indent=4)

    @property
    def ssid(self) -> t.Optional[str]:
        """Obtain ssid of current connected wifi.

        Returns:
            Connected wifi ssid. For example: Chinanet-test001
        """
        ssid = self._wifi_adapter.get_current_ssid()
        return ssid

    @property
    def rssi(self) -> t.Optional[str]:
        """Obtain the signal of currnet connected wifi.

        Returns:
            Connected wifi rssi. For example: -34
        """
        ret = self._wifi_adapter.get_current_rssi()
        # return json.dumps({"code": 0, "message": "", "data": {"ssid": ret}}, indent=4)
        return ret

    def connect(self, ssid: str, password: str, retry: int = 5) -> None:
        """Connect a special wifi network.

        Args:
            ssid: The ssid for a special wifi network.
            password: The password for a special wifi network.
            retry: Number of wifi scan retries.
        """
        # Determine whether the current wifi interface is available
        if self._wifi_adapter.is_on_or_off() == WiFiState.OFF:
            # If the wifi interface is not available, start the wifi interface
            if self._wifi_adapter.turn_on():
                time.sleep(2)
                return self._connect(ssid, password, retry=retry)
        else:
            logger.debug(
                msg=f"Wlan interface {self._wifi_adapter.interface} is working normally."
            )
            return self._connect(ssid, password, retry=retry)

    def disconnect(self) -> t.Optional[WiFiState]:
        """Disconnected current wifi network."""
        return self._wifi_adapter.disconnect()

    def turn_on_wifi(self) -> bool:
        """Enable wifi interface."""
        return self._wifi_adapter.turn_on()

    def turn_off_wifi(self) -> bool:
        """Disable wifi interface."""
        return self._wifi_adapter.turn_off()

    @property
    def wifi_state(self):
        """Obtain current wifi state.

        Returns:
            Current wifi state. For example: running
        """
        return self._wifi_adapter.get_state()

    def wifi_scan(self) -> str:
        """Obtain surrounding wifi network information.

        Returns:
            Wifi network information (ssid collection).
        """
        ret = self._wifi_adapter.get_networks()
        return json.dumps(
            {"code": 0, "message": "Scanning successfully.", "data": ret}, indent=4
        )

    def get_all_ssid(self):
        """Obtain a collection of available ssid.

        Returns:
            Collection of ssid. For example: ['test01', 'ChinaNet-test001', 'TP-Link1111']
        """
        return self._wifi_adapter.get_all_ssid()

    def _connect(self, ssid: str, password: str, retry: int) -> str:
        """Connect a special wifi network.

        Args:
            ssid: The ssid for a special wifi network.
            password: The password for a special wifi network.
            retry: Number of wifi scan retries
        """
        _retry = 1
        while _retry <= retry:
            rets = self._wifi_adapter.get_all_ssid()
            if ssid in rets:
                logger.info(msg=f"Scanning {_retry} times, SSID: {ssid} find already.")
                break
            else:
                logger.info(msg=f"Scanning {_retry} times, SSID: {ssid} not found.")
            _retry = _retry + 1
        else:
            return ""
        if (
            self._wifi_adapter.connect(ssid=ssid, password=password)
            == WiFiState.CONNECTED
        ):
            time.sleep(2)
            ret = self.check_host_state("jd.com")
            if ret:
                logger.info(
                    msg=f"SSID: {ssid} connected successfully, ping cost is: {ret:.2f}s"
                )
                return json.dumps(
                    {
                        "code": 0,
                        "message": "Connected successfully.",
                        "data": {
                            "state": WiFiState.CONNECTED.value,
                            "ssid": ssid,
                            "ping_time_cost": f"{ret:.2f}s",
                            "domain": "jd.com",
                        },
                    },
                    indent=4,
                )
            else:
                logger.info(msg="Network is unreachable, please check it first!")
                return json.dumps(
                    {
                        "code": 1000,
                        "message": "Network is unreachable, please check it first!",
                        "data": {
                            "state": WiFiState.CONNECTED.value,
                            "ssid": ssid,
                            "ping_time_cost": ret,
                            "domain": "jd.com",
                        },
                    },
                    indent=4,
                )
        else:
            logger.info(msg="Password or ssid verification failed.")
            return json.dumps(
                {
                    "code": 1,
                    "message": "Password or ssid verification failed.",
                    "data": {"state": WiFiState.CONNECTED_FAILED.value},
                },
                indent=4,
            )
