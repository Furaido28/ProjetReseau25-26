import ipaddress

class NetworkService:
    """
    Classe pour effectuer les calculs et vérifications réseau.
    """
    def __init__(self):
        # Ici, on peut initialiser des paramètres globaux si nécessaire
        # Par exemple des flags pour classless/classfull
        self.supported_modes = ["classless", "classfull"]