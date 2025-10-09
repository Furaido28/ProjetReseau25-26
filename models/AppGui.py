import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox
from models.SecurityManager import SecurityManager
from models.NetworkService import NetworkService

user = None

# ================== SERVICES ==================
security = SecurityManager("bdd/projetReseau.db")
network_service = NetworkService()

# ================== OUTILS GÉNÉRAUX ==================
def clear_root(root):
    """Efface tout le contenu de la fenêtre."""
    for widget in root.winfo_children():
        widget.destroy()


def show_custom_message(title, message, type_="info", parent=None):
    """Affiche une notification toast avec options épingler/fermer."""
    colors = {
        "info": "#3B82F6",
        "success": "#22C55E",
        "warning": "#EAB308",
        "error": "#EF4444",
    }
    color = colors.get(type_, "#3B82F6")

    toast = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
    toast.place(relx=0.5, rely=0.95, anchor="s")

    is_pinned = ctk.BooleanVar(value=False)

    def close_toast():
        toast.destroy()

    def toggle_pin():
        is_pinned.set(not is_pinned.get())
        if is_pinned.get():
            pin_button.configure(text="📌", fg_color="#1E3A8A")
        else:
            pin_button.configure(text="📍", fg_color=color)
            toast.after(3000, lambda: toast.destroy() if not is_pinned.get() else None)

    header = ctk.CTkFrame(toast, fg_color="transparent")
    header.pack(fill="x", padx=5, pady=(5, 0))

    ctk.CTkLabel(header, text=title, font=("Arial", 14, "bold"),
                 text_color="white", anchor="w").pack(side="left", padx=(8, 0))

    pin_button = ctk.CTkButton(header, text="📍", width=28, height=24,
                               corner_radius=8, fg_color=color, hover_color="#1E3A8A",
                               text_color="white", font=("Arial", 13),
                               command=toggle_pin)
    pin_button.pack(side="right", padx=(0, 3))

    close_button = ctk.CTkButton(header, text="✖", width=28, height=24,
                                 corner_radius=8, fg_color=color, hover_color="#991B1B",
                                 text_color="white", font=("Arial", 13, "bold"),
                                 command=close_toast)
    close_button.pack(side="right", padx=(0, 5))

    ctk.CTkLabel(toast, text=message, text_color="white",
                 justify="center", wraplength=1000, font=("Arial", 13)
                 ).pack(padx=15, pady=(0, 10))

    try:
        toast.attributes("-alpha", 0.0)
        for i in range(0, 11):
            toast.after(i * 30, lambda a=i: toast.attributes("-alpha", a / 10))
    except Exception:
        pass

    toast.after(3000, lambda: toast.destroy() if not is_pinned.get() else None)


def show_input_dialog(title: str, message: str) -> str | None:
    """
    Affiche une boîte de dialogue CTk pour saisir une valeur.
    Retourne la chaîne saisie, ou None si annulé.
    """
    result = {"value": None}

    # Création de la fenêtre
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    dialog.geometry("350x180")
    dialog.resizable(False, False)
    dialog.grab_set()  # bloque les interactions avec la fenêtre principale

    # Centrer la fenêtre
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) // 2
    y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) // 3
    dialog.geometry(f"+{x}+{y}")

    # Contenu
    frame = ctk.CTkFrame(dialog, corner_radius=12)
    frame.pack(expand=True, fill="both", padx=15, pady=15)

    ctk.CTkLabel(frame, text=message, wraplength=300, font=("Arial", 14)).pack(pady=(10, 10))

    entry = ctk.CTkEntry(frame, height=35, placeholder_text="Entrez une valeur ici...")
    entry.pack(pady=(0, 15), fill="x", padx=10)
    entry.focus_set()

    def on_ok():
        result["value"] = entry.get().strip()
        dialog.destroy()

    def on_cancel():
        result["value"] = None
        dialog.destroy()

    btn_frame = ctk.CTkFrame(frame)
    btn_frame.pack(pady=(5, 5))
    ctk.CTkButton(btn_frame, text="OK", command=on_ok, width=100).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Annuler", command=on_cancel, width=100).pack(side="right", padx=5)

    dialog.wait_window()  # bloque jusqu’à fermeture
    return result["value"]

# ================== PAGE CRÉATION MOT DE PASSE ==================
def page_creer_mdp(root):
    clear_root(root)

    def save_password():
        pwd = entry_password.get()
        if not pwd.strip():
            messagebox.showerror("Erreur", "Mot de passe vide interdit.")
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

    ctk.CTkButton(frame, text="Enregistrer", command=save_password,
                  height=40, corner_radius=10).pack(pady=15, padx=40, fill="x")


# ================== PAGE CONNEXION ==================
def page_connexion(root):
    clear_root(root)

    def login():
        username = entry_user.get().strip()
        pwd = entry_password.get()
        if security.verify_password(pwd):
            root.current_user = username  # ou un dict/objet user complet
            messagebox.showinfo("Succès", f"Bienvenue {username} !")
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

    ctk.CTkButton(frame, text="Connexion", command=login,
                  height=40, corner_radius=10).pack(pady=20, padx=40, fill="x")
    root.bind("<Return>", lambda event: login())


# ================== PAGE MENU PRINCIPAL ==================
def page_menu(root):
    clear_root(root)
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    username = getattr(root, "current_user", None) or "invité"

    ctk.CTkLabel(frame, text=f"Menu principal, bienvenu {username}" , font=("Arial", 22, "bold")).pack(pady=20)

    ctk.CTkButton(frame, text="Calcul adresse réseau",
                  command=lambda: page_adresse_reseau(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)
    ctk.CTkButton(frame, text="Vérification d'une adresse IP",
                  command=lambda: page_verif_ip_reseau(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)
    ctk.CTkButton(frame, text="Découpe par nb SR ou nb IP",
                  command=lambda: page_decoupe_mode(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)
    ctk.CTkButton(frame, text="Vérification d'une découpe VLSM",
                  command=lambda: page_verif_decoupe_vlsm(root),
                  height=40, corner_radius=10).pack(pady=10, fill="x", padx=60)


# ================== PAGE VERIFICATION IP ==================
def page_verif_ip_reseau(root):
    clear_root(root)

    def verifier():
        ip = entry_ip.get().strip()
        network_ip = entry_network_ip.get().strip()
        network_mask = entry_network_mask.get().strip()

        if not ip or not network_ip or not network_mask:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        if not network_mask.startswith("/"):
            messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
            return

        network_mask = network_mask[1:]  # on retire le "/"

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

    # Interface
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Vérification d'une adresse IP dans un réseau",
                 font=("Arial", 22, "bold")).pack(pady=(10, 20))

    form_frame = ctk.CTkFrame(frame, corner_radius=10)
    form_frame.pack(fill="x", padx=25, pady=(5, 15))

    def make_row(parent, label, placeholder):
        row = ctk.CTkFrame(parent)
        row.pack(pady=8, fill="x")
        ctk.CTkLabel(row, text=label, font=("Arial", 13)).grid(row=0, column=0, padx=(0, 8))
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, height=32)
        entry.grid(row=0, column=1, sticky="ew")
        row.grid_columnconfigure(1, weight=1)
        return entry

    entry_ip = make_row(form_frame, "IP à tester :", "ex : 192.168.1.42")
    entry_network_ip = make_row(form_frame, "IP réseau :", "ex : 192.168.1.0")
    entry_network_mask = make_row(form_frame, "Masque :", "ex : /24 ou /255.255.255.0")

    btns = ctk.CTkFrame(frame)
    btns.pack(fill="x", padx=40, pady=(5, 5))
    ctk.CTkButton(btns, text="Vérifier", command=verifier, height=40).grid(row=0, column=0, sticky="ew", padx=(0, 8))
    ctk.CTkButton(btns, text="Retour menu", command=lambda: page_menu(root),
                  height=40).grid(row=0, column=1, sticky="ew", padx=(8, 0))
    btns.grid_columnconfigure(0, weight=1)
    btns.grid_columnconfigure(1, weight=1)

    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=25, pady=(10, 10))
    ctk.CTkLabel(result_frame, text="Résultat", font=("Arial", 14, "bold")).pack(pady=(10, 5))
    text_result = ctk.CTkTextbox(result_frame, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.pack(expand=True, fill="both", padx=10, pady=(0, 10))


# ================== PAGE CALCUL ADRESSE RESEAU ==================
def page_adresse_reseau(root):
    clear_root(root)

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode = var_mode.get()

        if not ip:
            messagebox.showerror("Erreur", "L'adresse IP est obligatoire.")
            return

        if mode == "classless":
            if not mask:
                messagebox.showerror("Erreur", "Le masque est obligatoire en mode classless.")
                return
            if not mask.startswith("/"):
                messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
                return
            mask = mask[1:]  # retire le "/"

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

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Calcul d’adresse réseau",
                 font=("Arial", 22, "bold")).pack(pady=(10, 20))

    form_frame = ctk.CTkFrame(frame, corner_radius=10)
    form_frame.pack(fill="x", padx=30, pady=(10, 10))

    def row(label, placeholder):
        row = ctk.CTkFrame(form_frame)
        row.pack(pady=8, fill="x")
        ctk.CTkLabel(row, text=label, font=("Arial", 13, "bold")).grid(row=0, column=0, padx=(0, 8))
        entry = ctk.CTkEntry(row, placeholder_text=placeholder, height=32)
        entry.grid(row=0, column=1, sticky="ew")
        row.grid_columnconfigure(1, weight=1)
        return entry

    entry_ip = row("Adresse IP :", "ex : 192.168.1.42")
    entry_mask = row("Masque :", "ex : /24 ou /255.255.255.0")

    var_mode = ctk.StringVar(value="classless")
    mode_row = ctk.CTkFrame(form_frame)
    mode_row.pack(pady=8)
    ctk.CTkRadioButton(mode_row, text="Classless (CIDR)", variable=var_mode, value="classless").pack(side="left", padx=10)
    ctk.CTkRadioButton(mode_row, text="Classful", variable=var_mode, value="classful").pack(side="left", padx=10)

    btns = ctk.CTkFrame(frame)
    btns.pack(fill="x", padx=40, pady=(10, 0))
    ctk.CTkButton(btns, text="Calculer", command=calculer, height=40).grid(row=0, column=0, sticky="ew", padx=(0, 8))
    ctk.CTkButton(btns, text="Retour menu", command=lambda: page_menu(root),
                  height=40).grid(row=0, column=1, sticky="ew", padx=(8, 0))
    btns.grid_columnconfigure(0, weight=1)
    btns.grid_columnconfigure(1, weight=1)

    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=25, pady=(10, 15))
    ctk.CTkLabel(result_frame, text="Résultat du calcul", font=("Arial", 14, "bold")).pack(pady=(10, 5))
    text_result = ctk.CTkTextbox(result_frame, corner_radius=8, wrap="word", font=("Consolas", 13))
    text_result.pack(expand=True, fill="both", padx=10, pady=(0, 10))


# ================== PAGE DECOUPE PAR NB SR / NB IP ==================
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

        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0", "error")
            return

        mask = mask[1:]

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

        if not mask.startswith("/"):
            messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
            return

        mask = mask[1:]

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

            # Vide le tableau avant rechargement
            for item in tree.get_children():
                tree.delete(item)

            # Extraction et affichage des résultats
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
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode = var_mode.get()
        value = entry_value.get().strip()

        # validations
        if not ip or not mask:
            show_custom_message("Erreur", "IP et masque sont obligatoires pour enregistrer.", "error")
            return

        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0", "error")
            return

        # normaliser le masque (on enlève le "/")
        mask_clean = mask[1:].strip()

        # récupérer le nom via ta input box CTk
        name = show_input_dialog("Nom de découpe", "Veuillez entrer le nom de la découpe :")
        if not name:
            show_custom_message("Info", "Enregistrement annulé.", "info")
            return

        responsable = getattr(root, "current_user", None) or "invité"

        try:
            # imports ici pour éviter les imports cycliques au chargement
            from repository.DecoupeRepository import DecoupeRepository
            from models.Decoupe import Decoupe

            repo = DecoupeRepository()

            # créer l'objet métier
            decoupe = Decoupe(
                name=name.strip(),
                responsable_name=responsable,
                base_ip=ip,
                base_mask=mask_clean,
                mode=mode,
                value=value,
            )

            # insertion en base
            decoupe_id = repo.insert_decoupe(decoupe)

            # ✅ succès (pas de messagebox, on reste cohérent avec ton show_custom_message)
            show_custom_message("Succès", f"Découpe enregistrée (ID: {decoupe_id})", "success")

        except ValueError as ve:
            # ex.: contrainte UNIQUE sur name
            show_custom_message("Erreur", str(ve), "error")
        except Exception as e:
            show_custom_message("Erreur", f"Impossible d'enregistrer la découpe : {e}", "error")

    # --- LAYOUT ---
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Découpe réseau", font=("Arial", 20, "bold")).pack(pady=15)

    form_frame = ctk.CTkFrame(frame)
    form_frame.pack(fill="x", padx=20, pady=6)

    row1 = ctk.CTkFrame(form_frame)
    row1.pack(pady=6, fill="x")
    ctk.CTkLabel(row1, text="IP réseau").grid(row=0, column=0, padx=(0, 6))
    entry_ip = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.0.0", height=30)
    entry_ip.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    row2 = ctk.CTkFrame(form_frame)
    row2.pack(pady=6, fill="x")
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: /24 ou /255.255.255.0", height=30)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    var_mode = ctk.StringVar(value="nb_ips")
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=6)
    ctk.CTkRadioButton(row3, text="Par nombre d'IPs / SR", variable=var_mode, value="nb_ips").pack(side="left", padx=8)
    ctk.CTkRadioButton(row3, text="Par nombre de sous-réseaux", variable=var_mode, value="nb_sr").pack(side="left", padx=8)

    row4 = ctk.CTkFrame(form_frame)
    row4.pack(pady=6, fill="x")
    ctk.CTkLabel(row4, text="Valeur").grid(row=0, column=0, padx=(0, 6))
    entry_value = ctk.CTkEntry(row4, placeholder_text="ex: 8", height=30)
    entry_value.grid(row=0, column=1, sticky="ew")
    row4.grid_columnconfigure(1, weight=1)

    buttons_row = ctk.CTkFrame(frame)
    buttons_row.pack(pady=(6, 0), fill="x", padx=40)
    for i, (t, c) in enumerate([("Vérifier", verifier), ("Calculer", calculer), ("Enregistrer", enregistrer)]):
        ctk.CTkButton(buttons_row, text=t, command=c, height=40).grid(row=0, column=i, sticky="ew", padx=4, pady=6)
        buttons_row.grid_columnconfigure(i, weight=1)

    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root),
                  height=40).pack(pady=(10, 10), fill="x", padx=40)

    result_frame = ctk.CTkFrame(frame, corner_radius=10)
    result_frame.pack(expand=True, fill="both", padx=10, pady=10)

    columns = ("SR", "Réseau", "Masque", "1ère IP", "Dernière IP", "Broadcast", "Nb IPs")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

"""
Point 5 - Vérification Découpe VLSM
"""

import customtkinter as ctk
from tkinter import ttk

# NOTE: suppose que clear_root(root), show_custom_message(title, msg, type),
# et page_menu(root) existent déjà dans ton projet (comme dans ta page de référence).

MAX_SR = 100

def page_verif_decoupe_vlsm(root):
    clear_root(root)

    # --- LAYOUT racine (design calqué sur ta page_decoupe_mode) ---
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Vérif. découpe VLSM", font=("Arial", 20, "bold")).pack(pady=15)

    form_frame = ctk.CTkFrame(frame)
    form_frame.pack(fill="x", padx=20, pady=6)

    # Ligne IP réseau
    row1 = ctk.CTkFrame(form_frame)
    row1.pack(pady=6, fill="x")
    ctk.CTkLabel(row1, text="IP réseau").grid(row=0, column=0, padx=(0, 6))
    entry_network = ctk.CTkEntry(row1, placeholder_text="ex: 192.168.0.0", height=30)
    entry_network.grid(row=0, column=1, sticky="ew")
    row1.grid_columnconfigure(1, weight=1)

    # Ligne Masque
    row2 = ctk.CTkFrame(form_frame)
    row2.pack(pady=6, fill="x")
    ctk.CTkLabel(row2, text="Masque").grid(row=0, column=0, padx=(0, 6))
    entry_mask = ctk.CTkEntry(row2, placeholder_text="ex: /24 ou /255.255.255.0", height=30)
    entry_mask.grid(row=0, column=1, sticky="ew")
    row2.grid_columnconfigure(1, weight=1)

    # Ligne Nombre de sous-réseaux
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=6, fill="x")
    ctk.CTkLabel(row3, text="Nombre de sous-réseaux").grid(row=0, column=0, padx=(0, 6))
    entry_subnet_count = ctk.CTkEntry(row3, placeholder_text=f"1 à {MAX_SR}", height=30)
    entry_subnet_count.grid(row=0, column=1, sticky="ew")
    row3.grid_columnconfigure(1, weight=1)

    # Boutons d'action en haut (cohérent avec ta page)
    buttons_row = ctk.CTkFrame(frame)
    buttons_row.pack(pady=(6, 0), fill="x", padx=40)

    # Conteneur scrollable pour les champs dynamiques
    dynamic_frame = ctk.CTkFrame(frame, corner_radius=10)
    dynamic_frame.pack(expand=True, fill="both", padx=10, pady=10)

    scroll = ctk.CTkScrollableFrame(dynamic_frame)
    scroll.pack(expand=True, fill="both", padx=10, pady=10)

    # En-têtes visuels
    header = ctk.CTkFrame(scroll)
    header.grid(row=0, column=0, sticky="ew", pady=(0, 6))
    ctk.CTkLabel(header, text="#", width=40, anchor="w").grid(row=0, column=0, padx=(0, 8))
    ctk.CTkLabel(header, text="Nom (optionnel)", anchor="w").grid(row=0, column=1, padx=8)
    ctk.CTkLabel(header, text="Hôtes requis", anchor="w").grid(row=0, column=2, padx=8)
    header.grid_columnconfigure(1, weight=1)

    # Stockage des entrées dynamiques
    subnet_entries = []  # liste de dicts {name_entry, hosts_entry}

    def generer_champs():
        # Nettoyage
        for child in scroll.winfo_children():
            if child is header:
                continue
            child.destroy()
        subnet_entries.clear()

        # Validation nombre
        raw = entry_subnet_count.get().strip()
        if not raw:
            show_custom_message("Erreur", "Veuillez indiquer un nombre de sous-réseaux.", "error")
            return
        try:
            n = int(raw)
        except ValueError:
            show_custom_message("Erreur", "Le nombre de sous-réseaux doit être un entier.", "error")
            return
        if n <= 0:
            show_custom_message("Attention", "Le nombre doit être supérieur à 0.", "info")
            return
        if n > MAX_SR:
            show_custom_message("Limite", f"Maximum {MAX_SR} sous-réseaux. La valeur sera réduite à {MAX_SR}.", "info")
            n = MAX_SR

        # Génération des lignes
        for i in range(n):
            row = ctk.CTkFrame(scroll)
            row.grid(row=i+1, column=0, sticky="ew", pady=4)

            ctk.CTkLabel(row, text=str(i+1), width=40, anchor="w").grid(row=0, column=0, padx=(0, 8))
            name_entry = ctk.CTkEntry(row, placeholder_text=f"SR{i+1}", height=30)
            name_entry.grid(row=0, column=1, sticky="ew", padx=8)
            hosts_entry = ctk.CTkEntry(row, placeholder_text="ex: 50", height=30)
            hosts_entry.grid(row=0, column=2, padx=8)

            row.grid_columnconfigure(1, weight=1)

            subnet_entries.append({
                "name_entry": name_entry,
                "hosts_entry": hosts_entry,
            })

    # Bouton pour générer les champs
    ctk.CTkButton(buttons_row, text="Générer les champs", command=generer_champs, height=40).grid(
        row=0, column=0, sticky="ew", padx=4, pady=6
    )
    buttons_row.grid_columnconfigure(0, weight=1)

    # Bouton Retour (cohérence de design)
    ctk.CTkButton(frame, text="Retour menu", command=lambda: page_menu(root), height=40).pack(
        pady=(10, 10), fill="x", padx=40
    )

    # Optionnel: pré-générer 1 ligne vide au chargement
    entry_subnet_count.insert(0, "1")
    generer_champs()




