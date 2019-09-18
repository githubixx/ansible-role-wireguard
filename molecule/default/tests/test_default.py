import os
import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("pkg_name", [
    ("wireguard-tools"),
    ("wireguard-dkms"),
])
def test_is_wireguard_installed(host, pkg_name):
    pkg = host.package(pkg_name)

    assert pkg.is_installed


@pytest.mark.parametrize("private_ip", [
    ("10.8.0.101"),
    ("10.8.0.102"),
])
def test_is_vpn_connected(host, private_ip):
    assert host.addr(private_ip).is_reachable


def test_is_wireguard_running_and_enabled(host):
    assert host.service("wg-quick@wg0").is_running
    assert host.service("wg-quick@wg0").is_enabled
