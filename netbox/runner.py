from .core import Netbox


def running():
    netbox = Netbox()
    print("Start wifi connnection test")
    for _ in range(10):
        netbox.connect(ssid="001Hellboy-5", password="12345678")
        print()


if __name__ == "__main__":
    running()
