import customtkinter as ctk
from tkinter import messagebox

from models.Decoupe import Decoupe
from models.SecurityManager import SecurityManager
from models.NetworkService import NetworkService
from repository.DecoupeRepository import DecoupeRepository


security = SecurityManager("bdd/projetReseau.db")
network_service = NetworkService()
repo = DecoupeRepository("bdd/projetReseau.db")

def clear_root(root):
    for widget in root.winfo_children():
        widget.destroy()


"""
        Page de création de mot de passe
"""

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


"""
        Page de connexion
"""

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


def get_current_user(root):
    return getattr(root, "current_user", None)


"""
        Page d'accueil du programme
"""

def page_menu(root):
    frame = ctk.CTkFrame(root, corner_radius=15, width=400, height=300)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Menu principal", font=("Arial", 20, "bold")).pack(pady=20)
    ctk.CTkButton(frame, text="Calcul adresse réseau", command=lambda: page_adresse_reseau(root)).pack(pady=10)
    ctk.CTkButton(frame, text="Découpe en sous-réseaux", command=lambda: page_calcul_reseau(root)).pack(pady=10)
    ctk.CTkButton(frame, text="Vérifiication d'une adresse ip", command=lambda: page_verif_ip_reseau(root)).pack(pady=10)


"""
        Point 1 - Calculer les informations d'un reseau
"""

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


"""
        Point 2 - 
"""

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


"""
        Point 3 - Calculer des découpes en sous-réseaux d'un réseau
"""

def page_calcul_reseau(root):
    # --- Reset & layout racine ---
    for w in root.winfo_children(): w.destroy()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    body = ctk.CTkFrame(root, corner_radius=15)
    body.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    for c in range(4): body.grid_columnconfigure(c, weight=1)
    body.grid_rowconfigure(4, weight=1)  # zone texte extensible

    # --- Helpers UI ---
    def labeled_entry(parent, label, row, col_label, col_entry, placeholder=""):
        ctk.CTkLabel(parent, text=label)\
            .grid(row=row, column=col_label, sticky="e", padx=(0, 6), pady=4)
        e = ctk.CTkEntry(parent, placeholder_text=placeholder)
        e.grid(row=row, column=col_entry, sticky="we", padx=(0, 12) if col_entry == 1 else 0, pady=4)
        return e

    def set_save_enabled(enabled: bool):
        btn_save.configure(state="normal" if enabled else "disabled")

    def center_on_parent(win, parent):
        win.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (win.winfo_reqwidth() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (win.winfo_reqheight() // 2)
        win.geometry(f"+{x}+{y}")

    def ask_text_modal(parent, title, prompt, placeholder=""):
        result = {"value": None}
        dlg = ctk.CTkToplevel(parent)
        dlg.title(title); dlg.transient(parent); dlg.grab_set(); dlg.resizable(False, False)

        container = ctk.CTkFrame(dlg, corner_radius=12)
        container.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(container, text=prompt).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        entry = ctk.CTkEntry(container, placeholder_text=placeholder); entry.grid(row=1, column=0, columnspan=2, sticky="we")
        info = ctk.CTkLabel(container, text="", text_color="red"); info.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))

        def on_ok(_=None):
            val = entry.get().strip()
            if not val:
                info.configure(text="Le nom est obligatoire.")
                return
            result["value"] = val
            dlg.destroy()

        ctk.CTkButton(container, text="Valider", command=on_ok).grid(row=3, column=0, pady=(12, 0), sticky="e")
        ctk.CTkButton(container, text="Annuler", command=dlg.destroy, fg_color="gray").grid(row=3, column=1, pady=(12, 0), sticky="w")
        entry.bind("<Return>", on_ok); dlg.bind("<Escape>", lambda e: dlg.destroy())
        center_on_parent(dlg, parent); entry.focus_set()
        parent.wait_window(dlg)
        return result["value"]

    # --- UI ---
    ctk.CTkLabel(body, text="Découpe de réseau", font=("Arial", 18, "bold"))\
        .grid(row=0, column=0, columnspan=4, pady=(10, 6))

    entry_ip    = labeled_entry(body, "IP",                         row=1, col_label=0, col_entry=1, placeholder="ex: 192.168.1.10")
    entry_mask  = labeled_entry(body, "Masque",                     row=1, col_label=2, col_entry=3, placeholder="ex: 24 ou 255.255.255.0")
    ctk.CTkLabel(body, text="Nombre d’IP / sous-réseau")\
        .grid(row=2, column=0, columnspan=2, sticky="w", pady=4)
    entry_wanted = ctk.CTkEntry(body, placeholder_text="ex: 50")
    entry_wanted.grid(row=2, column=2, sticky="w", pady=4)

    btn_calcul = ctk.CTkButton(body, text="Calculer"); btn_calcul.grid(row=3, column=0, columnspan=4, pady=(8, 6))
    text_result = ctk.CTkTextbox(body); text_result.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=6)

    def enregistrer():
        name = ask_text_modal(root, "Nom de la découpe",
                              "Entre un nom pour cette découpe :", "ex: Bureau_Informatique")
        if not name:
            return

        # optionnel : demander aussi le responsable
        responsable = ask_text_modal(root, "Responsable",
                                     "Nom du responsable de cette découpe :", "ex: Ethan") or "Anonyme"

        # sécuriser 'wanted'
        wanted_raw = entry_wanted.get().strip()
        try:
            wanted = int(wanted_raw)
            if wanted <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre d’IP souhaité doit être un entier positif.")
            return

        # Crée l'objet métier
        d = Decoupe(name, entry_ip.get().strip(), entry_mask.get().strip(), wanted, "classless", responsable)

        try:
            decoupe_id = repo.insert_decoupe(d)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        # Si tu as déjà la liste des sous-réseaux calculés, insère-les ici.
        # Exemple: transforme le résultat de network_service.compute_subnets(...) en une liste de dicts
        # subnets = [
        #   {"network_ip": "192.168.1.0", "mask": "255.255.255.0",
        #    "first_host": "192.168.1.1", "last_host": "192.168.1.254",
        #    "broadcast": "192.168.1.255", "nb_ip": 256},
        #   ...
        # ]
        # repo.bulk_insert_subnets(decoupe_id, subnets)

        messagebox.showinfo("Succès", f"Découpe « {name} » enregistrée (id={decoupe_id}).")

    btn_save = ctk.CTkButton(body, text="Enregistrer", command=enregistrer, state="disabled")
    btn_save.grid(row=5, column=0, columnspan=4, pady=(4, 2))

    # --- Logique calcul ---
    def calculer():
        ip, mask, wanted = entry_ip.get().strip(), entry_mask.get().strip(), entry_wanted.get().strip()
        if not ip or not mask or not wanted:
            messagebox.showerror("Erreur", "IP, Masque et Nombre d’IP sont obligatoires.")
            set_save_enabled(False); return
        try:
            wanted_int = int(wanted)
            if wanted_int <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre d’IP souhaité doit être un entier positif.")
            set_save_enabled(False); return

        try:
            result = network_service.compute_subnets(ip, mask, wanted_int)
            text_result.delete("1.0", "end")
            text_result.insert("end", result if isinstance(result, str) else str(result))
            set_save_enabled(True)
        except Exception as e:
            text_result.delete("1.0", "end")
            text_result.insert("end", f"Erreur : {e}")
            set_save_enabled(False)

    btn_calcul.configure(command=calculer)
    for e in (entry_ip, entry_mask, entry_wanted): e.bind("<Return>", calculer)

    entry_ip.focus_set()
    root.update_idletasks()
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
    # root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")  # optionnel

"""
        Point 4 -
"""


"""
        Point 5 - Calcule de la possibilité d'une découpe VLSM
"""

