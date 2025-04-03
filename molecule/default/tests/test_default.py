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
        pkgs = ["desktop-file-utils", "tigervnc-server"]
    elif distribution in ["debian", "kali", "ubuntu"]:
        pkgs = ["desktop-file-utils", "tigervnc-standalone-server", "tigervnc-common"]
    else:
        # We don't support this distribution
        assert False, f"Unsupported distribution {distribution}"
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


def test_autostart_dir_exists(host):
    """Test that the directory exists and has the expected ownership and permissions."""
    f = host.file("/home/vnc/.config/autostart")
    assert f.exists
    assert f.is_directory
    assert f.user == "vnc"
    assert f.group == "vnc"
    assert f.mode == 0o755


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
    """Test that the file exists and has the expected ownership and permissions."""
    assert host.file(f).exists
    assert host.file(f).is_file
    assert host.file(f).user == "vnc"
    assert host.file(f).group == "vnc"
    assert host.file(f).mode == 0o644
