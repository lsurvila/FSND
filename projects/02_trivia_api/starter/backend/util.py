from python_hosts import Hosts


def get_localhost_address():
    name = 'localhost'
    hosts = Hosts().find_all_matching(name=name)
    return hosts[0].address if hosts else name
