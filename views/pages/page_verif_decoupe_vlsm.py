from tkinter import messagebox
import customtkinter as ctk
import tkinter.ttk as ttk

from controllers.NetworkService import NetworkService
from views.pages.page_menu import page_menu
from views.utils.tools import clear_root, show_custom_message

network_service = NetworkService()

MAX_SR = 100
NB_COLS = 3  # Nombre de colonnes pour limiter le défilement

def page_verif_decoupe_vlsm(root):
    clear_root(root)

    # --- LAYOUT racine (design similaire à page_decoupe_mode) ---
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(frame, text="Vérification découpe VLSM", font=("Arial", 20, "bold")).pack(pady=15)

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

    # Ligne Nombre de sous-réseaux + bouton "Générer" à droite
    row3 = ctk.CTkFrame(form_frame)
    row3.pack(pady=6, fill="x")
    ctk.CTkLabel(row3, text="Nombre de sous-réseaux").grid(row=0, column=0, padx=(0, 6))
    entry_subnet_count = ctk.CTkEntry(row3, placeholder_text=f"1 à {MAX_SR}", height=30)
    entry_subnet_count.grid(row=0, column=1, sticky="ew", padx=(0, 6))
    btn_generer_inline = ctk.CTkButton(row3, text="Générer", height=30)
    btn_generer_inline.grid(row=0, column=2)
    row3.grid_columnconfigure(1, weight=1)  # l'input s'étire

    # Conteneur scrollable pour les champs dynamiques
    dynamic_frame = ctk.CTkFrame(frame, corner_radius=10)
    dynamic_frame.pack(expand=True, fill="both", padx=10, pady=10)

    scroll = ctk.CTkScrollableFrame(dynamic_frame)
    scroll.pack(expand=True, fill="both", padx=10, pady=10)

    # Configurer une grille à plusieurs colonnes dans la zone scrollable
    for col in range(NB_COLS):
        scroll.grid_columnconfigure(col, weight=1, uniform="cols")

    # Stockage des entrées dynamiques (pour traitement)
    # Chaque item: {"name": "SR 1", "hosts_entry": <CTkEntry>}
    subnet_entries = []

    def generer_champs():
        # Nettoyage total du contenu scrollable
        for child in scroll.winfo_children():
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

        # Génération des cartes sur NB_COLS colonnes
        for i in range(n):
            r, c = divmod(i, NB_COLS)

            card = ctk.CTkFrame(scroll, corner_radius=12)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

            # En-tête (numéro SR)
            sr_name = f"SR {i+1}"
            ctk.CTkLabel(card, text=sr_name, font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 6))

            # Uniquement "Hôtes requis"
            row_hosts = ctk.CTkFrame(card)
            row_hosts.pack(fill="x", padx=10, pady=(0, 12))
            ctk.CTkLabel(row_hosts, text="Hôtes requis").grid(row=0, column=0, padx=(0, 6))
            hosts_entry = ctk.CTkEntry(row_hosts, placeholder_text="ex: 50", height=30)
            hosts_entry.grid(row=0, column=1, sticky="ew")
            row_hosts.grid_columnconfigure(1, weight=1)

            subnet_entries.append({
                "name": sr_name,
                "hosts_entry": hosts_entry,
            })

    # Associer le bouton inline "Générer"
    btn_generer_inline.configure(command=generer_champs)

    # --- BOUTONS DU BAS : Calculer + Retour ---
    bottom_buttons = ctk.CTkFrame(frame)
    bottom_buttons.pack(fill="x", padx=40, pady=(6, 10))

    def verifier():
        network = entry_network.get().strip()
        mask = entry_mask.get().strip()
        if not network or not mask:
            show_custom_message("Erreur", "Veuillez saisir l'IP réseau et le masque.", "error")
            return

        besoins = []
        for item in subnet_entries:
            sr = item["name"]
            raw = item["hosts_entry"].get().strip()
            try:
                h = int(raw)
                if h < 1: raise ValueError
            except ValueError:
                show_custom_message("Erreur", f"'{raw}' n'est pas un nombre d'hôtes valide pour {sr}.", "error")
                return
            besoins.append((sr, h))

        ok, msg, details = network_service.verify_vlsm(network, mask, besoins)
        if ok:
            # Petit récap lisible
            lines = [msg, "-" * 50]
            for d in details:
                lines.append(f"{d['name']}: {d['hosts']} hôtes → bloc {d['block_size']} adresses (/{d['prefix']})")
            show_custom_message("Vérification VLSM", "\n".join(lines), "info")
        else:
            # Affiche le motif d'échec + le besoin “bloquant”
            lines = [msg]
            if details:
                worst = min(details, key=lambda d: d["prefix"])
                lines.append(
                    f"Plus gros besoin rencontré : {worst['name']} → /{worst['prefix']} ({worst['block_size']} adresses).")
            show_custom_message("VLSM impossible", "\n".join(lines), "error")

    btn_calculer = ctk.CTkButton(bottom_buttons, text="Vérifier", command=verifier, height=40)
    btn_retour = ctk.CTkButton(bottom_buttons, text="Retour menu", command=lambda: page_menu(root), height=40)

    btn_calculer.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=6)
    btn_retour.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=6)
    bottom_buttons.grid_columnconfigure(0, weight=1)
    bottom_buttons.grid_columnconfigure(1, weight=1)

    # Par défaut, 3 SR et génération initiale
    entry_subnet_count.insert(0, "3")
    generer_champs()