from netbox.netbox import get_current_os_info


def test_get_current_os_info():
    info = get_current_os_info()
    assert info in ["Linux", "Windows"]
