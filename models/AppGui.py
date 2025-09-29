import customtkinter as ctk
from tkinter import messagebox
from models.SecurityManager import SecurityManager
from models.NetworkService import NetworkService

security = SecurityManager("bdd/projetReseau.db")
network_service = NetworkService()

def clear_root(root):
    for widget in root.winfo_children():
        widget.destroy()

def page_creer_mdp(root):
    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit")
            return
        security.set_password(pwd)
        messagebox.showinfo("Succès", "Mot de passe enregistré !")
        clear_root(root)
        page_connexion(root)

    frame = ctk.CTkFrame(root, corner_radius=15, width=320, height=200)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Créer un mot de passe", font=("Arial", 18, "bold")).pack(pady=15)
    entry_password = ctk.CTkEntry(frame, placeholder_text="Nouveau mot de passe", show="*", width=250)
    entry_password.pack(pady=10)
    ctk.CTkButton(frame, text="Enregistrer", command=save_password).pack(pady=15)

def page_connexion(root):
    def login():
        user = entry_user.get()
        pwd = entry_password.get()
        if security.verify_password(pwd):
            messagebox.showinfo("Succès", f"Bienvenue {user} !")
            clear_root(root)
            page_menu(root)
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")

    frame = ctk.CTkFrame(root, corner_radius=15, width=320, height=260)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Connectez-vous", font=("Arial", 20, "bold")).pack(pady=(20, 10))
    entry_user = ctk.CTkEntry(frame, placeholder_text="Utilisateur", width=250)
    entry_user.pack(pady=10)
    entry_password = ctk.CTkEntry(frame, placeholder_text="Mot de passe", show="*", width=250)
    entry_password.pack(pady=10)
    ctk.CTkButton(frame, text="Connexion", width=200, command=login).pack(pady=20)
    # <-- Lier Enter pour déclencher login
    root.bind("<Return>", lambda event: login())

def page_menu(root):
    frame = ctk.CTkFrame(root, corner_radius=15, width=400, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Menu principal", font=("Arial", 20, "bold")).pack(pady=20)
    ctk.CTkButton(frame, text="Calcul adresse réseau", command=lambda: page_adresse_reseau(root)).pack(pady=10)
    ctk.CTkButton(frame, text="Découpe en sous-réseaux", command=lambda: page_calcul_reseau(root)).pack(pady=10)
    ctk.CTkButton(frame, text="Vérifiication d'une adresse ip", command=lambda: page_verif_ip_reseau(root)).pack(pady=10)

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

    frame = ctk.CTkFrame(root, corner_radius=15, width=520, height=430)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Découpe de réseau", font=("Arial", 18, "bold")).pack(pady=(12, 6))

    # Ligne 1 : IP + Masque
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=6)
    ctk.CTkLabel(row1, text="IP").grid(row=0, column=0, padx=(0,6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.1.10", width=170)
    entry_ip.grid(row=0, column=1, padx=(0,12))

    ctk.CTkLabel(row1, text="Masque").grid(row=0, column=2, padx=(0,6))
    entry_mask = ctk.CTkEntry(row1, placeholder_text="ex: 24 ou 255.255.255.0", width=180)
    entry_mask.grid(row=0, column=3)

    # Ligne 2 : Nombre d'IP souhaité
    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=4)
    ctk.CTkLabel(row2, text="Nombre d’IP souhaité / sous-réseau").grid(row=0, column=0, padx=(0,8))
    entry_wanted = ctk.CTkEntry(row2, placeholder_text="ex: 50", width=120)
    entry_wanted.grid(row=0, column=1)

    ctk.CTkButton(frame, text="Calculer", command=calculer).pack(pady=8)

    text_result = ctk.CTkTextbox(frame, width=480, height=250)
    text_result.pack(pady=6)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root)).pack(pady=4)

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

    frame = ctk.CTkFrame(root, corner_radius=15, width=520, height=380)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Calcul adresse réseau", font=("Arial", 18, "bold")).pack(pady=(12, 8))

    # Ligne 1 : IP
    row1 = ctk.CTkFrame(frame)
    row1.pack(pady=6)
    ctk.CTkLabel(row1, text="IP").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.1.42", width=170)
    entry_ip.grid(row=0, column=1)

    # Ligne 2 : Masque
    row2 = ctk.CTkFrame(frame)
    row2.pack(pady=6)
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: 24 ou 255.255.255.0", width=180)
    entry_mask.grid(row=0, column=1)

    # Ligne 3 : Choix Classful / Classless
    row3 = ctk.CTkFrame(frame)
    row3.pack(pady=6)
    var_mode = ctk.StringVar(value="classless")
    ctk.CTkRadioButton(row3, text="Classless (CIDR)", variable=var_mode, value="classless").grid(row=0, column=0,
                                                                                                 padx=10)
    ctk.CTkRadioButton(row3, text="Classful", variable=var_mode, value="classful").grid(row=0, column=1, padx=10)

    ctk.CTkButton(frame, text="Calculer", command=calculer).pack(pady=10)

    text_result = ctk.CTkTextbox(frame, width=480, height=200)
    text_result.pack(pady=6)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root)).pack(pady=4)

def page_verif_ip_reseau(root):
    clear_root(root)

    def verifier():
        ip = entry_ip.get().strip()
        network_ip = entry_network_ip.get().strip()
        network_mask = entry_network_mask.get().strip()

        if not ip or not network_ip or not network_mask:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        # Appel de la méthode robuste
        result, first, last, error = network_service.define_ip_in_network(ip, network_ip, network_mask)

        text_result.delete("1.0", "end")  # Clear avant affichage

        if error:
            text_result.insert("end", f"Erreur : {error}")
        elif result:
            text_result.insert("end", f"L'adresse IP {ip} appartient au réseau {network_ip}/{network_mask}\n")
            text_result.insert("end", f"Plage d'IP du réseau : {first} → {last}")
        else:
            text_result.insert("end",
                               f"L'adresse IP {ip} **n'appartient pas** au réseau {network_ip}/{network_mask}")

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

    # Bouton Vérifier
    ctk.CTkButton(frame, text="Vérifier", command=verifier, height=40, corner_radius=10).pack(pady=10, fill="x",
                                                                                              padx=40)

    # Zone résultat
    text_result = ctk.CTkTextbox(frame)
    text_result.pack(pady=6, expand=True, fill="both", padx=20)

    # Bouton Retour
    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root), height=40, corner_radius=10).pack(
        pady=8, fill="x", padx=40)

