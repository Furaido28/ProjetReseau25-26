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

def show_custom_message(title, message, type_="info", parent=None):
    """
    Affiche une notification toast avec une croix (fermer)
    et un bouton 'pin' (garder affiché).
    """
    colors = {
        "info": "#3B82F6",
        "success": "#22C55E",
        "warning": "#EAB308",
        "error": "#EF4444",
    }
    color = colors.get(type_, "#3B82F6")

    # Conteneur du toast
    toast = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
    toast.place(relx=0.5, rely=0.95, anchor="s")

    # Variables de contrôle
    is_pinned = ctk.BooleanVar(value=False)

    # Fonctions
    def close_toast():
        toast.destroy()

    def toggle_pin():
        is_pinned.set(not is_pinned.get())
        if is_pinned.get():
            pin_button.configure(text="📌", fg_color="#1E3A8A")
        else:
            pin_button.configure(text="📍", fg_color=color)
            # Repart sur un timer pour auto-destruction
            toast.after(3000, lambda: toast.destroy() if not is_pinned.get() else None)

    # Contenu principal
    header = ctk.CTkFrame(toast, fg_color="transparent")
    header.pack(fill="x", padx=5, pady=(5, 0))

    ctk.CTkLabel(header, text=title, font=("Arial", 14, "bold"), text_color="white", anchor="w").pack(side="left", padx=(8, 0))

    # Boutons Pin & Close
    pin_button = ctk.CTkButton(
        header,
        text="📍",
        width=28,
        height=24,
        corner_radius=8,
        fg_color=color,
        hover_color="#1E3A8A",
        text_color="white",
        font=("Arial", 13),
        command=toggle_pin
    )
    pin_button.pack(side="right", padx=(0, 3))

    close_button = ctk.CTkButton(
        header,
        text="✖",
        width=28,
        height=24,
        corner_radius=8,
        fg_color=color,
        hover_color="#991B1B",
        text_color="white",
        font=("Arial", 13, "bold"),
        command=close_toast
    )
    close_button.pack(side="right", padx=(0, 5))

    # Message
    ctk.CTkLabel(
        toast,
        text=message,
        text_color="white",
        justify="center",
        wraplength=1000,
        font=("Arial", 13)
    ).pack(padx=15, pady=(0, 10))

    # Animation d’apparition douce
    toast.attributes = getattr(toast, "attributes", lambda *a, **kw: None)
    try:
        toast.attributes("-alpha", 0.0)
        for i in range(0, 11):
            toast.after(i * 30, lambda a=i: toast.attributes("-alpha", a / 10))
    except Exception:
        pass  # ignore si non supporté (Linux ou mac)

    # Disparaît automatiquement après 3 secondes si pas épinglé
    toast.after(3000, lambda: toast.destroy() if not is_pinned.get() else None)

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

        text_result.configure(state="normal")
        text_result.delete("1.0", "end")

        if error:
            text_result.insert("end", f"Erreur : {error}")
        elif result:
            text_result.insert("end", f"✅ L'adresse IP {ip} appartient au réseau {network_ip}/{network_mask}\n\n")
            text_result.insert("end", f"Plage d'adresses : {first} → {last}")
        else:
            text_result.insert("end", f"❌ L'adresse IP {ip} n'appartient pas au réseau {network_ip}/{network_mask}")

        text_result.configure(state="disabled")

    # --- Cadre principal ---
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(
        frame,
        text="Vérification d'une adresse IP dans un réseau",
        font=("Arial", 22, "bold")
    ).pack(pady=(10, 20))

    # --- Zone formulaire ---
    form_frame = ctk.CTkFrame(frame, corner_radius=10)
    form_frame.pack(fill="x", padx=25, pady=(5, 15))

    # Ligne 1 : IP à tester
    row1 = ctk.CTkFrame(form_frame)
    row1.pack(pady=8, fill="x")
    ctk.CTkLabel(row1, text="IP à tester :", font=("Arial", 13)).grid(row=0, column=0, padx=(0, 8))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex : 192.168.1.42", height=32)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Ligne 2 : IP réseau
    row2 = ctk.CTkFrame(form_frame)
    row2.pack(pady=8, fill="x")
    ctk.CTkLabel(row2, text="IP réseau :", font=("Arial", 13)).grid(row=0, column=0, padx=(0, 8))
    entry_network_ip = ctk.CTkEntry(row2, placeholder_text="ex : 192.168.1.0", height=32)
    entry_network_ip.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Ligne 3 : Masque
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=8, fill="x")
    ctk.CTkLabel(row3, text="Masque :", font=("Arial", 13)).grid(row=0, column=0, padx=(0, 8))
    entry_network_mask = ctk.CTkEntry(row3, placeholder_text="ex : 24 ou 255.255.255.0", height=32)
    entry_network_mask.grid(row=0, column=1, sticky="ew")
    row3.grid_columnconfigure(1, weight=1)

    # --- Ligne de boutons (Vérifier + Retour) ---
    btns_frame = ctk.CTkFrame(frame)
    btns_frame.pack(fill="x", padx=40, pady=(5, 5))

    btn_verif = ctk.CTkButton(btns_frame, text="Vérifier", command=verifier, height=40)
    btn_back = ctk.CTkButton(btns_frame, text="Retour menu", command=lambda: page_menu(root), height=40)

    btns_frame.grid_columnconfigure(0, weight=1)
    btns_frame.grid_columnconfigure(1, weight=1)
    btn_verif.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=6)
    btn_back.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=6)

    # --- Zone de résultat ---
    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=25, pady=(10, 10))

    ctk.CTkLabel(
        result_frame,
        text="Résultat de la vérification",
        font=("Arial", 14, "bold")
    ).pack(pady=(10, 5))

    text_result = ctk.CTkTextbox(result_frame, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.pack(expand=True, fill="both", padx=10, pady=(0, 10))

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
            mask_to_use = mask if mask else None
            result = network_service.calculate(ip, mask_to_use, is_classful)

            text_result.configure(state="normal")
            text_result.delete("1.0", "end")
            text_result.insert("end", result)
            text_result.configure(state="disabled")

        except Exception as e:
            text_result.configure(state="normal")
            text_result.delete("1.0", "end")
            text_result.insert("end", f"Erreur : {e}")
            text_result.configure(state="disabled")

    # === Interface ===
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    # Titre
    ctk.CTkLabel(
        frame,
        text="🔍 Calcul d’adresse réseau",
        font=("Arial", 22, "bold")
    ).pack(pady=(10, 20))

    # --- Zone formulaire ---
    form_frame = ctk.CTkFrame(frame, corner_radius=10)
    form_frame.pack(fill="x", padx=30, pady=(10, 10))

    # Ligne IP
    row1 = ctk.CTkFrame(form_frame)
    row1.pack(pady=8, fill="x")
    ctk.CTkLabel(row1, text="Adresse IP :", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=(0, 8))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex : 192.168.1.42", height=32)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Ligne masque
    row2 = ctk.CTkFrame(form_frame)
    row2.pack(pady=8, fill="x")
    ctk.CTkLabel(row2, text="Masque :", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=(0, 8))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex : 24 ou 255.255.255.0", height=32)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Ligne mode
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=8)
    var_mode = ctk.StringVar(value="classless")
    ctk.CTkRadioButton(row3, text="Classless (CIDR)", variable=var_mode, value="classless").pack(side="left", padx=10)
    ctk.CTkRadioButton(row3, text="Classful", variable=var_mode, value="classful").pack(side="left", padx=10)

    # --- Boutons Calculer + Retour ---
    btns_frame = ctk.CTkFrame(frame)
    btns_frame.pack(fill="x", padx=40, pady=(10, 0))
    btn_calc = ctk.CTkButton(btns_frame, text="Calculer", command=calculer, height=40)
    btn_back = ctk.CTkButton(btns_frame, text="Retour menu", command=lambda: page_menu(root), height=40)

    btns_frame.grid_columnconfigure(0, weight=1)
    btns_frame.grid_columnconfigure(1, weight=1)
    btn_calc.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=8)
    btn_back.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=8)

    # --- Zone résultat ---
    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=25, pady=(10, 15))

    ctk.CTkLabel(
        result_frame,
        text="Résultat du calcul",
        font=("Arial", 14, "bold")
    ).pack(pady=(10, 5))

    text_result = ctk.CTkTextbox(result_frame, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.pack(expand=True, fill="both", padx=10, pady=(0, 10))


# ------------------ PAGE CALCUL et Verif ADRESSE RESEAU ------------------

def page_decoupe_mode(root):
    clear_root(root)

    def verifier():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode = var_mode.get()

        if not ip or not mask or not val:
            show_custom_message("Erreur", "IP, Masque et Valeur sont obligatoires.", "error")
            return

        try:
            val = int(val)
            if val <= 0:
                raise ValueError
        except ValueError:
            show_custom_message("Erreur", "La valeur doit être un entier positif.", "error")
            return

        try:
            ip_cidr = f"{ip}/{mask}"
            if mode == "nb_sr":
                report = network_service.verify_decoupe_possible(ip_cidr, nb_sr=val)
            else:
                report = network_service.verify_decoupe_possible(ip_cidr, nb_ips=val)

            # Message dynamique selon le contenu du rapport
            if report.startswith("✅"):
                show_custom_message("Vérification réussie", report, "success")
            elif report.startswith("❌"):
                show_custom_message("Vérification impossible", report, "error")
            else:
                show_custom_message("Information", report, "info")

        except Exception as e:
            show_custom_message("Erreur", str(e), "error")

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
            sr, net, mask_val, first, last, bc, nb = [""] * 7
            for l in lines:
                if l.startswith("SR"):
                    if sr:
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
            if sr:
                tree.insert("", "end", values=(sr, net, mask_val, first, last, bc, nb))

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def enregistrer():
        messagebox.showinfo("OK", "Les champs sont enregistrés ✔️")

    # === LAYOUT PRINCIPAL ===
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Découpe réseau (Point 4)", font=("Arial", 20, "bold")).pack(pady=15)

    # --- Zone formulaire ---
    form_frame = ctk.CTkFrame(frame)
    form_frame.pack(fill="x", padx=20, pady=6)

    # --- Boutons Vérifier - Calculer - Enregistrer ---------------------
    buttons_row = ctk.CTkFrame(frame)
    buttons_row.pack(pady=(6, 0), fill="x", padx=40)

    btn_verif = ctk.CTkButton(buttons_row, text="Vérifier", command=verifier, height=40)
    btn_calc = ctk.CTkButton(buttons_row, text="Calculer", command=calculer, height=40)
    btn_save = ctk.CTkButton(buttons_row, text="Enregistrer", command=enregistrer, height=40)

    buttons_row.grid_columnconfigure(0, weight=1)
    buttons_row.grid_columnconfigure(1, weight=1)
    buttons_row.grid_columnconfigure(2, weight=1)

    btn_verif.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=6)
    btn_calc.grid(row=0, column=1, sticky="ew", padx=6, pady=6)
    btn_save.grid(row=0, column=2, sticky="ew", padx=(6, 0), pady=6)

    # --- Bouton Retour juste en dessous des 3 autres ---
    ctk.CTkButton(
        frame,
        text="Retour menu",
        command=lambda: page_menu(root),
        height=40
    ).pack(pady=(10, 10), fill="x", padx=40)

    # IP réseau
    row1 = ctk.CTkFrame(form_frame)
    row1.pack(pady=6, fill="x")
    ctk.CTkLabel(row1, text="IP réseau").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.0.0", height=30)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Masque
    row2 = ctk.CTkFrame(form_frame)
    row2.pack(pady=6, fill="x")
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: 24 ou 255.255.255.0", height=30)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Choix du mode
    var_mode = ctk.StringVar(value="nb_ips")
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=6)
    ctk.CTkRadioButton(row3, text="Par nombre d'IPs / SR", variable=var_mode, value="nb_ips").pack(side="left", padx=8)
    ctk.CTkRadioButton(row3, text="Par nombre de sous-réseaux", variable=var_mode, value="nb_sr").pack(side="left", padx=8)

    # Valeur
    row4 = ctk.CTkFrame(form_frame)
    row4.pack(pady=6, fill="x")
    ctk.CTkLabel(row4, text="Valeur").grid(row=0, column=0, padx=(0, 6))
    entry_value = ctk.CTkEntry(row4, placeholder_text="ex: 8", height=30)
    entry_value.grid(row=0, column=1, sticky="ew")
    row4.grid_columnconfigure(1, weight=1)

    # --- Tableau des résultats ---
    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=10, pady=10)

    columns = ("SR", "Réseau", "Masque", "1ère IP", "Dernière IP", "Broadcast", "Nb IPs")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    tree.pack(expand=True, fill="both", padx=10, pady=10)
