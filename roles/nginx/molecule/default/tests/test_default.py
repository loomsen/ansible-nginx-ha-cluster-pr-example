import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize('file, content, mode, owner, group', [
    ('/etc/systemd/system/nginx.service.d/override.conf',
        '', 0o0644, 'root', 'root')
])
def test_files_created(host, file, mode, owner, group, content):
    afile = host.file(file)
    assert afile.exists
    assert afile.mode == mode
    assert afile.user == owner
    assert afile.group == group
    if content != '':
        assert afile.contains(content)
