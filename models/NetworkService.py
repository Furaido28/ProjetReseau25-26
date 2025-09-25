# NetworkService.py
from netaddr import IPNetwork
import math

class NetworkService:
    """
    Classe pour effectuer les calculs et vérifications réseau.
    """
    def __init__(self):
        self.supported_modes = ["classless", "classfull"]

    def prefix_for_usable_hosts(self, usable_hosts: int) -> int:
        """
        Retourne le préfixe (p) tel que 2^(32-p) - 2 >= usable_hosts,
        borné à /30 minimum pour garder >=2 hôtes utilisables.
        """
        if usable_hosts < 1:
            raise ValueError("Le nombre d’IP souhaité doit être >= 1.")
        h = math.ceil(math.log2(usable_hosts + 2))
        p = 32 - h
        if p > 30:
            p = 30
        if p < 0:
            p = 0
        return p

    def compute_subnets(self, ip: str, mask: str, wanted_hosts: int) -> str:
        """
        Retourne un rapport texte avec la découpe réseau.
        """
        ip_cidr = f"{ip}/{mask}"
        result = ""

        net = IPNetwork(ip_cidr)
        new_prefix = self.prefix_for_usable_hosts(wanted_hosts)

        if new_prefix < net.prefixlen:
            return (
                "Erreur : Le besoin en IP par sous-réseau est trop grand pour le réseau de base.\n"
                f"Réseau de base : {net.cidr} → préfixe {net.prefixlen}\n"
                f"Besoins → suggère au moins /{new_prefix}, ce qui est plus large que /{net.prefixlen}.\n"
                "Réduis le nombre d’IP souhaité, ou choisis un réseau de base plus grand.\n"
            )

        result += f"Découpe en /{new_prefix} (≥ {wanted_hosts} hôtes utilisables) :\n"
        subs = list(net.subnet(new_prefix))
        result += f"Nombre de sous-réseaux : {len(subs)}\n\n"

        for s in subs:
            s_net = IPNetwork(str(s))
            usable = max(s_net.size - 2, 0) if s_net.prefixlen <= 30 else 0
            first_host = s_net.network + 1 if s_net.prefixlen <= 30 and s_net.size >= 4 else s_net.network
            last_host = s_net.broadcast - 1 if s_net.prefixlen <= 30 and s_net.size >= 4 else s_net.broadcast

            result += f"- {s_net.cidr}\n"
            result += f"    réseau    : {s_net.network}\n"
            result += f"    masque    : {s_net.netmask} (/ {s_net.prefixlen})\n"
            result += f"    broadcast : {s_net.broadcast}\n"
            result += f"    IP totales: {s_net.size} | hôtes utilisables: {usable}\n"
            result += f"    1er hôte  : {first_host} | Dernier hôte : {last_host}\n"

        return result