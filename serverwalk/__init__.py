import salt.client.ssh.client

class Host:
    def __init__(self):
        self.os         = OS()
        self.memory     = HostMemory()

class HostMemory:
    def __init__(self):
        self.free_mem = None
        self.used_mem = None
        self.total_mem = None
        self.free_swap = None
        self.used_swap = None
        self.total_swap = None

class OS:
    def __init__(self):
        self.hostname   = None
        self.fqdn       = None
        self.encoding   = None
        self.language   = None
        self.uptime     = None
        self.runlevel   = None
        self.distro     = None
        self.os_release = None
        self.os_family  = None
        self.kernel     = OSKernel()

class OSKernel:
    def __init__(self):
        self.kernel_ver = None
        self.modules = []

class Storage:
    def __init__(self):
        self.mountpoints  = []

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
            hosts[salt_host].os.kernel.kernel_ver = salt_results[salt_host]['return']

    # kernel modules
    salt_results = ssh.cmd('*', 'cmd.run', ['lsmod | awk \'{ print $1 }\''])
    # {u'fun_args': [u'uname -r'], u'jid': u'20181119114756115168', u'return': u'4.4.0-139-generic', u'retcode': 0, u'fun': u'cmd.run', u'id': u'demo2'}
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os.kernel.modules = salt_results[salt_host]['return'].split()[1:]

    #uptime
    salt_results = ssh.cmd('*', 'cmd.run', ['cat /proc/uptime'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os.uptime = salt_results[salt_host]['return'].split(' ')[0]

    #runlevel
    salt_results = ssh.cmd('*', 'cmd.run', ['runlevel'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].os.runlevel = salt_results[salt_host]['return'].split(' ')[1]

    # os family
    salt_results = ssh.cmd('*', 'grains.get', ['os_family'])
    for salt_host in salt_results:
        hosts[salt_host].os.os_family = salt_results[salt_host]['return']

    # os
    salt_results = ssh.cmd('*', 'grains.get', ['os'])
    for salt_host in salt_results:
        hosts[salt_host].os.distro = salt_results[salt_host]['return']

    # os release
    salt_results = ssh.cmd('*', 'grains.get', ['osrelease'])
    for salt_host in salt_results:
        hosts[salt_host].os.os_release = salt_results[salt_host]['return']

    # fqdn
    salt_results = ssh.cmd('*', 'grains.get', ['fqdn'])
    for salt_host in salt_results:
        hosts[salt_host].os.fqdn = salt_results[salt_host]['return']

    # locale
    salt_results = ssh.cmd('*', 'grains.get', ['locale_info'])
    for salt_host in salt_results:
        hosts[salt_host].os.encoding = salt_results[salt_host]['return']['defaultencoding']
        hosts[salt_host].os.language = salt_results[salt_host]['return']['defaultlanguage']

    #
    # MEM
    #

    # total_mem
    salt_results = ssh.cmd('*', 'grains.get', ['mem_total'])
    for salt_host in salt_results:
        hosts[salt_host].memory.total_mem = salt_results[salt_host]['return']

    #used_mem
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Mem: | awk \'{ print $3 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory.used_mem = salt_results[salt_host]['return']

    #free_mem
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Mem: | awk \'{ print $4 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory.free_mem = salt_results[salt_host]['return']

    # total_swap
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Swap: | awk \'{ print $2 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory.total_swap = salt_results[salt_host]['return']

    #used_swap
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Swap: | awk \'{ print $3 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory.used_swap = salt_results[salt_host]['return']

    #total_swap
    salt_results = ssh.cmd('*', 'cmd.run', ['free -m | grep ^Swap: | awk \'{ print $4 }\''])
    for salt_host in salt_results:
        hosts[salt_host].memory.free_swap = salt_results[salt_host]['return']
