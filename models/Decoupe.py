from itertools import count

class Decoupe:
    _id_counter = count(1)

    def __init__(self, name, base_ip, base_mask, wanted, mode="classless", responsable_name=None):
        new_id = next(self._id_counter)

        # Compat id/decoupe_id
        self.id = new_id
        self.decoupe_id = new_id
        self._decoupe_id = new_id  # <-- pour get_decoupe_id()

        # Attributs privés attendus par tes getters
        self._name = name
        self._base_ip = base_ip
        self._base_mask = base_mask
        self._wanted = int(wanted)
        self._mode = mode
        self._responsable_name = responsable_name

    """
        Getters
    """
    def get_decoupe_id(self):
        return self._decoupe_id

    def get_name(self):
        return self._name

    def get_responsable_name(self):
        return self._responsable_name

    def get_base_ip(self):
        return self._base_ip

    def get_base_mask(self):
        return self._base_mask

    def get_mode(self):
        return self._mode

    def get_wanted(self):
        return self._wanted