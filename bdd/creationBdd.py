import sqlite3

# Connexion à la base
database = sqlite3.connect('projetReseau.db')
db = database.cursor()

# -----------------------------
# Table settings : mot de passe global
# -----------------------------
db.execute('''
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# -----------------------------
# Table decoupes : plans réseau
# -----------------------------
db.execute('''
CREATE TABLE IF NOT EXISTS decoupes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    responsable TEXT NOT NULL,
    base_ip TEXT NOT NULL,
    base_mask TEXT NOT NULL,
    mode TEXT NOT NULL,
    value INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Index utile : rechercher les découpes par responsable
db.execute('''
CREATE INDEX IF NOT EXISTS idx_decoupes_responsable ON decoupes(responsable)
''')

# Commit et fermeture
database.commit()
database.close()

