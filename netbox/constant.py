from enum import Enum


class WiFiState(Enum):
    """Enumeration class for wireless status."""

    CONNECTED = 1
    DISCONNECTED = 2
    ON = 3
    OFF = 4
    CONNECTED_FAILED = 5


class NetworkState(Enum):
    """Enumeration class for network status."""

    OK = 1
