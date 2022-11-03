import ping3

from netbox.netbox import Netbox


def test_ping3_version_correct_or_not():
    assert ping3.__version__ >= "4.0.3"


def test_check_host_state_alive():
    netbox = Netbox()
    assert netbox.check_host_state("jd.com") is not None
    assert netbox.check_host_state("39.156.66.10") is not None


def test_check_host_status_not_alive():
    netbox = Netbox()
    assert netbox.check_host_state("not.example.com") is False
    assert netbox.check_host_state("3.3.3.3") is None
