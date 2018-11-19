import salt.client.ssh.client

class Host:
    hostname = ""
    kernel = ""
    uptime = ""
    runlevel = ""
    os = ""
    os_release = ""


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
    # uname kernel
    salt_results = ssh.cmd('*', 'cmd.run', ['uname -r'])
    # {u'fun_args': [u'uname -r'], u'jid': u'20181119114756115168', u'return': u'4.4.0-139-generic', u'retcode': 0, u'fun': u'cmd.run', u'id': u'demo2'}
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].kernel = salt_results[salt_host]['return']

    #uptime
    salt_results = ssh.cmd('*', 'cmd.run', ['cat /proc/uptime'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].uptime = salt_results[salt_host]['return'].split(' ')[0]

    #runlevel
    salt_results = ssh.cmd('*', 'cmd.run', ['runlevel'])
    for salt_host in salt_results:
        if salt_results[salt_host]['retcode']==0:
            hosts[salt_host].runlevel = salt_results[salt_host]['return'].split(' ')[1]

    # os
    salt_results = ssh.cmd('*', 'grains.get', ['os'])
    for salt_host in salt_results:
        hosts[salt_host].os = salt_results[salt_host]['return']

    # os release
    salt_results = ssh.cmd('*', 'grains.get', ['osrelease'])
    for salt_host in salt_results:
        hosts[salt_host].os = salt_results[salt_host]['return']
