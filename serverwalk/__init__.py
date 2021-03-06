import salt.client.ssh.client

class Host:
    def __init__(self):
        self.os         = {
            'hostname': None,
            'fqdn': None,
            'encoding': None,
            'language': None,
            'uptime': None,
            'runlevel': None,
            'distro': None,
            'os_release': None,
            'os_family': None,
            'kernel': {
                'kernel_ver': None,
                'modules': [],
            }
        }
        self.memory     = {
            'free_mem': None,
            'used_mem': None,
            'total_mem': None,
            'free_swap': None,
            'total_swap': None,
            'used_swap': None,
        }
        self.storage = {
            'mountpoints': []
        }

# Filesystem              Size  Used Avail Use% Mounted on
# /dev/sda1 on /boot type xfs (rw,relatime,seclabel,attr2,inode64,noquota)
class StorageMountpoint:
    def __init__(self):
        self.device = None
        self.mount = None
        self.fstype = None
        self.opts = None
        self.size = {
            'total': None,
            'used': None,
            'available': None,
            'percent_use': None,
        }


def getHosts():
    ssh = salt.client.ssh.client.SSHClient()
    # {u'demo': {u'fun_args': [], u'jid': u'20181119112056216471', u'return': True, u'retcode': 0, u'fun': u'test.ping', u'id': u'demo'}}
    salt_results = ssh.cmd('*', 'test.ping')
    hosts_alive = {}
    for salt_host in salt_results:
        if salt_results[salt_host]['return']:
            host = Host()
            host.hostname = salt_host
            hosts_alive[salt_host] = host
    return hosts_alive

def getHostInfo(hosts):
    ssh = salt.client.ssh.client.SSHClient()

    #
    # OS
    #

    # kernel ver
    salt_results = ssh.cmd('*', 'cmd.run', ['uname -r'])
    # {u'fun_args': [u'uname -r'], u'jid': u'20181119114756115168', u'return': u'4.4.0-139-generic', u'retcode': 0, u'fun': u'cmd.run', u'id': u'demo2'}
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os['kernel']['kernel_ver'] = salt_results[salt_host]['return']

    # kernel modules
    salt_results = ssh.cmd('*', 'cmd.run', ['lsmod | awk \'{ print $1 }\''])
    # {u'fun_args': [u'uname -r'], u'jid': u'20181119114756115168', u'return': u'4.4.0-139-generic', u'retcode': 0, u'fun': u'cmd.run', u'id': u'demo2'}
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os['kernel']['kernel.modules'] = salt_results[salt_host]['return'].split()[1:]

    #uptime
    salt_results = ssh.cmd('*', 'cmd.run', ['cat /proc/uptime'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os['uptime'] = salt_results[salt_host]['return'].split(' ')[0]

    #runlevel
    salt_results = ssh.cmd('*', 'cmd.run', ['runlevel'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os['runlevel'] = salt_results[salt_host]['return'].split(' ')[1]

    # os family
    salt_results = ssh.cmd('*', 'grains.get', ['os_family'])
    for salt_host in salt_results:
        hosts[salt_host].os['os_family'] = salt_results[salt_host]['return']

    # os
    salt_results = ssh.cmd('*', 'grains.get', ['os'])
    for salt_host in salt_results:
        hosts[salt_host].os['distro'] = salt_results[salt_host]['return']

    # os release
    salt_results = ssh.cmd('*', 'grains.get', ['osrelease'])
    for salt_host in salt_results:
        hosts[salt_host].os['os_release'] = salt_results[salt_host]['return']

    # fqdn
    salt_results = ssh.cmd('*', 'grains.get', ['fqdn'])
    for salt_host in salt_results:
        hosts[salt_host].os['fqdn'] = salt_results[salt_host]['return']

    # locale
    salt_results = ssh.cmd('*', 'grains.get', ['locale_info'])
    for salt_host in salt_results:
        hosts[salt_host].os['encoding'] = salt_results[salt_host]['return']['defaultencoding']
        hosts[salt_host].os['language'] = salt_results[salt_host]['return']['defaultlanguage']

    #
    # MEM
    #

    # total_mem
    salt_results = ssh.cmd('*', 'grains.get', ['mem_total'])
    for salt_host in salt_results:
        hosts[salt_host].memory['total_mem'] = salt_results[salt_host]['return']

    #used_mem
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Mem: | awk \'{ print $3 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory['used_mem'] = salt_results[salt_host]['return']

    #free_mem
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Mem: | awk \'{ print $4 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory['free_mem'] = salt_results[salt_host]['return']

    # total_swap
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Swap: | awk \'{ print $2 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory['total_swap'] = salt_results[salt_host]['return']

    #used_swap
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Swap: | awk \'{ print $3 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory['used_swap'] = salt_results[salt_host]['return']

    #total_swap
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Swap: | awk \'{ print $4 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory['free_swap'] = salt_results[salt_host]['return']

    #
    # storage - mounts
    #

    salt_results = ssh.cmd('*', 'cmd.run', ['mount'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            mounts = salt_results[salt_host]['return'].splitlines()
            for mount in mounts:
                items = mount.split(' ')
                storagemount = StorageMountpoint()
                storagemount.device = items[0]
                storagemount.mount = items[2]
                storagemount.fstype = items[4]
                storagemount.opts = items[5]
                hosts[salt_host].storage['mountpoints'].append(storagemount)

    salt_results = ssh.cmd('*', 'cmd.run', ['df -hP'])
    for salt_host in salt_results:

    #next((x for x in test_list if x.value == value), None)
