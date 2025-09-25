class Decoupe:
    def __init__(self, decoupe_id, name, responsable_name, base_ip, base_mask, mode):
        self._decoupe_id = decoupe_id
        self._name = name
        self._responsable_name = responsable_name
        self._base_ip = base_ip
        self._base_mask = base_mask
        self._mode = mode