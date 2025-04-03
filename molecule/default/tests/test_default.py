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


def test_systemd_service_enabled(host):
    """Test that the VNC systemd service is valid and enabled."""
    service = host.service("vncserver@1")
    # TODO: Something funky happens on Ubuntu 22.04.  is_valid is false for
    # reasons unrelated to the systemd service we put in place.  See #57 for
    # more details.
    if (
        host.system_info.distribution != "ubuntu"
        or host.system_info.codename != "jammy"
    ):
        assert service.is_valid
    assert service.is_enabled
    assert not service.is_masked


def test_vnc_user(host):
    """Test that the VNC user was created."""
    user = host.user("vnc")
    assert user.exists
    assert user.shell == "/bin/bash"


def test_vnc_user_config(host):
    """Test that config files for the VNC user were created."""
    # Test that the ~vnc/.vnc directory was created.
    f = host.file("/home/vnc/.vnc")
    assert f.exists
    assert f.is_directory
    assert f.user == "vnc"
    assert f.group == "vnc"
    assert f.mode == 0o755

    # Test that the ~vnc/.vnc/passwd file was created.
    f = host.file("/home/vnc/.vnc/passwd")
    assert f.exists
    assert f.is_file
    assert f.user == "vnc"
    assert f.group == "vnc"
    assert f.mode == 0o600

    # Test that the ~vnc/.ssh directory was created.
    f = host.file("/home/vnc/.ssh")
    assert f.exists
    assert f.is_directory
    assert f.user == "vnc"
    assert f.group == "vnc"
    assert f.mode == 0o755
