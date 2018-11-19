import salt.client.ssh.client

ssh = salt.client.ssh.client.SSHClient()
ssh.cmd('*', 'test.ping')
