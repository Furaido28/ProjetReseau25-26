class Subnet:
    def __init__(self, network_ip, mask, first, last, broadcast, nb_ip):
        self._network_ip = network_ip
        self._mask = mask
        self._first = first
        self._last = last
        self._broadcast = broadcast
        self._nb_ip = nb_ip