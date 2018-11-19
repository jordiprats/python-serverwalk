import serverwalk
import jsonpickle

hosts = serverwalk.getHosts()
serverwalk.getHostInfo(hosts)

print jsonpickle.encode(hosts)
