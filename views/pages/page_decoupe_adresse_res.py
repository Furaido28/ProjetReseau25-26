from tkinter import messagebox
from typing import Optional

import customtkinter as ctk
import tkinter.ttk as ttk

from netaddr import IPAddress, AddrFormatError

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.clearRoot import clear_root
from views.utils.showCustomMessage import show_custom_message
from views.utils.showInputDialog import show_input_dialog

network_service = NetworkService()

def page_decoupe_mode(root):
    # Thème global (optionnel)
    ctk.set_appearance_mode("light")   # "light" ou "system"
    ctk.set_default_color_theme("green")

    clear_root(root)
    root.geometry("1250x700")

    # ---------------------------
    # COULEURS / STYLE
    # ---------------------------
    PRIMARY = "#34A853"
    PRIMARY_HOVER = "#2C8E47"
    DISABLED = "#7F8C8D"

    # ---------------------------
    # HELPERS BOUTONS
    # ---------------------------
    def set_btn_disabled(btn):
        btn.configure(state="disabled", fg_color=DISABLED, hover_color=DISABLED)

    def set_btn_enabled(btn):
        btn.configure(state="normal", fg_color=PRIMARY, hover_color=PRIMARY_HOVER)

    def disable_calc_and_save():
        set_btn_disabled(btn_calculer)
        set_btn_disabled(btn_enregistrer)

    # ---------------------------
    # LOGIQUE
    # ---------------------------
    def verifier() -> Optional[bool]:
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode = var_mode.get()

        if not ip or not mask or not val:
            show_custom_message("Erreur", "IP, Masque et Valeur sont obligatoires.", "error")
            return False

        try:
            IPAddress(ip)
        except AddrFormatError:
            show_custom_message("Erreur", f"L'adresse IP '{ip}' est invalide.", "error")
            return False

        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0", "error")
            return False

        mask_clean = mask[1:]

        if mode != "nb_sr" and mode != "nb_ip":
            mode = "nb_ip" if mode == "nombre d'ip total" else "nb_sr"

        try:
            val_int = int(val)
            if val_int <= 0:
                raise ValueError
        except ValueError:
            show_custom_message("Erreur", "La valeur doit être un entier positif.", "error")
            return False

        try:
            ip_cidr = f"{ip}/{mask_clean}"
            if mode == "nb_sr":
                report = network_service.verify_decoupe_possible(ip_cidr, nb_sr=val_int)
            else:
                report = network_service.verify_decoupe_possible(ip_cidr, nb_ips=val_int)

            if report.startswith("✅"):
                show_custom_message("Vérification réussie", report, "success")
                return True
            elif report.startswith("❌"):
                show_custom_message("Vérification impossible", report, "error")
            else:
                show_custom_message("Information", report, "info")
            return False
        except Exception as e:
            show_custom_message("Erreur", str(e), "error")
            return False

    def calculer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        val = entry_value.get().strip()
        mode = var_mode.get()

        if mode != "nb_sr" and mode != "nb_ip":
            mode = "nb_ip" if mode == "nombre d'ip total" else "nb_sr"

        if not ip or not mask or not val:
            messagebox.showerror("Erreur", "IP, Masque et Valeur sont obligatoires.")
            return

        if not mask.startswith("/"):
            messagebox.showerror("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0")
            return

        mask_clean = mask[1:]

        try:
            val_int = int(val)
            if val_int <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "La valeur doit être un entier positif.")
            return

        try:
            ip_cidr = f"{ip}/{mask_clean}"
            if mode == "nb_sr":
                report = network_service.compute_subnets_choice(ip_cidr, nb_sr=val_int)
            else:
                report = network_service.compute_subnets_choice(ip_cidr, nb_ips=val_int)

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

            set_btn_enabled(btn_enregistrer)
        except Exception as e:
            show_custom_message("Erreur", f"{str(e)}", "error")

    def enregistrer():
        ip = entry_ip.get().strip()
        mask = entry_mask.get().strip()
        mode = var_mode.get()
        value = entry_value.get().strip()

        if mode != "nb_sr" and mode != "nb_ip":
            mode = "nb_ip" if mode == "nombre d'ip total" else "nb_sr"

        if not ip or not mask:
            show_custom_message("Erreur", "IP et masque sont obligatoires pour enregistrer.", "error")
            return

        if not mask.startswith("/"):
            show_custom_message("Erreur", "Le masque doit commencer par '/'. Exemple : /24 ou /255.255.255.0", "error")
            return

        mask_clean = mask[1:].strip()
        name = show_input_dialog("Nom de découpe", "Veuillez entrer le nom de la découpe :")
        if not name:
            show_custom_message("Info", "Enregistrement annulé.", "info")
            return

        responsable = getattr(root, "current_user", None) or "invité"

        try:
            from repository.DecoupeRepository import DecoupeRepository
            repo = DecoupeRepository()
            decoupe_id = repo.insert_decoupe(
                name=name.strip(),
                responsable=responsable,
                base_ip=ip,
                base_mask=mask_clean,
                mode=mode,
                value=value,
            )
            show_custom_message("Succès", f"Découpe enregistrée (ID: {decoupe_id})", "success")
        except ValueError as ve:
            show_custom_message("Erreur", str(ve), "error")
        except Exception as e:
            show_custom_message("Erreur", f"Impossible d'enregistrer la découpe : {e}", "error")

    def verifier_and_enable_next():
        isOK = verifier()
        if not isOK:
            return
        set_btn_enabled(btn_calculer)

    def calculer_and_enable_next():
        calculer()
        set_btn_enabled(btn_calculer)

    # ---------------------------
    # LAYOUT VERTICAL (FORM EN HAUT, RÉSULTAT EN BAS)
    # ---------------------------
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, corner_radius=16)
    container.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
    container.grid_rowconfigure(0, weight=0)  # header
    container.grid_rowconfigure(1, weight=0)  # form
    container.grid_rowconfigure(2, weight=0)  # actions
    container.grid_rowconfigure(3, weight=1)  # results
    container.grid_columnconfigure(0, weight=1)

    # En-tête
    header = ctk.CTkFrame(container, corner_radius=16)
    header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
    header.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(
        header,
        text="Découpe réseau",
        font=("Segoe UI", 25, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(6, 0))
    ctk.CTkLabel(
        header,
        text="Cette page vous permet de créer vos découpes réseau, vérifier leur validité et les enregistrer facilement dans la base de données.",
        font=("Segoe UI", 20),
        wraplength=1150,
        justify="left"
    ).grid(row=1, column=0, sticky="w", pady=(0, 6))

    # Carte formulaire
    form_card = ctk.CTkFrame(container, corner_radius=16)
    form_card.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 8))
    form_card.grid_columnconfigure(0, weight=0)
    form_card.grid_columnconfigure(1, weight=1)

    # Variables (seulement pour le mode)
    var_mode = ctk.StringVar(value="nombre d'ip total")

    # Ligne 1 : IP
    ctk.CTkLabel(form_card, text="IP réseau", font=("Segoe UI", 15)).grid(
        row=0, column=0, sticky="e", padx=(16, 10), pady=(16, 8)
    )
    entry_ip = ctk.CTkEntry(
        form_card, placeholder_text="ex : 192.168.0.0", height=36
    )
    entry_ip.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=(16, 8))

    # Ligne 2 : Masque
    ctk.CTkLabel(form_card, text="Masque", font=("Segoe UI", 15)).grid(
        row=1, column=0, sticky="e", padx=(16, 10), pady=8
    )
    entry_mask = ctk.CTkEntry(
        form_card,
        placeholder_text="ex : /24 ou /255.255.255.0",
        height=36,
    )
    entry_mask.grid(row=1, column=1, sticky="ew", padx=(0, 16), pady=8)

    # Ligne 3 : Mode
    ctk.CTkLabel(form_card, text="Mode", font=("Segoe UI", 15)).grid(
        row=2, column=0, sticky="e", padx=(16, 10), pady=8
    )
    seg_mode = ctk.CTkSegmentedButton(
        form_card,
        values=["nombre d'ip total", "nombre de sous-réseau"],
        variable=var_mode,
        font=ctk.CTkFont(size=15, weight="bold"),

        text_color="white",
        text_color_disabled="white",

        fg_color="#979DA2",
        selected_color=PRIMARY,
        selected_hover_color=PRIMARY_HOVER,
        unselected_color="#979DA2",
        unselected_hover_color="#B3B3B3"
    )
    seg_mode.set("nombre d'ip total")
    seg_mode.grid(row=2, column=1, sticky="w", padx=(0, 16), pady=8)

    # Ligne 4 : Valeur
    ctk.CTkLabel(form_card, text="Valeur", font=("Segoe UI", 15)).grid(
        row=3, column=0, sticky="e", padx=(16, 10), pady=8
    )
    entry_value = ctk.CTkEntry(
        form_card, placeholder_text="ex : 8", height=36
    )
    entry_value.grid(row=3, column=1, sticky="ew", padx=(0, 16), pady=8)

    # Barre d’actions
    actions = ctk.CTkFrame(container, corner_radius=12)
    actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 8))
    for i in range(4):
        actions.grid_columnconfigure(i, weight=1)

    btn_verifier = ctk.CTkButton(
        actions, text="Vérifier", command=lambda: verifier_and_enable_next(),
        height=44, corner_radius=10,
        fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn_verifier.grid(row=0, column=0, sticky="ew", padx=6, pady=8)

    btn_calculer = ctk.CTkButton(
        actions, text="Calculer", command=lambda: calculer_and_enable_next(),
        height=44, corner_radius=10,
        fg_color=DISABLED, hover_color=DISABLED,
        font=("Segoe UI Semibold", 18, "bold"),
        state="disabled"
    )
    btn_calculer.grid(row=0, column=1, sticky="ew", padx=6, pady=8)

    btn_enregistrer = ctk.CTkButton(
        actions, text="Enregistrer", command=enregistrer,
        height=44, corner_radius=10,
        fg_color=DISABLED, hover_color=DISABLED,
        font=("Segoe UI Semibold", 18, "bold"),
        state="disabled"
    )
    btn_enregistrer.grid(row=0, column=2, sticky="ew", padx=6, pady=8)

    btn_retour = ctk.CTkButton(
        actions, text="Retour menu", command=lambda: page_menu(root),
        height=44, corner_radius=10,
        fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
        font=("Segoe UI Semibold", 18, "bold"),
    )
    btn_retour.grid(row=0, column=3, sticky="ew", padx=6, pady=8)

    # ---------------------------
    # Désactivation des boutons après modification dans les inputs box
    # ---------------------------
    def on_any_input_change(*_):
        disable_calc_and_save()
        for item in tree.get_children():
            tree.delete(item)

    # Seulement la trace sur le mode (les entries utilisent les placeholders)
    var_mode.trace_add("write", on_any_input_change)

    # Bind clavier pour IP / Masque / Valeur
    entry_ip.bind("<KeyRelease>", lambda e: on_any_input_change())
    entry_mask.bind("<KeyRelease>", lambda e: on_any_input_change())
    entry_value.bind("<KeyRelease>", lambda e: on_any_input_change())

    # ---------------------------
    # RÉSULTATS EN BAS (s'étend)
    # ---------------------------
    result_card = ctk.CTkFrame(container, corner_radius=16)
    result_card.grid(row=3, column=0, sticky="nsew", padx=16, pady=(8, 16))
    result_card.grid_rowconfigure(0, weight=1)
    result_card.grid_columnconfigure(0, weight=1)

    # Définition des colonnes
    columns = ("SR", "Réseau", "Masque", "1ère IP", "Dernière IP", "Broadcast", "Nb IPs")

    # Style du Treeview
    style = ttk.Style()
    style.configure("Modern.Treeview", font=("Segoe UI", 12), rowheight=28)
    style.configure("Modern.Treeview.Heading", font=("Segoe UI Semibold", 13, "bold"))
    style.map("Modern.Treeview.Heading", background=[("active", "#E8F6EF")])
    style.map("Treeview",
              background=[('selected', PRIMARY)],
              foreground=[('selected', 'white')])

    # Tableau
    tree = ttk.Treeview(result_card, columns=columns, show="headings", style="Modern.Treeview")
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=150, anchor="center")

    # Scrollbar
    vsb = ttk.Scrollbar(result_card, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 6))
    vsb.grid(row=0, column=1, sticky="ns", pady=(12, 6))
