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

# -----------------------------
# Table subnets : sous-réseaux
# -----------------------------
db.execute('''
CREATE TABLE IF NOT EXISTS subnets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decoupe_id INTEGER NOT NULL,
    network_ip TEXT NOT NULL,
    mask TEXT NOT NULL,
    first_host TEXT NOT NULL,
    last_host TEXT NOT NULL,
    broadcast TEXT NOT NULL,
    nb_ip INTEGER NOT NULL,
    FOREIGN KEY(decoupe_id) REFERENCES decoupes(id) ON DELETE CASCADE,
    UNIQUE(decoupe_id, network_ip)
)
''')

# Index utile : rechercher rapidement tous les subnets d'une découpe
db.execute('''
CREATE INDEX IF NOT EXISTS idx_subnets_decoupe ON subnets(decoupe_id)
''')

# Commit et fermeture
database.commit()
database.close()

