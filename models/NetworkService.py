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

    def get_classful_mask(self, ip: str):
        """
        Détermine la classe et le masque par défaut d'une adresse IP.
        """
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

    def calculate(self, ip, mask, isClassFull):
        """
        Calcule les informations réseau (adresse, broadcast, masque, etc.)
        en mode Classful ou Classless.
        """
        ip_class = None

        if isClassFull:
            # Déterminer masque par défaut
            ip_class, default_mask = self.get_classful_mask(ip)
            if ip_class in ("D", "E"):
                return "L'adresse IP n'est pas classable (classe D ou E)."

            if not mask:
                # Utilisation du masque par défaut
                mask = default_mask
            else:
                # Vérification de la cohérence du masque fourni
                default_prefix = IPNetwork(f"0.0.0.0/{default_mask}").prefixlen
                given_prefix = IPNetwork(f"0.0.0.0/{mask}").prefixlen
                if given_prefix < default_prefix:
                    return (f"Erreur : en classful, le masque ne peut pas être plus petit "
                            f"que celui de la classe (/{default_prefix}).")

        else:
            if not mask:
                raise ValueError("En mode classless, le masque doit être fourni.")

        # Création du réseau
        network = IPNetwork(f"{ip}/{mask}")

        # Résultats détaillés
        result = ""
        result += f"Mode : {'Classful' if isClassFull else 'Classless'}\n"
        if ip_class:
            result += f"Classe IP : {ip_class}\n"
        result += f"Adresse réseau : {network.network}\n"
        result += f"Adresse broadcast : {network.broadcast}\n"
        result += f"Masque : {network.netmask}\n"
        result += f"Préfixe : /{network.prefixlen}\n"
        result += f"Nombre total d'IP : {network.size}\n"

        if network.size > 2:
            result += f"Plage utilisable : {network.network + 1} → {network.broadcast - 1}\n"
        else:
            result += f"Aucune IP utilisable (réseau trop petit)\n"

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
            return True,IPAddress(int(network.first)+1), IPAddress(int(network.last)-2), None
        else:
            return False,IPAddress(int(network.first)+1), IPAddress(int(network.last)-2), None

    def compute_subnets_choice(self, ip_cidr: str, nb_sr: int = None, nb_ips: int = None) -> str:
        """
        Découpe un réseau soit en fonction du nombre de sous-réseaux, soit en fonction du nb d'IPs.
        Retourne un rapport texte détaillé.
        """
        net = IPNetwork(ip_cidr)
        result = f"Réseau de base : {net}\n"
        result += f"Masque : {net.netmask}  |  Taille : {net.size} adresses\n"
        result += "-" * 60 + "\n"

        subnets = []

        if nb_sr:  # Découpe en nb_sr sous-réseaux
            nb_bits_sup = (nb_sr - 1).bit_length()
            new_prefix = net.prefixlen + nb_bits_sup
            subnets = list(net.subnet(new_prefix))

        elif nb_ips:  # Découpe en fonction d’un nb d’IPs
            prefix = 32
            while 2 ** (32 - prefix) < nb_ips:
                prefix -= 1
            subnets = list(net.subnet(prefix))

        else:
            raise ValueError("Il faut préciser soit nb_sr, soit nb_ips.")

        for i, sr in enumerate(subnets, start=1):
            usable = max(sr.size - 2, 0) if sr.prefixlen <= 30 else 0
            first_host = sr.network + 1 if sr.prefixlen <= 30 and sr.size >= 4 else sr.network
            last_host = sr.broadcast - 1 if sr.prefixlen <= 30 and sr.size >= 4 else sr.broadcast

            result += f"SR{i} : {sr}\n"
            result += f"  - Adresse réseau : {sr.network}\n"
            result += f"  - Masque : {sr.netmask} (/{sr.prefixlen})\n"
            result += f"  - Première IP utilisable : {first_host}\n"
            result += f"  - Dernière IP utilisable : {last_host}\n"
            result += f"  - Adresse de broadcast : {sr.broadcast}\n"
            result += f"  - Nb total d’adresses : {sr.size} (dont {usable} utilisables)\n"
            result += "-" * 60 + "\n"

        return result