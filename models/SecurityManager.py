import sqlite3
import bcrypt

class SecurityManager:
    """
    Classe pour gérer le mot de passe global du programme.
    """
    def __init__(self, db_path="../bdd/projetReseau.db"):
        # Connexion à la base
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_settings_table()

    def _init_settings_table(self):
        """Crée la table settings si elle n'existe pas."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def set_password(self, plain_password: str):
        """
        Définir ou modifier le mot de passe global du programme.
        Le mot de passe est haché avant d'être stocké.
        """
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        # On supprime l'ancien mot de passe (une seule ligne)
        self.cursor.execute("DELETE FROM settings")
        self.cursor.execute("INSERT INTO settings (id, password) VALUES (1, ?)", (hashed,))
        self.conn.commit()

    def verify_password(self, plain_password: str) -> bool:
        """
        Vérifie si le mot de passe saisi correspond au mot de passe global.
        Retourne True si correct, False sinon.
        """
        self.cursor.execute("SELECT password FROM settings WHERE id = 1")
        row = self.cursor.fetchone()
        if not row:
            return False  # Pas de mot de passe défini
        stored_hash = row["password"]
        return bcrypt.checkpw(plain_password.encode(), stored_hash)

    def close(self):
        """Fermer la connexion à la BDD."""
        self.conn.close()
