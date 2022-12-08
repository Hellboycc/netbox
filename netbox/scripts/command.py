import click  # type:ignore

from ..constant import WiFiState
from ..core import Netbox
from ..version import __version__


@click.group()
@click.version_option(version=__version__, help="Print version information and quit")
def cli():
    """A simple and flexible CLI tool for network testing"""
    pass


@cli.command()
def version():
    """Show the CLI tool version information"""
    click.echo(f"Current version is {__version__}")


@cli.group()
@click.pass_context
def wlan(ctx):
    """Manage wifi network"""
    ctx.obj = Netbox()


@wlan.command(help="Scan surround wifi network")
@click.option("--ssid", type=str, help="Name of wifi network", metavar="String")
@click.pass_obj
def scan(netbox: Netbox, ssid: str) -> None:
    if ssid is None:
        info = netbox.wifi_scan()
        click.echo(f"Surrounding wifi network:\n {info}")
        return
    if ssid in netbox.get_all_ssid():
        click.echo(f"Current ssid {ssid} exists.")
    else:
        click.echo(f"Current ssid {ssid} is not found.")


@wlan.command(help="Current wifi network information")
@click.pass_obj
def current(netbox):
    info = netbox.current_wifi_info
    click.echo(info)


@wlan.command(help="Connect a wifi network")
@click.argument("ssid")
@click.argument("password")
@click.option(
    "--retry", type=int, help="Number of wifi scan retries", metavar="Integer"
)
@click.pass_obj
def connect(netbox, ssid, password, retry):
    if retry is None:
        netbox.connect(ssid=ssid, password=password)
    else:
        netbox.connect(ssid=ssid, password=password, retry=retry)


@wlan.command(help="Disconnect current wifi network")
@click.pass_obj
def disconnect(netbox):
    current_ssid = netbox.ssid
    if netbox.disconnect() == WiFiState.DISCONNECTED:
        netbox.turn_on_wifi()
        print(f"Disconnect from {current_ssid} wifi network")
