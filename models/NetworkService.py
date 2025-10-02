# NetworkService.py
from netaddr import IPNetwork, IPAddress, AddrFormatError
import math
#test
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

    def get_classful_mask(self,ip: str):
        first_octet = int(ip.split(".")[0])

        if 1 <= first_octet <= 126:
            return "A", "255.0.0.0"
        elif 128 <= first_octet <= 191:
            return "B", "255.255.0.0"
        elif 192 <= first_octet <= 223:
            return "C", "255.255.255.0"
        elif 224 <= first_octet <= 239:
            return "D", None  # Multicast
        elif 240 <= first_octet <= 255:
            return "E", None  # Expérimental
        else:
            raise ValueError("Adresse IP invalide ou non classable.")




    def calculate(self,ip, mask, isClassFull):
        combined_string =""
        if(isClassFull):
            mask=""
            ip_class, mask = self.get_classful_mask(ip)
            if(ip_class == "D" or ip_class == "E"):
                return "l'adresse IP n'est pas classable"
            else:
                combined_string += ip+"/"+mask
        else:
            if mask is None:
                raise ValueError("En mode classless, le masque doit être fourni.")
            combined_string += ip+"/"+mask

        network = IPNetwork(combined_string)

        result = ""
        result += f"Adresse réseau : {network.network}\n"
        result += f"Adresse broadcast : {network.broadcast}\n"

        return result


    def define_ip_in_network(self, ip, network_ip, network_mask):
        try:
            network = IPNetwork(f"{network_ip}/{network_mask}")
        except AddrFormatError:
            return False, None, None, "Adresse réseau ou masque invalide"

        try:
            ip_obj = IPAddress(ip)
        except AddrFormatError:
            return False, None, None, "Adresse IP invalide"

        if ip_obj in network:
            return True,IPAddress(network.first), IPAddress(network.last), None
        else:
            return False, IPAddress(network.first), IPAddress(network.last), None

