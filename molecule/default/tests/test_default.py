"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution in ["amzn", "fedora"]:
        pkgs = ["tigervnc-server"]
    elif distribution in ["debian", "kali", "ubuntu"]:
        pkgs = ["tigervnc-standalone-server", "tigervnc-common"]
    else:
        # We don't support this distribution
        assert False, f"Unsupported distribution {distribution}"
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


@pytest.mark.parametrize(
    "f",
    [
        "/home/vnc/.config/autostart/light-locker.desktop",
        "/home/vnc/.config/autostart/xfce4-power-manager-disable-dpms.desktop",
        "/home/vnc/.config/autostart/xfce4-screensaver-disable.desktop",
        "/home/vnc/.config/autostart/xfce4-screensaver-disable-screen-locking.desktop",
    ],
)
def test_autostart_files_exist(host, f):
    """Test that the file exists."""
    assert host.file(f).exists
