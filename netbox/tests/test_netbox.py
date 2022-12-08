import ping3  # type:ignore

import netbox

from ..version import __version__


def test_main_version() -> None:
    assert netbox.__version__ == __version__


def test_ping3_version_correct_or_not() -> None:
    assert ping3.__version__ >= "4.0.3"


# def test_check_host_state_alive():
#     netbox = Netbox()
#     assert netbox.check_host_state("jd.com") is not None
#     assert netbox.check_host_state("39.156.66.10") is not None


# def test_check_host_status_not_alive():
#     netbox = Netbox()
#     assert netbox.check_host_state("not.example.com") is False
#     assert netbox.check_host_state("3.3.3.3") is None


# def test_get_connected_wifi_info():
#     netbox = Netbox()
#     assert netbox.ssid == "001Hellboy-5"
