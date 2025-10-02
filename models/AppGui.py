import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox
from models.SecurityManager import SecurityManager
from models.NetworkService import NetworkService
#test
# Services
security = SecurityManager("bdd/projetReseau.db")
network_service = NetworkService()


# ------------------ UTILS ------------------
def clear_root(root):
    """Efface tout le contenu de la fenêtre."""
    for widget in root.winfo_children():
        widget.destroy()


# ------------------ PAGE CREATION MOT DE PASSE ------------------
def page_creer_mdp(root):
    clear_root(root)

    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit")
            return
        security.set_password(pwd)
        messagebox.showinfo("Succès", "Mot de passe enregistré !")
        clear_root(root)
        page_connexion(root)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Créer un mot de passe", font=("Arial", 22, "bold")).pack(pady=(10, 15))

    entry_password = ctk.CTkEntry(frame, placeholder_text="Nouveau mot de passe", show="*", height=30)
    entry_password.pack(pady=10, padx=40, fill="x")

    ctk.CTkButton(frame, text="Enregistrer", command=save_password, height=40, corner_radius=10).pack(
        pady=15, padx=40, fill="x"
    )


# ------------------ PAGE CONNEXION ------------------
def page_connexion(root):
    clear_root(root)

    def login():
        user = entry_user.get()
        pwd = entry_password.get()
        if security.verify_password(pwd):
            messagebox.showinfo("Succès", f"Bienvenue {user} !")
            clear_root(root)
            page_menu(root)
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Connectez-vous", font=("Arial", 22, "bold")).pack(pady=(10, 20))

    entry_user = ctk.CTkEntry(frame, placeholder_text="Utilisateur", height=30)
    entry_user.pack(pady=8, padx=40, fill="x")

    entry_password = ctk.CTkEntry(frame, placeholder_text="Mot de passe", show="*", height=30)
    entry_password.pack(pady=8, padx=40, fill="x")

    ctk.CTkButton(frame, text="Connexion", command=login, height=40, corner_radius=10).pack(
        pady=20, padx=40, fill="x"
    )

    # Lier la touche Entrée pour valider
    root.bind("<Return>", lambda event: login())


# ------------------ PAGE MENU ------------------
def page_menu(root):
    clear_root(root)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Menu principal", font=("Arial", 22, "bold")).pack(pady=20)

    ctk.CTkButton(frame, text="Calcul adresse réseau", command=lambda: page_adresse_reseau(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)
    ctk.CTkButton(frame, text="Découpe en sous-réseaux", command=lambda: page_calcul_reseau(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)
    ctk.CTkButton(frame, text="Vérification d'une adresse IP", command=lambda: page_verif_ip_reseau(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)
    ctk.CTkButton(frame, text="Découpe par nb SR ou nb IP", command=lambda: page_decoupe_mode(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)


# ------------------ PAGE VERIF IP DANS UN RESEAU ------------------
def page_verif_ip_reseau(root):
    clear_root(root)

    def verifier():
        ip = entry_ip.get().strip()
        network_ip = entry_network_ip.get().strip()
        network_mask = entry_network_mask.get().strip()

        if not ip or not network_ip or not network_mask:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        result, first, last, error = network_service.define_ip_in_network(ip, network_ip, network_mask)

        text_result.delete("1.0", "end")

        if error:
            text_result.insert("end", f"Erreur : {error}")
        elif result:
            text_result.insert("end", f"L'adresse IP {ip} appartient au réseau {network_ip}/{network_mask}\n")
            text_result.insert("end", f"Plage d'IP du réseau : {first} → {last}")
        else:
            text_result.insert("end", f"L'adresse IP {ip} n'appartient pas au réseau {network_ip}/{network_mask}")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Vérification IP dans un réseau", font=("Arial", 22, "bold")).pack(pady=(10, 15))

    # Ligne IP à tester
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row1, text="IP à tester").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.1.42", height=30)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Ligne IP réseau
    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row2, text="IP réseau").grid(row=0, column=0, padx=(0, 6))
    entry_network_ip = ctk.CTkEntry(row2, placeholder_text="ex: 192.168.1.0", height=30)
    entry_network_ip.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Ligne masque
    row3 = ctk.CTkFrame(frame)
    row3.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row3, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_network_mask = ctk.CTkEntry(row3, placeholder_text="ex: 24 ou 255.255.255.0", height=30)
    entry_network_mask.grid(row=0, column=1, sticky="ew")
    row3.grid_columnconfigure(1, weight=1)

    ctk.CTkButton(frame, text="Vérifier", command=verifier, height=40, corner_radius=10).pack(
        pady=10, fill="x", padx=40
    )

    text_result = ctk.CTkTextbox(frame)
    text_result.pack(pady=6, expand=True, fill="both", padx=20)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root), height=40, corner_radius=10).pack(
        pady=8, fill="x", padx=40
    )


# ------------------ PAGE CALCUL RESEAU (SUBNETTING) ------------------
def page_calcul_reseau(root):
    clear_root(root)

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        wanted = entry_wanted.get().strip()

        if not ip or not mask or not wanted:
            messagebox.showerror("Erreur", "IP, Masque et Nombre d’IP sont obligatoires.")
            return
        if not wanted.isdigit():
            messagebox.showerror("Erreur", "Le nombre d’IP souhaité doit être un entier positif.")
            return

        try:
            result = network_service.compute_subnets(ip, mask, int(wanted))
            text_result.delete("1.0", "end")
            text_result.insert("end", result)
        except Exception as e:
            text_result.delete("1.0", "end")
            text_result.insert("end", f"Erreur : {e}")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Découpe de réseau", font=("Arial", 22, "bold")).pack(pady=(10, 15))

    # Ligne 1 : IP + Masque
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row1, text="IP").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.1.10", height=30)
    entry_ip.grid(row=0, column=1, padx=(0, 12))
    ctk.CTkLabel(row1, text="Masque").grid(row=0, column=2, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row1, placeholder_text="ex: 24 ou 255.255.255.0", height=30)
    entry_mask.grid(row=0, column=3)

    # Ligne 2 : Nombre d'IP souhaité
    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row2, text="Nombre d’IP souhaité / sous-réseau").grid(row=0, column=0, padx=(0, 8))
    entry_wanted = ctk.CTkEntry(row2, placeholder_text="ex: 50", height=30)
    entry_wanted.grid(row=0, column=1)

    ctk.CTkButton(frame, text="Calculer", command=calculer, height=40, corner_radius=10).pack(
        pady=10, padx=40, fill="x"
    )

    text_result = ctk.CTkTextbox(frame)
    text_result.pack(pady=6, expand=True, fill="both", padx=20)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root), height=40, corner_radius=10).pack(
        pady=8, fill="x", padx=40
    )


# ------------------ PAGE CALCUL ADRESSE RESEAU ------------------
def page_adresse_reseau(root):
    clear_root(root)

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode = var_mode.get()

        if not ip:
            messagebox.showerror("Erreur", "L'adresse IP est obligatoire.")
            return
        if mode == "classless" and not mask:
            messagebox.showerror("Erreur", "En mode classless, le masque est obligatoire.")
            return

        try:
            is_classful = (mode == "classful")
            result = network_service.calculate(ip, mask if not is_classful else None, is_classful)
            text_result.delete("1.0", "end")
            text_result.insert("end", result)
        except Exception as e:
            text_result.delete("1.0", "end")
            text_result.insert("end", f"Erreur : {e}")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Calcul adresse réseau", font=("Arial", 22, "bold")).pack(pady=(10, 15))

    # Ligne 1 : IP
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row1, text="IP").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.1.42", height=30)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Ligne 2 : Masque
    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: 24 ou 255.255.255.0", height=30)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Ligne 3 : Choix Classful / Classless
    row3 = ctk.CTkFrame(frame)
    row3.pack(pady=6, fill="x", padx=20)
    var_mode = ctk.StringVar(value="classless")
    ctk.CTkRadioButton(row3, text="Classless (CIDR)", variable=var_mode, value="classless").grid(row=0, column=0, padx=10)
    ctk.CTkRadioButton(row3, text="Classful", variable=var_mode, value="classful").grid(row=0, column=1, padx=10)

    ctk.CTkButton(frame, text="Calculer", command=calculer, height=40, corner_radius=10).pack(
        pady=10, padx=40, fill="x"
    )

    text_result = ctk.CTkTextbox(frame)
    text_result.pack(pady=6, expand=True, fill="both", padx=20)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root), height=40, corner_radius=10).pack(
        pady=8, fill="x", padx=40
    )

# ------------------ PAGE CALCUL ADRESSE RESEAU ------------------

def page_decoupe_mode(root):
    clear_root(root)

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode = var_mode.get()

        if not ip or not mask or not val:
            messagebox.showerror("Erreur", "IP, Masque et Valeur sont obligatoires.")
            return

        try:
            val = int(val)
            if val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "La valeur doit être un entier positif.")
            return

        try:
            ip_cidr = f"{ip}/{mask}"
            if mode == "nb_sr":
                report = network_service.compute_subnets_choice(ip_cidr, nb_sr=val)
            else:
                report = network_service.compute_subnets_choice(ip_cidr, nb_ips=val)

            # Nettoyer le tableau avant de recharger
            for item in tree.get_children():
                tree.delete(item)

            # Parser le rapport texte
            lines = [l for l in report.splitlines() if l and not l.startswith("---")]
            sr, net, mask_val, first, last, bc, nb = [""]*7
            for l in lines:
                if l.startswith("SR"):
                    if sr:  # sauvegarde ligne précédente
                        tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))
                    sr = l.split(":")[0]
                elif "Adresse réseau" in l:
                    net = l.split(":")[1].strip()
                elif "Masque" in l:
                    mask_val = l.split(":")[1].strip()
                elif "Première" in l:
                    first = l.split(":")[1].strip()
                elif "Dernière" in l:
                    last = l.split(":")[1].strip()
                elif "broadcast" in l:
                    bc = l.split(":")[1].strip()
                elif "Nb total" in l:
                    nb = l.split(":")[1].strip()
            # insérer la dernière ligne
            if sr:
                tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Découpe réseau (Point 4)", font=("Arial", 20, "bold")).pack(pady=15)

    # Ligne IP réseau
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row1, text="IP réseau").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.0.0", height=30)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Ligne Masque
    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: 24 ou 255.255.255.0", height=30)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Choix du mode
    var_mode = ctk.StringVar(value="nb_ips")
    row3 = ctk.CTkFrame(frame)
    row3.pack(pady=6)
    ctk.CTkRadioButton(row3, text="Par nombre d'IPs / SR", variable=var_mode, value="nb_ips").pack(side="left", padx=8)
    ctk.CTkRadioButton(row3, text="Par nombre de sous-réseaux", variable=var_mode, value="nb_sr").pack(side="left", padx=8)

    # Champ valeur
    row4 = ctk.CTkFrame(frame)
    row4.pack(pady=6, fill="x", padx=20)
    ctk.CTkLabel(row4, text="Valeur").grid(row=0, column=0, padx=(0, 6))
    entry_value = ctk.CTkEntry(row4, placeholder_text="ex: 8", height=30)
    entry_value.grid(row=0, column=1, sticky="ew")
    row4.grid_columnconfigure(1, weight=1)

    # Tableau des résultats
    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=10, pady=10)

    columns = ("SR", "Réseau", "Masque", "1ère IP", "Dernière IP", "Broadcast", "Nb IPs")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=12)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Boutons
    ctk.CTkButton(frame, text="Calculer", command=calculer, height=40).pack(pady=10, fill="x", padx=40)
    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root), height=40).pack(pady=8, fill="x", padx=40)
