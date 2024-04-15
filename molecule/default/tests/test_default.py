"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
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
