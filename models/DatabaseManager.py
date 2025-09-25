import sqlite3
from models.Decoupe import Decoupe
from models.Subnet import Subnet

class DatabaseManager:
    """
    Classe pour gérer les interactions avec la base de données.
    """
    def __init__(self, db_path="bdd/projetReseau.db"):
        # Connexion à la base
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # permet d'accéder aux colonnes par nom
        self.cursor = self.conn.cursor()