import sqlite3
database = sqlite3.connect('projetReseau.db')
db = database.cursor()

# création de la table users
db.execute('''  CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
           ''')

#id : identifiant unique de chaque utilisateur
#username : nom de l'utilisateur unique pour faciliter la connexion au programme
#password : mdp qui devra être hashé avant l'insertion dans la bdd
#created_at : date de création de l'utilisateur


#création de la table découpes
db.execute('''  CREATE TABLE IF NOT EXISTS decoupes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                responsable_id INTEGER NOT NULL,
                base_ip TEXT NOT NULL,
                base_mask TEXT NOT NULL,
                mode TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(responsable_id) REFERENCES users(id)
            )
           ''')

#id : identifiant unique de la découpe
#name : nom de la découpe unique et choisi par l'utilisateur
#responsable_id : id de l'utilisateur qui à créé la découpe (seul lui peut y accéder)
#base_ip : adresse ip qui servira de base à la découpe
#base_mask : masque de sr qui servira à déterminer la taille du réseau
#mode : permet de déterminer le mode de la découpe classless ou classfull
#created_at : date de création de la découpe

#création de la table subnets
db.execute('''  CREATE TABLE IF NOT EXISTS subnets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decoupe_id INTEGER NOT NULL,
                network_ip TEXT NOT NULL,
                mask TEXT NOT NULL,
                first_host TEXT NOT NULL,
                last_host TEXT NOT NULL,
                broadcast TEXT NOT NULL,
                nb_ip INTEGER NOT NULL,
                FOREIGN KEY(decoupe_id) REFERENCES decoupes(id),
                UNIQUE(decoupe_id, network_ip)
            )
           ''')


#id : identifiant du sous-réseau
#decoupe_id : identifiant de la découpe à laquelle appartient de sr
#network_ip : adresse du sr
#mask : masque du sr
#first_host : première ip utilisable
#last_host : dernière ip utilisable
#broadcast : adresse de broadcast du sr
#nb_ip : nombre de d'ip utilisable que le sr contient
#pas besoin de mettre de ; car sqlite considère ce qu'il y a dans les () comme une seule instruction

